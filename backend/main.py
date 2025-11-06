"""
FastAPI Backend for Job Upskilling Platform
Minimal routing with LangGraph-based workflow orchestration.
"""

from fastapi import FastAPI, HTTPException, Depends, UploadFile, File, Form, status
from typing import Optional
import secrets
import tempfile
import os

from app.auth.jwt_handler import get_current_user, security
from app.auth.routes_auth import router as auth_router
from app.models.schemas import (
    JDAnalysisResponse, Skill, CompanyInsight,
    GenerateRoadmapRequest, RoadmapResponse, Phase, Resource, Project
)
from app.core.orchestrator import run_workflow
from app.db.memory_store import get_jd_analysis_db, get_roadmaps_db

# Initialize FastAPI app with security configuration
app = FastAPI(
    title="Job Upskilling API",
    version="1.0.0",
    swagger_ui_init_oauth={
        "clientId": "swagger-ui",
        "usePkceWithAuthorizationCodeGrant": False,
    }
)

# Add security scheme to OpenAPI
app.openapi_schema = None  # Clear cache to regenerate

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    from fastapi.openapi.utils import get_openapi
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    # Add security scheme
    openapi_schema["components"]["securitySchemes"] = {
        "bearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Include auth routes
app.include_router(auth_router)


@app.post("/analyze-jd", response_model=JDAnalysisResponse, status_code=status.HTTP_200_OK)
async def analyze_job_description(
    jd_text: str = Form(...),
    resume: Optional[UploadFile] = File(None),
    current_user: dict = Depends(get_current_user)
):
    """
    Analyze a job description and extract skills using LangGraph workflow.
    Optionally accepts a resume to extract skills.
    """
    resume_file_path = None
    
    try:
        # Handle resume upload if provided
        if resume and resume.filename:
            if not resume.filename.endswith(".pdf"):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Only PDF files are supported"
                )
            
            # Save resume temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                content = await resume.read()
                tmp_file.write(content)
                resume_file_path = tmp_file.name
        
        # Run workflow with new structure
        result = run_workflow(
            user_id=current_user["email"],
            jd_text=jd_text,
            resume_file_path=resume_file_path
        )
        
        # Extract data from new workflow structure
        jd_data = result.get("jd_data", {})
        role_context = result.get("role_context", {})
        company_info = result.get("company_info", {})
        skill_insights = result.get("skill_insights", [])
        
        # Get role from jd_data or role_context
        role = jd_data.get("role") or role_context.get("role", "Unknown")
        
        # Convert required_skills from jd_data to Skill objects
        required_skills = jd_data.get("required_skills", [])
        skills = []
        
        # Map skills to Skill objects with priority from skill_insights
        for skill_name in required_skills:
            # Find matching skill insight for priority/importance
            insight = next(
                (si for si in skill_insights if si.get("skill_name", "").lower() == skill_name.lower()),
                None
            )
            
            # Determine priority based on skill insights or default
            priority = "must-have"  # Default for required skills
            importance_score = 8  # Default score
            
            skills.append(Skill(
                name=skill_name,
                priority=priority,
                importance_score=importance_score,
                why=insight.get("company_relevance", "") if insight else None
            ))
        
        # Convert company_info and skill_insights to CompanyInsight objects
        company_insights = []
        if company_info:
            # Create company insight from company_info
            recent_projects = company_info.get("recent_projects", [])
            tech_stack = company_info.get("common_tech_stack", [])
            
            if recent_projects or tech_stack:
                company_insights.append(CompanyInsight(
                    title=f"{company_info.get('name', 'Company')} Technology Stack",
                    url="",
                    content=company_info.get("description", ""),
                    skills_used=tech_stack,
                    relevance="high"
                ))
        
        # Generate JD ID and store
        jd_id = f"jd_{secrets.token_urlsafe(8)}"
        jd_analysis_db = get_jd_analysis_db()
        jd_analysis_db[jd_id] = {
            "jd_id": jd_id,
            "jd_text": jd_text,
            "role": role,
            "skills": [skill.dict() for skill in skills],
            "company_insights": [insight.dict() for insight in company_insights],
            "user_email": current_user["email"],
            "workflow_result": result
        }
        
        return JDAnalysisResponse(
            role=role,
            skills=skills,
            jd_id=jd_id,
            company_insights=company_insights if company_insights else None
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error analyzing JD: {str(e)}"
        )
    finally:
        # Clean up temp file
        if resume_file_path and os.path.exists(resume_file_path):
            os.unlink(resume_file_path)


@app.post("/generate-roadmap", response_model=RoadmapResponse, status_code=status.HTTP_201_CREATED)
async def generate_roadmap(
    request: GenerateRoadmapRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Generate a learning roadmap based on a JD analysis.
    Uses the workflow result to create personalized learning phases.
    Converts the new learning_roadmap structure (per-skill with stages) to legacy Phase structure (weekly phases).
    """
    jd_analysis_db = get_jd_analysis_db()
    
    # Check if JD analysis exists
    if request.jd_id not in jd_analysis_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="JD analysis not found"
        )
    
    jd_data = jd_analysis_db[request.jd_id]
    workflow_result = jd_data.get("workflow_result", {})
    
    # Get new learning_roadmap structure (per-skill with stages)
    learning_roadmap = workflow_result.get("learning_roadmap", [])
    project_recommendations = workflow_result.get("project_recommendations", [])
    ranked_skills = workflow_result.get("ranked_skills", [])
    
    # Convert new structure (per-skill roadmaps) to legacy Phase structure (weekly phases)
    phases = []
    
    if learning_roadmap:
        # Group stages by level across all skills
        beginner_stages = []
        intermediate_stages = []
        job_ready_stages = []
        
        for skill_roadmap in learning_roadmap:
            skill_name = skill_roadmap.get("skill", "")
            stages = skill_roadmap.get("stages", [])
            
            for stage in stages:
                level = stage.get("level", "").lower()
                resources = stage.get("resources", [])
                
                # Add skill name to resources description for context
                enhanced_resources = []
                for res in resources:
                    enhanced_resources.append({
                        **res,
                        "description": f"[{skill_name}] {res.get('description', '')}"
                    })
                
                if "beginner" in level:
                    beginner_stages.append({
                        "skill": skill_name,
                        "resources": enhanced_resources
                    })
                elif "intermediate" in level:
                    intermediate_stages.append({
                        "skill": skill_name,
                        "resources": enhanced_resources
                    })
                elif "job-ready" in level or "jobready" in level:
                    job_ready_stages.append({
                        "skill": skill_name,
                        "resources": enhanced_resources
                    })
        
        # Create Phase objects from grouped stages
        week = 1
        
        if beginner_stages:
            # Combine all beginner resources
            all_resources = []
            skills_list = []
            for stage in beginner_stages:
                skills_list.append(stage["skill"])
                all_resources.extend(stage["resources"])
            
            phases.append(Phase(
                week=week,
                skills=list(set(skills_list)),  # Remove duplicates
                resources=[
                    Resource(
                        type=res.get("type", "docs"),
                        title=res.get("title", ""),
                        url=res.get("url", ""),
                        description=res.get("description", "")
                    )
                    for res in all_resources[:10]  # Limit to 10 resources per phase
                ],
                projects=[
                    Project(
                        title=proj.get("title", ""),
                        description=proj.get("description", ""),
                        difficulty="beginner"
                    )
                    for proj in project_recommendations[:1]  # One project per phase
                ] if project_recommendations else [],
                description="Beginner phase: Learn fundamentals and basics"
            ))
            week += 1
        
        if intermediate_stages:
            all_resources = []
            skills_list = []
            for stage in intermediate_stages:
                skills_list.append(stage["skill"])
                all_resources.extend(stage["resources"])
            
            phases.append(Phase(
                week=week,
                skills=list(set(skills_list)),
                resources=[
                    Resource(
                        type=res.get("type", "docs"),
                        title=res.get("title", ""),
                        url=res.get("url", ""),
                        description=res.get("description", "")
                    )
                    for res in all_resources[:10]
                ],
                projects=[
                    Project(
                        title=proj.get("title", ""),
                        description=proj.get("description", ""),
                        difficulty="intermediate"
                    )
                    for proj in (project_recommendations[1:2] if len(project_recommendations) > 1 else [])
                ],
                description="Intermediate phase: Practical application and hands-on practice"
            ))
            week += 1
        
        if job_ready_stages:
            all_resources = []
            skills_list = []
            for stage in job_ready_stages:
                skills_list.append(stage["skill"])
                all_resources.extend(stage["resources"])
            
            phases.append(Phase(
                week=week,
                skills=list(set(skills_list)),
                resources=[
                    Resource(
                        type=res.get("type", "docs"),
                        title=res.get("title", ""),
                        url=res.get("url", ""),
                        description=res.get("description", "")
                    )
                    for res in all_resources[:10]
                ],
                projects=[
                    Project(
                        title=proj.get("title", ""),
                        description=proj.get("description", ""),
                        difficulty="advanced"
                    )
                    for proj in (project_recommendations[2:3] if len(project_recommendations) > 2 else [])
                ],
                description="Job-ready phase: Advanced concepts and production-level projects"
            ))
    
    # If no phases from workflow, create basic fallback
    if not phases:
        fallback_skills = [skill.get("skill", "Core Skills") for skill in ranked_skills[:3]] if ranked_skills else ["Core Skills"]
        phases = [
            Phase(
                week=1,
                skills=fallback_skills,
                resources=[Resource(type="docs", title="Documentation", url="", description="Start with official documentation")],
                projects=[Project(title="Practice Project", description="Learn basics through hands-on practice", difficulty="beginner")],
                description="Beginner phase: Start your learning journey"
            )
        ]
    
    # Generate roadmap ID and store
    roadmap_id = f"roadmap_{secrets.token_urlsafe(8)}"
    roadmaps_db = get_roadmaps_db()
    total_skills = len(ranked_skills) if ranked_skills else len(jd_data.get("skills", []))
    
    roadmaps_db[roadmap_id] = {
        "roadmap_id": roadmap_id,
        "jd_id": request.jd_id,
        "role": jd_data.get("role", "Unknown"),
        "phases": [phase.dict() for phase in phases],
        "total_skills": total_skills,
        "estimated_weeks": len(phases),
        "user_email": current_user["email"]
    }
    
    return RoadmapResponse(
        roadmap_id=roadmap_id,
        jd_id=request.jd_id,
        role=jd_data.get("role", "Unknown"),
        phases=phases,
        total_skills=total_skills,
        estimated_weeks=len(phases)
    )


@app.get("/user/roadmaps")
async def get_user_roadmaps(current_user: dict = Depends(get_current_user)):
    """Get all roadmaps for the current user."""
    roadmaps_db = get_roadmaps_db()
    user_roadmaps = [
        roadmap for roadmap in roadmaps_db.values()
        if roadmap.get("user_email") == current_user["email"]
    ]
    return {"roadmaps": user_roadmaps}


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy", "version": "1.0.0"}


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Job Upskilling API", "version": "1.0.0"}

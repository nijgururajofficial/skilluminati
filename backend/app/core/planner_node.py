"""Roadmap Maker Node - Skill Gap & Learning Path Generator."""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import json
import os
import logging
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

# Initialize Gemini LLM
try:
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=os.getenv("GOOGLE_API_KEY", "")
    )
except Exception as e:
    logger.warning(f"Failed to initialize Gemini LLM: {e}")
    llm = None


class RoadmapNodeInput(BaseModel):
    """Input schema for RoadmapMakerNode."""
    user_id: str
    resume_data: Dict[str, Any]
    jd_data: Dict[str, Any]
    research_context: Dict[str, Any]


class RoadmapMakerNode:
    """Roadmap Maker Node - Decision + synthesis layer that generates personalized learning roadmaps."""
    
    def __init__(self):
        """Initialize RoadmapMakerNode."""
        self.llm = llm
    
    def process(self, input_data: RoadmapNodeInput) -> Dict:
        """
        Generate personalized skill roadmap with gap analysis and learning paths.
        
        This node does NOT:
        - Research or scrape company data
        - Parse resume or JD directly
        
        It DOES:
        - Compute skill gaps
        - Rank importance
        - Generate staged learning paths
        - Suggest relevant projects
        - Initialize progress tracking
        
        Args:
            input_data: RoadmapNodeInput with user_id, resume_data, jd_data, and research_context
            
        Returns:
            Dict with skill_gap_analysis, ranked_skills, learning_roadmap, project_recommendations, 
            progress_template, and status
        """
        resume_data = input_data.resume_data
        jd_data = input_data.jd_data
        research_context = input_data.research_context
        
        # Extract data
        resume_skills = resume_data.get("skills", [])
        jd_required_skills = jd_data.get("required_skills", [])
        skill_insights = research_context.get("skill_insights", [])
        company_info = research_context.get("company_info", {})
        role_context = research_context.get("role_context", {})
        
        # Step 1: Skill Gap Analysis
        skill_gap_analysis = self._analyze_skill_gaps(resume_skills, jd_required_skills)
        
        # Step 2: Priority Scoring
        ranked_skills = self._rank_skills_by_priority(
            skill_gap_analysis, skill_insights, jd_data, research_context
        )
        
        # Step 3: Generate Learning Roadmap
        learning_roadmap = self._generate_learning_roadmap(
            ranked_skills, role_context, company_info, skill_insights
        )
        
        # Step 4: Generate Project Recommendations
        project_recommendations = self._generate_project_recommendations(
            ranked_skills, role_context, company_info, skill_insights
        )
        
        # Step 5: Initialize Progress Template
        progress_template = self._initialize_progress_template(ranked_skills)
        
        return {
            "user_id": input_data.user_id,
            "skill_gap_analysis": skill_gap_analysis,
            "ranked_skills": ranked_skills,
            "learning_roadmap": learning_roadmap,
            "project_recommendations": project_recommendations,
            "progress_template": progress_template,
            "status": "roadmap_generated"
        }
    
    def _analyze_skill_gaps(
        self, 
        resume_skills: List[str], 
        jd_required_skills: List[str]
    ) -> Dict[str, List[str]]:
        """
        Compare resume skills vs JD skills and categorize into missing/weak/matched.
        
        Returns:
            Dict with missing_skills, weak_skills, matched_skills
        """
        resume_skills_lower = {s.lower().strip() for s in resume_skills if s}
        jd_skills_lower = {s.lower().strip() for s in jd_required_skills if s}
        
        # Find matches (exact or partial)
        matched_skills = []
        missing_skills = []
        weak_skills = []
        
        for jd_skill in jd_required_skills:
            jd_skill_lower = jd_skill.lower().strip()
            
            # Check for exact match
            if jd_skill_lower in resume_skills_lower:
                matched_skills.append(jd_skill)
            else:
                # Check for partial match (e.g., "Python" matches "Python 3.9")
                is_partial_match = any(
                    jd_skill_lower in resume_skill or resume_skill in jd_skill_lower
                    for resume_skill in resume_skills_lower
                )
                
                if is_partial_match:
                    weak_skills.append(jd_skill)
                else:
                    missing_skills.append(jd_skill)
        
        return {
            "missing_skills": missing_skills,
            "weak_skills": weak_skills,
            "matched_skills": matched_skills
        }
    
    def _rank_skills_by_priority(
        self,
        skill_gap_analysis: Dict[str, List[str]],
        skill_insights: List[Dict],
        jd_data: Dict[str, Any],
        research_context: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Combine JD importance and company relevance to rank skills by urgency.
        
        Returns:
            List of ranked skills with priority_score
        """
        ranked_skills = []
        
        # Create skill insights map for quick lookup
        insights_map = {
            insight.get("skill_name", "").lower(): insight
            for insight in skill_insights
        }
        
        # Score missing skills (highest priority)
        for skill in skill_gap_analysis.get("missing_skills", []):
            skill_lower = skill.lower()
            insight = insights_map.get(skill_lower, {})
            
            # Calculate priority score (0.0 to 1.0)
            # Base score from being missing: 0.8
            priority_score = 0.8
            
            # Boost if mentioned in company tech stack
            company_tech_stack = research_context.get("company_info", {}).get("common_tech_stack", [])
            if any(skill_lower in tech.lower() for tech in company_tech_stack):
                priority_score += 0.1
            
            # Boost if has high company relevance
            company_relevance = insight.get("company_relevance", "")
            if company_relevance and len(company_relevance) > 20:
                priority_score += 0.05
            
            priority_score = min(priority_score, 1.0)
            
            ranked_skills.append({
                "skill": skill,
                "priority_score": round(priority_score, 2),
                "gap_type": "missing",
                "insight": insight
            })
        
        # Score weak skills (medium priority)
        for skill in skill_gap_analysis.get("weak_skills", []):
            skill_lower = skill.lower()
            insight = insights_map.get(skill_lower, {})
            
            priority_score = 0.5  # Base score for weak skills
            
            # Boost if mentioned in company tech stack
            company_tech_stack = research_context.get("company_info", {}).get("common_tech_stack", [])
            if any(skill_lower in tech.lower() for tech in company_tech_stack):
                priority_score += 0.2
            
            priority_score = min(priority_score, 0.9)
            
            ranked_skills.append({
                "skill": skill,
                "priority_score": round(priority_score, 2),
                "gap_type": "weak",
                "insight": insight
            })
        
        # Sort by priority score (descending)
        ranked_skills.sort(key=lambda x: x["priority_score"], reverse=True)
        
        return ranked_skills
    
    def _generate_learning_roadmap(
        self,
        ranked_skills: List[Dict],
        role_context: Dict[str, Any],
        company_info: Dict[str, Any],
        skill_insights: List[Dict]
    ) -> List[Dict[str, Any]]:
        """
        Generate multi-stage learning paths (Beginner → Intermediate → Job-Ready) for each skill.
        
        Returns:
            List of learning roadmaps per skill with stages
        """
        if not self.llm:
            raise RuntimeError("LLM not initialized. Cannot generate learning roadmap.")
        
        try:
            # Prepare context
            top_skills = ranked_skills[:10]  # Limit to top 10 skills
            skills_text = "\n".join([f"- {s['skill']}" for s in top_skills])
            
            role = role_context.get("role", "")
            company_name = company_info.get("name", "")
            
            prompt = ChatPromptTemplate.from_messages([
                ("system", """You are a career coach and skill strategist. Given a list of skills that need to be learned, generate a personalized, progressive learning roadmap for each skill.

For each skill, create 3 stages:
- Beginner: Foundations and basics
- Intermediate: Practical application
- Job-Ready: Advanced concepts and real-world projects

Each stage should include 2-3 learning resources (courses, tutorials, docs, YouTube links) with URLs when possible.

Return ONLY valid JSON with this structure:
{{
    "learning_roadmap": [
        {{
            "skill": "Airflow",
            "stages": [
                {{
                    "level": "Beginner",
                    "resources": [
                        {{"type": "docs", "title": "Airflow 101 Docs", "url": "https://airflow.apache.org/docs/", "description": "Official documentation"}},
                        {{"type": "tutorial", "title": "YouTube Setup Tutorial", "url": "https://youtube.com/...", "description": "Setup guide"}}
                    ]
                }},
                {{
                    "level": "Intermediate",
                    "resources": [
                        {{"type": "course", "title": "ETL Project with DAGs", "url": "", "description": "Hands-on project"}},
                        {{"type": "blog", "title": "Medium Blog: Airflow on GCP", "url": "", "description": "Best practices"}}
                    ]
                }},
                {{
                    "level": "Job-Ready",
                    "resources": [
                        {{"type": "project", "title": "Deploy Airflow DAG on Composer", "url": "", "description": "Production deployment"}},
                        {{"type": "project", "title": "Mini Project: Data Pipeline", "url": "", "description": "End-to-end pipeline"}}
                    ]
                }}
            ]
        }}
    ]
}}"""),
                ("human", """Role: {role}
Company: {company_name}
Skills to Learn:
{skills_text}

Generate a 3-stage learning roadmap for each skill.""")
            ])
            
            chain = prompt | self.llm
            response = chain.invoke({
                "role": role,
                "company_name": company_name or "the industry",
                "skills_text": skills_text
            })
            
            content = response.content
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            
            roadmap_result = json.loads(content)
            return roadmap_result.get("learning_roadmap", [])
            
        except Exception as e:
            logger.error(f"Failed to generate learning roadmap: {e}")
            raise
    
    def _generate_project_recommendations(
        self,
        ranked_skills: List[Dict],
        role_context: Dict[str, Any],
        company_info: Dict[str, Any],
        skill_insights: List[Dict]
    ) -> List[Dict[str, str]]:
        """
        Suggest mini-projects tied to skills and company use-cases.
        
        Returns:
            List of project recommendations with title and description
        """
        if not self.llm:
            raise RuntimeError("LLM not initialized. Cannot generate project recommendations.")
        
        try:
            top_skills = [s["skill"] for s in ranked_skills[:5]]
            skills_text = ", ".join(top_skills)
            
            role = role_context.get("role", "")
            company_name = company_info.get("name", "")
            real_world_examples = role_context.get("real_world_examples", [])
            
            examples_text = "\n".join(f"- {ex}" for ex in real_world_examples[:3]) if real_world_examples else "Not specified"
            
            prompt = ChatPromptTemplate.from_messages([
                ("system", """You are a project recommendation assistant. Given skills to learn, role context, and company examples, suggest 2-3 hands-on projects that would help the user practice these skills in a real-world context.

Each project should:
- Combine multiple skills
- Be relevant to the role and company context
- Be achievable but challenging
- Have clear deliverables

Return ONLY valid JSON with this structure:
{{
    "project_recommendations": [
        {{
            "title": "Data Pipeline Project",
            "description": "Build and automate an ETL pipeline using Airflow + BigQuery"
        }},
        {{
            "title": "SQL Analysis Portfolio",
            "description": "Analyze datasets using SQL and visualize insights"
        }}
    ]
}}"""),
                ("human", """Role: {role}
Company: {company_name}
Skills to Practice: {skills_text}
Real-World Examples:
{examples_text}

Suggest 2-3 relevant projects.""")
            ])
            
            chain = prompt | self.llm
            response = chain.invoke({
                "role": role,
                "company_name": company_name or "the industry",
                "skills_text": skills_text,
                "examples_text": examples_text
            })
            
            content = response.content
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            
            projects_result = json.loads(content)
            return projects_result.get("project_recommendations", [])
            
        except Exception as e:
            logger.error(f"Failed to generate project recommendations: {e}")
            raise
    
    def _initialize_progress_template(self, ranked_skills: List[Dict]) -> Dict[str, Any]:
        """
        Initialize tracking schema for user progress and Job Fit Score.
        
        Returns:
            Progress template with total_skills, completed_skills, job_fit_score, last_updated
        """
        total_skills = len(ranked_skills)
        
        return {
            "total_skills": total_skills,
            "completed_skills": 0,
            "job_fit_score": 0.0,
            "last_updated": None,
            "skill_progress": {
                skill["skill"]: {
                    "completed": False,
                    "stages_completed": [],
                    "last_updated": None
                }
                for skill in ranked_skills
            }
        }


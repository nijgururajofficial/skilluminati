"""Function schemas for structured output using Google GenAI SDK."""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


# ============================================================================
# Main Node Output Schemas
# ============================================================================

class ResumeData(BaseModel):
    """Resume data structure."""
    skills: List[str] = Field(default_factory=list, description="List of technical skills, tools, and technologies")
    experience: List[str] = Field(default_factory=list, description="List of work experience positions/roles")
    education: str = Field(default="", description="Education background (degree, institution)")
    projects: List[str] = Field(default_factory=list, description="List of projects mentioned")
    tools: List[str] = Field(default_factory=list, description="List of tools and technologies used")


class JDData(BaseModel):
    """Job description data structure."""
    company: str = Field(default="", description="Company name")
    role: str = Field(default="", description="Job role/title")
    required_skills: List[str] = Field(default_factory=list, description="List of required technical skills")
    tools: List[str] = Field(default_factory=list, description="List of tools and technologies mentioned")
    responsibilities: List[str] = Field(default_factory=list, description="List of key responsibilities")


class MainNodeOutput(BaseModel):
    """Output schema for MainNode."""
    user_id: str = Field(description="User identifier")
    resume_data: ResumeData = Field(description="Parsed resume data")
    jd_data: JDData = Field(description="Parsed job description data")
    status: str = Field(default="parsed", description="Processing status")


# ============================================================================
# Research Node Output Schemas
# ============================================================================

class CompanyInfo(BaseModel):
    """Company information structure."""
    name: str = Field(default="", description="Company name")
    industry: str = Field(default="", description="Industry sector")
    description: str = Field(default="", description="Brief company description")
    recent_projects: List[str] = Field(default_factory=list, description="List of recent projects")
    common_tech_stack: List[str] = Field(default_factory=list, description="List of common technologies used")


class RoleContext(BaseModel):
    """Role context structure."""
    role: str = Field(default="", description="Job role/title")
    responsibilities_summary: List[str] = Field(default_factory=list, description="Summary of key responsibilities")
    real_world_examples: List[str] = Field(default_factory=list, description="Real-world task examples")


class SkillInsight(BaseModel):
    """Skill insight structure."""
    skill_name: str = Field(description="The skill name")
    usage_context: str = Field(description="How this skill is typically used in this role/company context")
    related_tools: List[str] = Field(default_factory=list, description="List of related tools, frameworks, or technologies")
    company_relevance: str = Field(description="Why this skill matters for this company/role")


class ResearchNodeOutput(BaseModel):
    """Output schema for ResearchNode."""
    user_id: str = Field(description="User identifier")
    company_info: CompanyInfo = Field(description="Company research information")
    role_context: RoleContext = Field(description="Role context and real-world examples")
    skill_insights: List[SkillInsight] = Field(default_factory=list, description="Detailed insights for each skill")
    research_summary: str = Field(description="Synthesized research summary")
    status: str = Field(default="researched", description="Processing status")


# ============================================================================
# Roadmap Maker Node Output Schemas
# ============================================================================

class SkillGapAnalysis(BaseModel):
    """Skill gap analysis structure."""
    missing_skills: List[str] = Field(default_factory=list, description="Skills completely missing from resume")
    weak_skills: List[str] = Field(default_factory=list, description="Skills with partial match in resume")
    matched_skills: List[str] = Field(default_factory=list, description="Skills that match between resume and JD")


class RankedSkill(BaseModel):
    """Ranked skill structure."""
    skill: str = Field(description="Skill name")
    priority_score: float = Field(description="Priority score from 0.0 to 1.0")
    gap_type: str = Field(description="Type of gap: 'missing' or 'weak'")
    insight: Optional[Dict[str, Any]] = Field(default=None, description="Associated skill insight if available")


class LearningResource(BaseModel):
    """Learning resource structure."""
    type: str = Field(description="Resource type: 'docs', 'tutorial', 'course', 'blog', 'project'")
    title: str = Field(description="Resource title")
    url: str = Field(default="", description="Resource URL")
    description: str = Field(description="Brief description of the resource")


class LearningStage(BaseModel):
    """Learning stage structure."""
    level: str = Field(description="Stage level: 'Beginner', 'Intermediate', or 'Job-Ready'")
    resources: List[LearningResource] = Field(default_factory=list, description="Learning resources for this stage")


class SkillRoadmap(BaseModel):
    """Learning roadmap for a single skill."""
    skill: str = Field(description="Skill name")
    stages: List[LearningStage] = Field(default_factory=list, description="Learning stages for this skill")


class ProjectRecommendation(BaseModel):
    """Project recommendation structure."""
    title: str = Field(description="Project title")
    description: str = Field(description="Project description and deliverables")


class SkillProgress(BaseModel):
    """Individual skill progress tracking."""
    completed: bool = Field(default=False, description="Whether the skill is completed")
    stages_completed: List[str] = Field(default_factory=list, description="List of completed stage levels")
    last_updated: Optional[str] = Field(default=None, description="Last update timestamp")


class ProgressTemplate(BaseModel):
    """Progress tracking template."""
    total_skills: int = Field(description="Total number of skills to learn")
    completed_skills: int = Field(default=0, description="Number of completed skills")
    job_fit_score: float = Field(default=0.0, description="Job fit score from 0.0 to 1.0")
    last_updated: Optional[str] = Field(default=None, description="Last update timestamp")
    skill_progress: Dict[str, SkillProgress] = Field(default_factory=dict, description="Progress for each skill")


class RoadmapMakerNodeOutput(BaseModel):
    """Output schema for RoadmapMakerNode."""
    user_id: str = Field(description="User identifier")
    skill_gap_analysis: SkillGapAnalysis = Field(description="Analysis of skill gaps")
    ranked_skills: List[RankedSkill] = Field(default_factory=list, description="Skills ranked by priority")
    learning_roadmap: List[SkillRoadmap] = Field(default_factory=list, description="Learning roadmaps for each skill")
    project_recommendations: List[ProjectRecommendation] = Field(default_factory=list, description="Recommended projects")
    progress_template: ProgressTemplate = Field(description="Progress tracking template")
    status: str = Field(default="roadmap_generated", description="Processing status")


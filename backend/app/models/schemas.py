"""Pydantic models for API request/response schemas."""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, EmailStr, Field


# ============================================================================
# Authentication Schemas
# ============================================================================

class UserSignup(BaseModel):
    """User registration schema."""
    email: EmailStr
    password: str
    name: str


class UserLogin(BaseModel):
    """User login schema."""
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """JWT token response schema."""
    access_token: str
    token_type: str = "bearer"


# ============================================================================
# Job Description Analysis Schemas
# ============================================================================

class Skill(BaseModel):
    """Skill schema for API responses."""
    name: str
    priority: str = Field(description="Priority level: 'must-have', 'nice-to-have', or 'optional'")
    importance_score: Optional[int] = Field(None, description="Importance score from 1-10")
    why: Optional[str] = Field(None, description="Reason for importance")


class CompanyInsight(BaseModel):
    """Company insight schema."""
    title: str
    url: str
    content: str
    skills_used: List[str] = Field(default_factory=list)
    relevance: str = Field(default="medium", description="Relevance level: 'high', 'medium', 'low'")


class JDAnalysisResponse(BaseModel):
    """Response schema for JD analysis endpoint."""
    role: str
    skills: List[Skill]
    jd_id: str
    company_insights: Optional[List[CompanyInsight]] = None


# ============================================================================
# Roadmap Generation Schemas
# ============================================================================

class GenerateRoadmapRequest(BaseModel):
    """Request schema for roadmap generation."""
    jd_id: str


class Resource(BaseModel):
    """Learning resource schema."""
    type: str = Field(description="Resource type: 'course', 'tutorial', 'docs', 'blog', 'project', 'video'")
    title: str
    url: str = Field(default="", description="Resource URL")
    description: str


class Project(BaseModel):
    """Project recommendation schema."""
    title: str
    description: str
    difficulty: Optional[str] = Field(None, description="Difficulty level: 'beginner', 'intermediate', 'advanced'")


class LearningStage(BaseModel):
    """Learning stage schema (Beginner, Intermediate, Job-Ready)."""
    level: str = Field(description="Stage level: 'Beginner', 'Intermediate', or 'Job-Ready'")
    resources: List[Resource] = Field(default_factory=list)


class SkillRoadmap(BaseModel):
    """Learning roadmap for a single skill."""
    skill: str
    stages: List[LearningStage] = Field(default_factory=list)


class Phase(BaseModel):
    """Legacy phase schema for backward compatibility."""
    week: int
    skills: List[str]
    resources: List[Resource]
    projects: List[Project]
    description: str


class RoadmapResponse(BaseModel):
    """Response schema for roadmap generation endpoint."""
    roadmap_id: str
    jd_id: str
    role: str
    phases: List[Phase]
    total_skills: int
    estimated_weeks: int


# ============================================================================
# New Roadmap Schemas (Matching Node Outputs)
# ============================================================================

class SkillGapAnalysis(BaseModel):
    """Skill gap analysis schema."""
    missing_skills: List[str] = Field(default_factory=list, description="Skills completely missing from resume")
    weak_skills: List[str] = Field(default_factory=list, description="Skills with partial match")
    matched_skills: List[str] = Field(default_factory=list, description="Skills that match between resume and JD")


class RankedSkill(BaseModel):
    """Ranked skill schema."""
    skill: str
    priority_score: float = Field(description="Priority score from 0.0 to 1.0")
    gap_type: str = Field(description="Type of gap: 'missing' or 'weak'")
    insight: Optional[Dict[str, Any]] = Field(None, description="Associated skill insight")


class ProjectRecommendation(BaseModel):
    """Project recommendation schema."""
    title: str
    description: str


class SkillProgress(BaseModel):
    """Individual skill progress tracking."""
    completed: bool = Field(default=False)
    stages_completed: List[str] = Field(default_factory=list)
    last_updated: Optional[str] = None


class ProgressTemplate(BaseModel):
    """Progress tracking template."""
    total_skills: int
    completed_skills: int = Field(default=0)
    job_fit_score: float = Field(default=0.0, description="Job fit score from 0.0 to 1.0")
    last_updated: Optional[str] = None
    skill_progress: Dict[str, SkillProgress] = Field(default_factory=dict)


class CompleteRoadmapResponse(BaseModel):
    """Complete roadmap response matching RoadmapMakerNode output."""
    user_id: str
    skill_gap_analysis: SkillGapAnalysis
    ranked_skills: List[RankedSkill] = Field(default_factory=list)
    learning_roadmap: List[SkillRoadmap] = Field(default_factory=list)
    project_recommendations: List[ProjectRecommendation] = Field(default_factory=list)
    progress_template: ProgressTemplate
    status: str = "roadmap_generated"


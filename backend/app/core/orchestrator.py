"""
Orchestrator - Compiles LangGraph workflow and runs the complete pipeline.
Uses MainNode, ResearchNode, and RoadmapMakerNode to create a structured workflow.
"""

from typing import TypedDict, List, Dict, Annotated, Optional, Any
from langgraph.graph import StateGraph, END
import logging

from app.core.main_node import MainNode, MainNodeInput
from app.core.research_node import ResearchNode, ResearchNodeInput
from app.core.planner_node import RoadmapMakerNode, RoadmapNodeInput

logger = logging.getLogger(__name__)


class AgentState(TypedDict):
    """State for the LangGraph workflow."""
    user_id: Optional[str]
    resume_file_path: Optional[str]
    jd_text: Optional[str]
    # MainNode output
    resume_data: Optional[Dict[str, Any]]
    jd_data: Optional[Dict[str, Any]]
    # ResearchNode output
    company_info: Optional[Dict[str, Any]]
    role_context: Optional[Dict[str, Any]]
    skill_insights: Optional[List[Dict[str, Any]]]
    research_summary: Optional[str]
    research_context: Optional[Dict[str, Any]]  # Combined research output
    # RoadmapMakerNode output
    skill_gap_analysis: Optional[Dict[str, Any]]
    ranked_skills: Optional[List[Dict[str, Any]]]
    learning_roadmap: Optional[List[Dict[str, Any]]]
    project_recommendations: Optional[List[Dict[str, Any]]]
    progress_template: Optional[Dict[str, Any]]
    # Status
    status: Optional[str]
    current_node: str
    messages: Annotated[List, "messages"]


def main_node(state: AgentState) -> AgentState:
    """
    Main Node: Parses resume and JD into structured data.
    Uses MainNode class.
    """
    try:
        main_node_instance = MainNode()
        
        main_input = MainNodeInput(
            user_id=state.get("user_id", ""),
            resume_file_path=state.get("resume_file_path"),
            jd_text=state.get("jd_text", "")
        )
        
        result = main_node_instance.process(main_input)
        
        return {
            **state,
            "resume_data": result.get("resume_data", {}),
            "jd_data": result.get("jd_data", {}),
            "status": result.get("status", "parsed"),
            "current_node": "research"
        }
    except Exception as e:
        logger.error(f"MainNode failed: {e}")
        raise


def research_node(state: AgentState) -> AgentState:
    """
    Research Node: Researches company, role, and skill context.
    Uses ResearchNode class.
    """
    try:
        research_node_instance = ResearchNode()
        
        research_input = ResearchNodeInput(
            user_id=state.get("user_id", ""),
            resume_data=state.get("resume_data", {}),
            jd_data=state.get("jd_data", {})
        )
        
        result = research_node_instance.process(research_input)
        
        # Combine research outputs into research_context for next node
        research_context = {
            "company_info": result.get("company_info", {}),
            "role_context": result.get("role_context", {}),
            "skill_insights": result.get("skill_insights", []),
            "research_summary": result.get("research_summary", "")
        }
        
        return {
            **state,
            "company_info": result.get("company_info", {}),
            "role_context": result.get("role_context", {}),
            "skill_insights": result.get("skill_insights", []),
            "research_summary": result.get("research_summary", ""),
            "research_context": research_context,
            "status": result.get("status", "researched"),
            "current_node": "roadmap"
        }
    except Exception as e:
        logger.error(f"ResearchNode failed: {e}")
        raise


def roadmap_node(state: AgentState) -> AgentState:
    """
    Roadmap Maker Node: Generates personalized learning roadmap with skill gap analysis.
    Uses RoadmapMakerNode class.
    """
    try:
        roadmap_node_instance = RoadmapMakerNode()
        
        roadmap_input = RoadmapNodeInput(
            user_id=state.get("user_id", ""),
            resume_data=state.get("resume_data", {}),
            jd_data=state.get("jd_data", {}),
            research_context=state.get("research_context", {})
        )
        
        result = roadmap_node_instance.process(roadmap_input)
        
        return {
            **state,
            "skill_gap_analysis": result.get("skill_gap_analysis", {}),
            "ranked_skills": result.get("ranked_skills", []),
            "learning_roadmap": result.get("learning_roadmap", []),
            "project_recommendations": result.get("project_recommendations", []),
            "progress_template": result.get("progress_template", {}),
            "status": result.get("status", "roadmap_generated"),
            "current_node": "end"
        }
    except Exception as e:
        logger.error(f"RoadmapMakerNode failed: {e}")
        raise


def create_workflow() -> StateGraph:
    """
    Create and compile the LangGraph workflow.
    
    Flow:
    MainNode -> ResearchNode -> RoadmapMakerNode -> END
    
    Returns:
        Compiled LangGraph workflow
    """
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("main", main_node)
    workflow.add_node("research", research_node)
    workflow.add_node("roadmap", roadmap_node)
    
    # Set entry point
    workflow.set_entry_point("main")
    
    # Define flow: main -> research -> roadmap -> end
    workflow.add_edge("main", "research")
    workflow.add_edge("research", "roadmap")
    workflow.add_edge("roadmap", END)
    
    return workflow.compile()


# Global workflow instance
workflow = create_workflow()


def run_workflow(
    user_id: str,
    jd_text: str,
    resume_file_path: Optional[str] = None
) -> Dict:
    """
    Run the complete workflow with initial state.
    
    Args:
        user_id: User identifier
        jd_text: Job description text
        resume_file_path: Optional path to resume file (PDF)
        
    Returns:
        Dict with complete workflow results including:
        - resume_data: Parsed resume data
        - jd_data: Parsed job description data
        - company_info: Company research information
        - role_context: Role context and examples
        - skill_insights: Detailed skill insights
        - skill_gap_analysis: Gap analysis results
        - ranked_skills: Skills ranked by priority
        - learning_roadmap: Learning paths for each skill
        - project_recommendations: Recommended projects
        - progress_template: Progress tracking template
    """
    initial_state: AgentState = {
        "user_id": user_id,
        "resume_file_path": resume_file_path,
        "jd_text": jd_text,
        "resume_data": None,
        "jd_data": None,
        "company_info": None,
        "role_context": None,
        "skill_insights": None,
        "research_summary": None,
        "research_context": None,
        "skill_gap_analysis": None,
        "ranked_skills": None,
        "learning_roadmap": None,
        "project_recommendations": None,
        "progress_template": None,
        "status": None,
        "current_node": "main",
        "messages": []
    }
    
    try:
        result = workflow.invoke(initial_state)
        return result
    except Exception as e:
        logger.error(f"Workflow execution failed: {e}")
        raise


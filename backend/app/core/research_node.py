"""Research Node - Company & Skill Insight Engine."""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_tavily import TavilySearch
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
        google_api_key=os.getenv("GOOGLE_API_KEY", "AIzaSyDtCKotA23GXp397l_CxHDaTY5kktoPX_o")
    )
except Exception as e:
    logger.warning(f"Failed to initialize Gemini LLM: {e}")
    llm = None

# Initialize search tool
try:
    search_tool = TavilySearch(
        max_results=5,
        api_key=os.getenv("TAVILY_API_KEY", "")
    )
except Exception as e:
    logger.warning(f"Tavily search not available: {e}")
    search_tool = None


class ResearchNodeInput(BaseModel):
    """Input schema for ResearchNode."""
    user_id: str
    resume_data: Dict[str, Any]
    jd_data: Dict[str, Any]


class ResearchNode:
    """Research Node - Context expander that researches company, role, and skill insights."""
    
    def __init__(self):
        """Initialize ResearchNode."""
        self.llm = llm
        self.search_tool = search_tool
    
    def process(self, input_data: ResearchNodeInput) -> Dict:
        """
        Research company, role, and skill context to enrich understanding.
        
        This node does NOT:
        - Compare user's skills yet
        - Generate the roadmap
        
        It ONLY:
        - Researches external context (company, industry, role)
        - Enriches skill understanding
        - Stores knowledge base for the roadmap generator
        
        Args:
            input_data: ResearchNodeInput with user_id, resume_data, and jd_data
            
        Returns:
            Dict with company_info, role_context, skill_insights, research_summary, and status
        """
        jd_data = input_data.jd_data
        resume_data = input_data.resume_data
        
        company_name = jd_data.get("company", "")
        role = jd_data.get("role", "")
        required_skills = jd_data.get("required_skills", [])
        responsibilities = jd_data.get("responsibilities", [])
        
        # Research company context
        company_info = self._research_company_info(company_name, role)
        
        # Research role context
        role_context = self._research_role_context(role, responsibilities, company_name)
        
        # Research skill insights
        skill_insights = self._research_skill_insights(required_skills, company_name, role)
        
        # Synthesize research summary
        research_summary = self._synthesize_research(
            company_info, role_context, skill_insights
        )
        
        return {
            "user_id": input_data.user_id,
            "company_info": company_info,
            "role_context": role_context,
            "skill_insights": skill_insights,
            "research_summary": research_summary,
            "status": "researched"
        }
    
    def _research_company_info(self, company_name: str, role: str) -> Dict:
        """
        Research company overview, projects, and tech stack.
        
        Returns:
            Dict with name, industry, description, recent_projects, common_tech_stack
        """
        if not company_name:
            raise ValueError("Company name is required for research")
        
        # Use search tool to find company information
        search_results = []
        if self.search_tool:
            try:
                queries = [
                    f"{company_name} company overview technology stack",
                    f"{company_name} recent projects case studies",
                    f"{company_name} {role} tech stack"
                ]
                
                for query in queries[:2]:
                    try:
                        result = self.search_tool.invoke({"query": query})
                        # Handle different result formats from TavilySearch
                        # The new TavilySearch may return a string or different format
                        try:
                            # Check if result is a list and can be sliced
                            if isinstance(result, list):
                                # Safely get first 2 items
                                try:
                                    items_to_add = []
                                    for i, item in enumerate(result):
                                        if i >= 2:
                                            break
                                        items_to_add.append(item)
                                    search_results.extend(items_to_add)
                                except (TypeError, IndexError):
                                    # If we can't iterate, treat as single item
                                    search_results.append({"content": str(result)[:500], "title": query})
                            elif isinstance(result, str):
                                # If result is a string (search content), create a dict from it
                                search_results.append({"content": result[:500], "title": query})
                            elif isinstance(result, dict):
                                # If result is a single dict, add it
                                search_results.append(result)
                            else:
                                # Try to convert to string and use as content
                                content_str = str(result)
                                search_results.append({"content": content_str[:500], "title": query})
                        except Exception as parse_error:
                            # If anything fails, just use the string representation
                            logger.warning(f"Could not process search result for query '{query}': {parse_error}, type: {type(result)}")
                            try:
                                search_results.append({"content": str(result)[:500], "title": query})
                            except Exception:
                                pass  # Skip this result if we can't process it
                    except Exception as e:
                        logger.warning(f"Search query failed: {query}, {e}")
            except Exception as e:
                logger.warning(f"Company search failed: {e}")
        
        # Use LLM to extract structured company info
        if self.llm:
            try:
                search_content = "\n\n".join([
                    f"Title: {r.get('title', '')}\nContent: {r.get('content', '')[:500]}"
                    for r in search_results[:5]
                ]) if search_results else "No external research data available."
                
                prompt = ChatPromptTemplate.from_messages([
                    ("system", """You are a company research assistant. Given a company name and any available research data, extract structured information about the company.

Return ONLY valid JSON with this structure:
{{
    "name": "Company Name",
    "industry": "Industry sector",
    "description": "Brief company description",
    "recent_projects": ["Project 1", "Project 2"],
    "common_tech_stack": ["Technology 1", "Technology 2"]
}}"""),
                    ("human", """Company: {company_name}
Role: {role}
Research Data:
{search_content}

Extract company information from the above data.""")
                ])
                
                chain = prompt | self.llm
                response = chain.invoke({
                    "company_name": company_name,
                    "role": role,
                    "search_content": search_content
                })
                
                content = response.content
                if "```json" in content:
                    content = content.split("```json")[1].split("```")[0].strip()
                elif "```" in content:
                    content = content.split("```")[1].split("```")[0].strip()
                
                company_info = json.loads(content)
                return {
                    "name": company_info.get("name", company_name),
                    "industry": company_info.get("industry", ""),
                    "description": company_info.get("description", ""),
                    "recent_projects": company_info.get("recent_projects", []),
                    "common_tech_stack": company_info.get("common_tech_stack", [])
                }
            except Exception as e:
                logger.error(f"Failed to extract company info: {e}")
                raise
        
        raise RuntimeError("LLM not initialized. Cannot research company info.")
    
    def _research_role_context(self, role: str, responsibilities: List[str], company_name: str) -> Dict:
        """
        Research what the role actually involves in real-world contexts.
        
        Returns:
            Dict with role, responsibilities_summary, real_world_examples
        """
        if not role:
            raise ValueError("Role is required for research")
        
        # Use search tool to find role context
        search_results = []
        if self.search_tool:
            try:
                queries = [
                    f"{role} day to day responsibilities real world examples",
                    f"{role} {company_name} typical tasks" if company_name else f"{role} typical tasks"
                ]
                
                for query in queries:
                    try:
                        result = self.search_tool.invoke({"query": query})
                        # Handle different result formats from TavilySearch
                        # The new TavilySearch may return a string or different format
                        try:
                            # Check if result is a list and can be sliced
                            if isinstance(result, list):
                                # Safely get first 2 items
                                try:
                                    items_to_add = []
                                    for i, item in enumerate(result):
                                        if i >= 2:
                                            break
                                        items_to_add.append(item)
                                    search_results.extend(items_to_add)
                                except (TypeError, IndexError):
                                    # If we can't iterate, treat as single item
                                    search_results.append({"content": str(result)[:500], "title": query})
                            elif isinstance(result, str):
                                # If result is a string (search content), create a dict from it
                                search_results.append({"content": result[:500], "title": query})
                            elif isinstance(result, dict):
                                # If result is a single dict, add it
                                search_results.append(result)
                            else:
                                # Try to convert to string and use as content
                                content_str = str(result)
                                search_results.append({"content": content_str[:500], "title": query})
                        except Exception as parse_error:
                            # If anything fails, just use the string representation
                            logger.warning(f"Could not process search result for query '{query}': {parse_error}, type: {type(result)}")
                            try:
                                search_results.append({"content": str(result)[:500], "title": query})
                            except Exception:
                                pass  # Skip this result if we can't process it
                    except Exception as e:
                        logger.warning(f"Search query failed: {query}, {e}")
            except Exception as e:
                logger.warning(f"Role search failed: {e}")
        
        # Use LLM to extract role context
        if self.llm:
            try:
                search_content = "\n\n".join([
                    f"Title: {r.get('title', '')}\nContent: {r.get('content', '')[:500]}"
                    for r in search_results[:5]
                ]) if search_results else "No external research data available."
                
                responsibilities_text = "\n".join(f"- {r}" for r in responsibilities) if responsibilities else "Not specified"
                
                prompt = ChatPromptTemplate.from_messages([
                    ("system", """You are a role research assistant. Given a job role, responsibilities from JD, and research data, extract what this role actually involves in real-world contexts.

Return ONLY valid JSON with this structure:
{{
    "role": "Job Role",
    "responsibilities_summary": ["Responsibility 1", "Responsibility 2"],
    "real_world_examples": ["Example task 1", "Example task 2"]
}}"""),
                    ("human", """Role: {role}
JD Responsibilities:
{responsibilities_text}

Research Data:
{search_content}

Extract role context and real-world examples.""")
                ])
                
                chain = prompt | self.llm
                response = chain.invoke({
                    "role": role,
                    "responsibilities_text": responsibilities_text,
                    "search_content": search_content
                })
                
                content = response.content
                if "```json" in content:
                    content = content.split("```json")[1].split("```")[0].strip()
                elif "```" in content:
                    content = content.split("```")[1].split("```")[0].strip()
                
                role_context = json.loads(content)
                return {
                    "role": role_context.get("role", role),
                    "responsibilities_summary": role_context.get("responsibilities_summary", responsibilities),
                    "real_world_examples": role_context.get("real_world_examples", [])
                }
            except Exception as e:
                logger.error(f"Failed to extract role context: {e}")
                raise
        
        raise RuntimeError("LLM not initialized. Cannot research role context.")
    
    def _research_skill_insights(self, skills: List[str], company_name: str, role: str) -> List[Dict]:
        """
        Deep dive into each skill to understand usage context and related tools.
        
        Returns:
            List of skill insight dicts with skill_name, usage_context, related_tools, company_relevance
        """
        if not skills:
            return []
        
        # Research skills in batches to avoid too many API calls
        skills_batch = skills[:10]  # Limit to top 10 skills
        
        if not self.llm:
            raise RuntimeError("LLM not initialized. Cannot research skill insights.")
        
        skills_text = "\n".join(f"- {skill}" for skill in skills_batch)
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a skill research assistant. Given a list of skills, company name, and role, research how each skill is used in real-world contexts.

For each skill, provide:
- skill_name: the skill name
- usage_context: how this skill is typically used in this role/company context
- related_tools: list of related tools, frameworks, or technologies
- company_relevance: why this skill matters for this company/role

Return ONLY valid JSON with this structure:
{{
    "skill_insights": [
        {{
            "skill_name": "TensorFlow",
            "usage_context": "Used for distributed training and model export in production.",
            "related_tools": ["TFX", "Keras", "TensorBoard"],
            "company_relevance": "Part of their experimentation stack."
        }}
    ]
}}"""),
            ("human", """Company: {company_name}
Role: {role}
Skills:
{skills_text}

Research each skill's usage context, related tools, and company relevance.""")
        ])
        
        chain = prompt | self.llm
        response = chain.invoke({
            "company_name": company_name or "the industry",
            "role": role or "this role",
            "skills_text": skills_text
        })
        
        content = response.content
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
        
        insights_result = json.loads(content)
        return insights_result.get("skill_insights", [])
    
    def _synthesize_research(self, company_info: Dict, role_context: Dict, skill_insights: List[Dict]) -> str:
        """
        Synthesize all research into a comprehensive summary.
        
        Returns:
            String summary of the research findings
        """
        if self.llm:
            try:
                company_summary = json.dumps(company_info, indent=2)
                role_summary = json.dumps(role_context, indent=2)
                skills_summary = json.dumps(skill_insights[:5], indent=2)  # Top 5 skills
                
                prompt = ChatPromptTemplate.from_messages([
                    ("system", """You are a research synthesis assistant. Combine company information, role context, and skill insights into a concise, actionable summary.

The summary should highlight:
- Company focus and tech stack
- Role requirements and real-world context
- Key skills and their importance

Return a 2-3 sentence summary without JSON formatting."""),
                    ("human", """Company Info:
{company_summary}

Role Context:
{role_summary}

Skill Insights:
{skills_summary}

Create a research summary.""")
                ])
                
                chain = prompt | self.llm
                response = chain.invoke({
                    "company_summary": company_summary,
                    "role_summary": role_summary,
                    "skills_summary": skills_summary
                })
                
                return response.content.strip()
            except Exception as e:
                logger.error(f"Failed to synthesize research: {e}")
                raise
        
        raise RuntimeError("LLM not initialized. Cannot synthesize research summary.")


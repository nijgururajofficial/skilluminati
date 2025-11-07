"""Main Node - Context Builder for Resume & JD Parsing."""

from typing import Optional, List, Dict
from pydantic import BaseModel
import json
import os
import logging
import re
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

logger = logging.getLogger(__name__)
from dotenv import load_dotenv

load_dotenv()

# Initialize Gemini LLM
try:
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=os.getenv("GOOGLE_API_KEY", "")
    )
except Exception as e:
    logger.warning(f"Failed to initialize Gemini LLM: {e}")
    llm = None


class MainNodeInput(BaseModel):
    """Input schema for MainNode."""
    user_id: str
    resume_file_path: Optional[str] = None  # Path to uploaded resume
    jd_text: str  # Raw JD text


class MainNode:
    """Main Node - Context Builder that parses resume and JD into structured data."""
    
    def __init__(self):
        """Initialize MainNode."""
        self.llm = llm
    
    def process(self, input_data: MainNodeInput) -> Dict:
        """
        Parse resume and JD into structured context data.
        
        This node does NOT:
        - Compare skills
        - Recommend learning paths
        - Generate roadmaps
        
        It ONLY:
        - Extracts structured context
        - Cleans raw input
        - Seeds graph state for downstream intelligence
        
        Args:
            input_data: MainNodeInput with JD text, user_id, and optional resume file path
            
        Returns:
            Dict with parsed resume_data, jd_data, and status
        """
        # Parse resume if provided
        logger.info("MainNode processing start | user_id=%s", input_data.user_id)
        resume_data = {}
        if input_data.resume_file_path:
            resume_data = self._parse_resume(input_data.resume_file_path)
        
        # Parse job description
        jd_data = self._parse_job_description(input_data.jd_text)
        
        logger.info(
            "MainNode processing complete | user_id=%s | resume_sections=%d | jd_sections=%d",
            input_data.user_id,
            len(resume_data.keys()),
            len(jd_data.keys()),
        )
        
        return {
            "user_id": input_data.user_id,
            "resume_data": resume_data,
            "jd_data": jd_data,
            "status": "parsed"
        }
    
    def _parse_resume(self, resume_file_path: str) -> Dict:
        """
        Parse resume file into structured data.
        
        Returns:
            Dict with skills, experience, education, projects, and tools
        """
        resume_content = ""
        
        # Load PDF if file path provided
        loader = PyPDFLoader(resume_file_path)
        documents = loader.load()
        logger.debug("MainNode resume PDF loaded | pages=%d", len(documents))
        resume_content = "\n".join([doc.page_content for doc in documents])
        
        if not resume_content:
            raise ValueError("Resume file is empty or could not be parsed")
        
        # Extract structured data using Gemini
        if not self.llm:
            raise RuntimeError("LLM not initialized. Cannot parse resume.")
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a parsing assistant that converts resumes into structured JSON objects without evaluation or recommendations.

Extract the following information from the resume:
- skills: List of technical skills, tools, and technologies
- experience: List of work experience positions/roles
- education: Education background (degree, institution)
- projects: List of projects mentioned
- tools: List of tools and technologies used

Return ONLY valid JSON with this structure:
{{
    "skills": ["Python", "TensorFlow", "SQL"],
    "experience": ["AI Intern at S3CURA", "Data Engineer Intern at ABC Corp"],
    "education": "MS in Computer Science",
    "projects": ["AI Interview Bot", "Image Caption Generator"],
    "tools": ["AWS", "Docker", "Keras"]
}}"""),
            ("human", "Resume Content:\n{resume_content}")
        ])
        
        chain = prompt | self.llm
        response = chain.invoke({"resume_content": resume_content})

        content = response.content
        resume_parsed = self._extract_json(content, context="resume")
        logger.info(
            "MainNode resume parsing success | skills=%d | experience=%d",
            len(resume_parsed.get("skills", [])),
            len(resume_parsed.get("experience", [])),
        )
        return {
            "skills": resume_parsed.get("skills", []),
            "experience": resume_parsed.get("experience", []),
            "education": resume_parsed.get("education", ""),
            "projects": resume_parsed.get("projects", []),
            "tools": resume_parsed.get("tools", [])
        }
    
    def _parse_job_description(self, jd_text: str) -> Dict:
        """
        Parse job description into structured data.
        
        Returns:
            Dict with company, role, required_skills, tools, and responsibilities
        """
        if not jd_text:
            raise ValueError("Job description text is empty")
        
        # Extract structured data using Gemini
        if not self.llm:
            raise RuntimeError("LLM not initialized. Cannot parse job description.")
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a parsing assistant that converts job descriptions into structured JSON objects without evaluation or recommendations.

Extract the following information from the job description:
- company: Company name
- role: Job role/title
- required_skills: List of required technical skills
- tools: List of tools and technologies mentioned
- responsibilities: List of key responsibilities

Return ONLY valid JSON with this structure:
{{
    "company": "OpenAI",
    "role": "Machine Learning Engineer",
    "required_skills": ["Python", "TensorFlow", "MLOps", "GCP"],
    "tools": ["Vertex AI", "Docker"],
    "responsibilities": [
        "Build and deploy scalable ML systems",
        "Work with data pipelines"
    ]
}}"""),
            ("human", "Job Description:\n{jd_text}")
        ])
        
        chain = prompt | self.llm
        response = chain.invoke({"jd_text": jd_text})

        content = response.content
        jd_parsed = self._extract_json(content, context="job description")
        logger.info(
            "MainNode JD parsing success | company=%s | role=%s | skills=%d",
            jd_parsed.get("company", ""),
            jd_parsed.get("role", ""),
            len(jd_parsed.get("required_skills", [])),
        )
        return {
            "company": jd_parsed.get("company", ""),
            "role": jd_parsed.get("role", ""),
            "required_skills": jd_parsed.get("required_skills", []),
            "tools": jd_parsed.get("tools", []),
            "responsibilities": jd_parsed.get("responsibilities", [])
        }

    def _extract_json(self, raw_content: str, context: str) -> Dict:
        """Extract and sanitize JSON content from model responses."""
        if not raw_content:
            raise ValueError(f"Empty response content while parsing {context}")

        content = raw_content.strip()
        if "```json" in content:
            content = content.split("```json", 1)[1]
            content = content.split("```", 1)[0]
        elif "```" in content:
            content = content.split("```", 1)[1]
            content = content.split("```", 1)[0]

        if "{" in content and "}" in content:
            start = content.index("{")
            end = content.rindex("}") + 1
            content = content[start:end]

        try:
            return json.loads(content)
        except json.JSONDecodeError as exc:
            logger.debug(
                "MainNode %s JSON parsing needs sanitization | error=%s",
                context,
                exc,
            )

        sanitized = self._sanitize_json_string(content)
        try:
            return json.loads(sanitized)
        except json.JSONDecodeError as exc:
            logger.error(
                "MainNode %s JSON parsing failed | error=%s | content=%s",
                context,
                exc,
                sanitized,
            )
            raise

    @staticmethod
    def _sanitize_json_string(content: str) -> str:
        """Attempt to coerce near-JSON content into valid JSON."""
        if not content:
            return "{}"

        lines = content.strip().replace("\r", "").splitlines()
        fixed_lines = []
        for line in lines:
            stripped = line.strip()

            # Auto-quote bare trailing string values such as   fangraph"
            if stripped.endswith('"') and not stripped.startswith('"'):
                has_comma = stripped.endswith('",')
                text = stripped.rstrip(',').rstrip('"').strip()
                if text:
                    indent = line[: len(line) - len(line.lstrip())]
                    stripped = f'"{text}"'
                    if has_comma:
                        stripped += ','
                    line = indent + stripped

            fixed_lines.append(line)

        sanitized = "\n".join(fixed_lines)

        # Remove trailing commas before closing braces/brackets
        sanitized = re.sub(r",(\s*[}\]])", r"\1", sanitized)

        # Replace single quotes around keys/values with double quotes when safe
        sanitized = re.sub(r"'([^']+)'\s*:", lambda m: f'"{m.group(1)}":', sanitized)
        sanitized = re.sub(r":\s*'([^']*)'", lambda m: f': "{m.group(1)}"', sanitized)

        # Ensure adjacent quoted strings are comma separated inside arrays
        sanitized = re.sub(r'"\s+(?=")', '", ', sanitized)

        return sanitized


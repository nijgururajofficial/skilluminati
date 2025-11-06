# Job Upskilling Platform - Backend API

A FastAPI backend that helps job seekers upskill by analyzing job descriptions, researching companies, and generating personalized learning roadmaps using LangGraph and Google Gemini.

## Features

- **Resume & JD Parsing**: Extracts skills, experience, and requirements from resumes and job descriptions
- **Company Research**: Researches company tech stack and real-world projects using Tavily Search
- **Skill Gap Analysis**: Identifies missing skills and prioritizes learning
- **Personalized Roadmaps**: Generates 3-stage learning paths with resources and project recommendations
- **JWT Authentication**: Secure user authentication and authorization

## Architecture

The system uses a **LangGraph workflow** with three main nodes:

1. **MainNode** (Context Builder): Parses resume and job description into structured data
2. **ResearchNode** (Insight Engine): Researches company, role, and skill context
3. **RoadmapMakerNode** (Roadmap Generator): Analyzes skill gaps and generates learning roadmaps

## Setup

### Prerequisites

- Python 3.8 or higher
- Google API Key (for Gemini LLM)
- Tavily API Key (for company research)

### Installation Steps

1. **Navigate to the backend directory:**
   ```bash
   cd backend
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set environment variables:**
   
   Create a `.env` file in the `backend` directory or set these environment variables:
   ```bash
   GOOGLE_API_KEY=your_google_api_key_here
   TAVILY_API_KEY=your_tavily_api_key_here
   SECRET_KEY=your_secret_key_for_jwt
   ```
   
   **Note:** 
   - Get your Google API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Get your Tavily API key from [Tavily](https://tavily.com)
   - Generate a secret key for JWT (any random string)

## Running the Application

1. **Start the FastAPI server:**
   ```bash
   uvicorn main:app --reload
   ```

2. **Access the API:**
   - API Base URL: `http://localhost:8000`
   - Swagger UI Documentation: `http://localhost:8000/docs`
   - ReDoc Documentation: `http://localhost:8000/redoc`

3. **To stop the server:**
   Press `Ctrl+C` in the terminal

## API Endpoints

### Authentication
- `POST /signup` - Register a new user
- `POST /login` - Login and get JWT token

### Job Analysis & Roadmap
- `POST /analyze-jd` - Analyze job description (requires JWT)
- `POST /generate-roadmap` - Generate learning roadmap (requires JWT)
- `GET /user/roadmaps` - Get all user roadmaps (requires JWT)

### Health Check
- `GET /` - API status
- `GET /health` - Health check endpoint

## Using Swagger UI

1. Navigate to `http://localhost:8000/docs`
2. Click the **Authorize** button (lock icon)
3. Enter your JWT token in the format: `Bearer your_jwt_token_here`
4. Click **Authorize** to authenticate
5. You can now test all protected endpoints

## Project Structure

```
backend/
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Python dependencies
├── README.md              # This file
│
└── app/
    ├── auth/              # Authentication (JWT, routes)
    ├── core/              # LangGraph nodes and orchestrator
    │   ├── main_node.py           # Context Builder
    │   ├── research_node.py       # Insight Engine
    │   ├── planner_node.py        # Roadmap Maker
    │   ├── orchestrator.py        # Workflow orchestration
    │   └── function_schemas.py    # Output schemas
    ├── models/            # Pydantic schemas
    └── db/                # In-memory data storage
```

## Notes

- **In-Memory Storage**: Data is stored in memory and will be lost on server restart
- **JWT Tokens**: Expire after 1 hour
- **Resume Format**: Currently supports PDF files
- **Production**: Replace in-memory storage with a database (PostgreSQL, MongoDB, etc.) for production use

## Troubleshooting

- **Import errors**: Make sure you've activated the virtual environment and installed all dependencies
- **API key errors**: Verify your environment variables are set correctly
- **Port already in use**: Change the port with `uvicorn main:app --reload --port 8001`

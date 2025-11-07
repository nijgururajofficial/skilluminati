# Skilluminati

**Decode the job. Focus your prep.**

Skilluminati is an intelligent job analysis platform that helps job seekers decode job descriptions, identify critical skills, and generate personalized learning roadmaps. Built with FastAPI (backend) and React + TypeScript (frontend), powered by Google Gemini AI and LangGraph.

## Features

- 📋 **Job Description Analysis**: Extract core skills and company context from any job posting
- 📄 **Resume Parsing**: Upload your resume to compare against job requirements
- 🎯 **Skill Gap Analysis**: Identify missing skills and prioritize learning
- 🗺️ **Personalized Roadmaps**: Generate focused 3-stage learning paths (Beginner → Intermediate → Job-Ready)
- 🏢 **Company Research**: Get insights into company tech stack and real-world projects

## Prerequisites

- **Python 3.8+** (for backend)
- **Node.js 18+** and **npm** (for frontend)
- **Google API Key** (for Gemini LLM) - Get it from [Google AI Studio](https://makersuite.google.com/app/apikey)
- **Tavily API Key** (optional, for company research) - Get it from [Tavily](https://tavily.com)

## Quick Start

### 1. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file in backend directory
# Add your API keys:
GOOGLE_API_KEY=your_google_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here  # Optional
SECRET_KEY=your_secret_key_for_jwt  # Any random string

# Run the backend server
uvicorn main:app --reload
```

The backend will be available at `http://localhost:8000`

### 2. Frontend Setup

```bash
# Navigate to frontend directory
cd skilluminati_frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```

The frontend will be available at `http://localhost:5173`

## Using the Job Analyzer

1. **Start both servers** (backend and frontend) as described above

2. **Navigate to the Job Analyzer page:**
   ```
   http://localhost:5173/job-analyzer
   ```

3. **Paste the Job Description:**
   - Copy the full job description from any job posting
   - Paste it into the "Job description" text field

4. **Upload Your Resume (Optional):**
   - Click the resume upload area
   - Select your resume PDF file
   - This helps Skilluminati compare your skills against the job requirements

5. **Click "Analyze":**
   - Skilluminati will extract 5-8 core skills
   - Show company context and tech stack insights
   - Display priority scores for each skill

6. **View Your Roadmap:**
   - Click "View roadmap" to see personalized learning paths
   - Each skill includes 3 stages: Beginner, Intermediate, and Job-Ready
   - Resources are concise and focused on tutorials and official docs

## Project Structure

```
Skilluminati/
├── backend/                    # FastAPI backend
│   ├── app/
│   │   ├── auth/              # JWT authentication
│   │   ├── core/              # LangGraph workflow nodes
│   │   │   ├── main_node.py           # Context Builder (parses resume/JD)
│   │   │   ├── research_node.py       # Company & skill research
│   │   │   ├── planner_node.py        # Roadmap generator
│   │   │   └── orchestrator.py        # Workflow orchestration
│   │   ├── models/            # Pydantic schemas
│   │   └── db/                # In-memory storage
│   ├── main.py                # FastAPI entry point
│   ├── requirements.txt       # Python dependencies
│   └── README.md              # Backend documentation
│
├── skilluminati_frontend/      # React + TypeScript frontend
│   ├── src/
│   │   ├── features/
│   │   │   ├── job-analyzer/  # Job analysis feature
│   │   │   ├── learning-path/ # Roadmap visualization
│   │   │   └── ...
│   │   ├── config/            # API configuration
│   │   └── ...
│   ├── package.json           # Node dependencies
│   └── README.md              # Frontend documentation
│
└── README.md                  # This file
```

## API Endpoints

### Job Analysis
- `POST /analyze-jd` - Analyze job description and resume
- `POST /generate-roadmap` - Generate learning roadmap

### Authentication (Optional)
- `POST /signup` - Register new user
- `POST /login` - Login and get JWT token

### Documentation
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Architecture

Skilluminati uses a **LangGraph workflow** with three main nodes:

1. **MainNode** (Context Builder): Parses resume and job description into structured data
2. **ResearchNode** (Insight Engine): Researches company, role, and skill context using Tavily Search
3. **RoadmapMakerNode** (Roadmap Generator): Analyzes skill gaps and generates focused learning roadmaps

## Environment Variables

### Backend (.env file in `backend/` directory)

```bash
GOOGLE_API_KEY=your_google_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here  # Optional
SECRET_KEY=your_secret_key_for_jwt
```

### Frontend

The frontend is configured to connect to `http://localhost:8000` by default. Update `skilluminati_frontend/src/config/api.ts` if your backend runs on a different port.

## Development

### Backend Development

```bash
cd backend
uvicorn main:app --reload --port 8000
```

### Frontend Development

```bash
cd skilluminati_frontend
npm run dev
```

### Building for Production

**Frontend:**
```bash
cd skilluminati_frontend
npm run build
```

**Backend:**
The backend is ready for production deployment with any ASGI server (e.g., Gunicorn, Uvicorn).

## Troubleshooting

- **Backend won't start**: Make sure your virtual environment is activated and all dependencies are installed
- **Frontend can't connect to backend**: Verify the backend is running on port 8000 and check `src/config/api.ts`
- **API key errors**: Ensure your `.env` file in the `backend/` directory has valid API keys
- **Port conflicts**: Change ports using `--port` flag for uvicorn or update Vite config for frontend

## Notes

- **In-Memory Storage**: Data is stored in memory and will be lost on server restart
- **Resume Format**: Currently supports PDF files
- **Production**: Replace in-memory storage with a database (PostgreSQL, MongoDB, etc.) for production use

## License

This project is private and proprietary.


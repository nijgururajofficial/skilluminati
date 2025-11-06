# API Documentation

## Authentication Endpoints

### **Route:**
`POST /signup`

### **Description:**
Registers a new user account and returns a JWT access token for authentication. The user must provide email, password, and name.

### **Payload:**
JSON Body
```json
{
  "email": "user@example.com",
  "password": "securepassword123",
  "name": "John Doe"
}
```

### **Output:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### **Error Responses:**
- `400 Bad Request`: Email already registered
- `500 Internal Server Error`: Server error during registration

---

### **Route:**
`POST /login`

### **Description:**
Authenticates an existing user and returns a JWT access token. The user must provide valid email and password credentials.

### **Payload:**
JSON Body
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

### **Output:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### **Error Responses:**
- `401 Unauthorized`: Incorrect email or password
- `500 Internal Server Error`: Server error during authentication

---

## Job Description Analysis Endpoints

### **Route:**
`POST /analyze-jd`

### **Description:**
Analyzes a job description (JD) and compares it with the user's resume to extract key role details, must-have skills, their importance, and company insights. Returns structured data for roadmap and research nodes. Requires authentication.

### **Authentication:**
Bearer Token (JWT) - Required

### **Payload:**
Multipart Form Data
```json
{
  "jd_text": "Full job description text",
  "resume": "Resume file (PDF)" // Optional
}
```

### **Output:**
```json
{
  "role": "Python Engineer",
  "skills": [
    {
      "name": "Python programming",
      "priority": "must-have",
      "importance_score": 8,
      "why": "Core requirement for the role"
    }
  ],
  "jd_id": "jd_xSFy8rcCgMQ",
  "company_insights": [
    {
      "title": "BlackRock Technology Stack",
      "url": "",
      "content": "Company uses Python, AWS, and Docker in their tech stack",
      "skills_used": ["Python", "AWS", "Docker"],
      "relevance": "high"
    }
  ]
}
```

### **Error Responses:**
- `400 Bad Request`: Invalid file format (only PDF supported)
- `401 Unauthorized`: Missing or invalid authentication token
- `500 Internal Server Error`: Error during JD analysis

---

## Roadmap Generation Endpoints

### **Route:**
`POST /generate-roadmap`

### **Description:**
Generates a personalized learning roadmap based on a previously analyzed job description. Creates weekly learning phases with resources, projects, and skill progression from Beginner → Intermediate → Job-Ready. Requires authentication.

### **Authentication:**
Bearer Token (JWT) - Required

### **Payload:**
JSON Body
```json
{
  "jd_id": "jd_xSFy8rcCgMQ"
}
```

### **Output:**
```json
{
  "roadmap_id": "roadmap_abc123xyz",
  "jd_id": "jd_xSFy8rcCgMQ",
  "role": "Python Engineer",
  "phases": [
    {
      "week": 1,
      "skills": ["Python", "SQL", "Docker"],
      "resources": [
        {
          "type": "docs",
          "title": "Python Official Documentation",
          "url": "https://docs.python.org/",
          "description": "Official Python documentation"
        },
        {
          "type": "course",
          "title": "Python for Data Science",
          "url": "https://...",
          "description": "Comprehensive Python course"
        }
      ],
      "projects": [
        {
          "title": "Data Pipeline Project",
          "description": "Build an ETL pipeline using Python",
          "difficulty": "beginner"
        }
      ],
      "description": "Beginner phase: Learn fundamentals and basics"
    },
    {
      "week": 2,
      "skills": ["AWS", "Kubernetes"],
      "resources": [...],
      "projects": [...],
      "description": "Intermediate phase: Practical application and hands-on practice"
    },
    {
      "week": 3,
      "skills": ["MLOps", "Production Deployment"],
      "resources": [...],
      "projects": [...],
      "description": "Job-ready phase: Advanced concepts and production-level projects"
    }
  ],
  "total_skills": 8,
  "estimated_weeks": 3
}
```

### **Error Responses:**
- `401 Unauthorized`: Missing or invalid authentication token
- `404 Not Found`: JD analysis not found for the provided jd_id
- `500 Internal Server Error`: Error during roadmap generation

---

## User Data Endpoints

### **Route:**
`GET /user/roadmaps`

### **Description:**
Retrieves all learning roadmaps created by the authenticated user. Returns a list of roadmaps with their IDs, associated JD IDs, roles, phases, and progress information. Requires authentication.

### **Authentication:**
Bearer Token (JWT) - Required

### **Payload:**
None (uses JWT token from Authorization header)

### **Output:**
```json
{
  "roadmaps": [
    {
      "roadmap_id": "roadmap_abc123xyz",
      "jd_id": "jd_xSFy8rcCgMQ",
      "role": "Python Engineer",
      "phases": [...],
      "total_skills": 8,
      "estimated_weeks": 3,
      "user_email": "user@example.com"
    },
    {
      "roadmap_id": "roadmap_def456uvw",
      "jd_id": "jd_yTGz9sDhNRP",
      "role": "Data Engineer",
      "phases": [...],
      "total_skills": 6,
      "estimated_weeks": 2,
      "user_email": "user@example.com"
    }
  ]
}
```

### **Error Responses:**
- `401 Unauthorized`: Missing or invalid authentication token
- `500 Internal Server Error`: Error retrieving roadmaps

---

## Health & Status Endpoints

### **Route:**
`GET /health`

### **Description:**
Health check endpoint to verify API server status and version. No authentication required.

### **Payload:**
None

### **Output:**
```json
{
  "status": "healthy",
  "version": "1.0.0"
}
```

---

### **Route:**
`GET /`

### **Description:**
Root endpoint that returns API information and version. No authentication required.

### **Payload:**
None

### **Output:**
```json
{
  "message": "Job Upskilling API",
  "version": "1.0.0"
}
```

---

## Authentication Flow

1. **Sign Up or Login** to get a JWT token:
   - `POST /signup` or `POST /login`
   - Copy the `access_token` from the response

2. **Authorize in Swagger UI**:
   - Click the **"Authorize"** button (lock icon) at the top right
   - Enter: `Bearer <your_access_token>`
   - Click **"Authorize"** then **"Close"**

3. **Use Protected Endpoints**:
   - All endpoints except `/signup`, `/login`, `/health`, and `/` require authentication
   - The token will be automatically included in requests

## Error Response Format

All error responses follow this format:
```json
{
  "detail": "Error message describing what went wrong"
}
```

## Status Codes

- `200 OK`: Request successful
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Authentication required or invalid token
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error


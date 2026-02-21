# Design Document: BRD Generation Backend

## Overview

The BRD Generation Backend is a Python FastAPI service that accepts project context from multiple sources and generates structured Business Requirements Documents using OpenAI's API. The system follows a simple request-response pattern with a single endpoint that orchestrates input validation, prompt construction, OpenAI API interaction, and response formatting.

The architecture emphasizes separation of concerns with distinct layers for API handling, business logic, and external service integration. The design prioritizes simplicity for this prototype while maintaining extensibility for future enhancements.

## Architecture

The system follows a layered architecture:

```
┌─────────────────────────────────────┐
│         FastAPI Layer               │
│  (Routing, Validation, Responses)   │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│       Service Layer                 │
│  (Business Logic, Orchestration)    │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│      OpenAI Client Layer            │
│  (Prompt Construction, API Calls)   │
└─────────────────────────────────────┘
```

**Layer Responsibilities:**

- **FastAPI Layer**: Handles HTTP requests, input validation using Pydantic models, and response formatting
- **Service Layer**: Orchestrates the BRD generation workflow, coordinates between components
- **OpenAI Client Layer**: Manages OpenAI API communication, prompt engineering, and response parsing

## Components and Interfaces

### 1. API Models (Pydantic)

**BRDRequest**
```python
class BRDRequest(BaseModel):
    projectName: str
    emailText: str
    slackText: str
    meetingText: str
```

**BRDResponse**
```python
class BRDResponse(BaseModel):
    requirements: List[Requirement]
    acceptanceCriteria: List[AcceptanceCriterion]
    designSketch: DesignSketch

class Requirement(BaseModel):
    id: str
    description: str
    priority: str

class AcceptanceCriterion(BaseModel):
    requirementId: str
    criterion: str

class DesignSketch(BaseModel):
    folders: List[str]
    files: List[FileDescription]

class FileDescription(BaseModel):
    path: str
    purpose: str
```

**ErrorResponse**
```python
class ErrorResponse(BaseModel):
    error: str
    details: Optional[str] = None
```

### 2. API Endpoint

**POST /generate_brd**

```python
@app.post("/generate_brd", response_model=BRDResponse)
async def generate_brd(request: BRDRequest) -> BRDResponse:
    """
    Generate a Business Requirements Document from project context.
    
    Args:
        request: BRDRequest containing project context
        
    Returns:
        BRDResponse with structured BRD content
        
    Raises:
        HTTPException: 422 for validation errors, 500 for processing errors
    """
```

### 3. BRD Service

```python
class BRDService:
    def __init__(self, openai_client: OpenAIClient):
        self.openai_client = openai_client
    
    async def generate_brd(self, request: BRDRequest) -> BRDResponse:
        """
        Orchestrate BRD generation process.
        
        Args:
            request: Validated BRD request
            
        Returns:
            Structured BRD response
            
        Raises:
            OpenAIError: If OpenAI API call fails
            ValidationError: If response parsing fails
        """
```

### 4. OpenAI Client

```python
class OpenAIClient:
    def __init__(self, api_key: str, model: str = "gpt-4"):
        self.api_key = api_key
        self.model = model
        self.client = OpenAI(api_key=api_key)
    
    def construct_prompt(self, request: BRDRequest) -> str:
        """
        Build a prompt for OpenAI from project context.
        
        Args:
            request: BRD request with project context
            
        Returns:
            Formatted prompt string
        """
    
    async def generate_brd_content(self, prompt: str) -> dict:
        """
        Call OpenAI API to generate BRD content.
        
        Args:
            prompt: Constructed prompt
            
        Returns:
            Parsed JSON response from OpenAI
            
        Raises:
            OpenAIError: If API call fails or response is invalid
        """
```

### 5. Configuration

```python
class Settings(BaseSettings):
    openai_api_key: str
    openai_model: str = "gpt-4"
    server_port: int = 8000
    server_host: str = "0.0.0.0"
    
    class Config:
        env_file = ".env"
```

## Data Models

### Request Flow Data

1. **HTTP Request** → BRDRequest (Pydantic validation)
2. **BRDRequest** → Prompt String (prompt construction)
3. **Prompt String** → OpenAI API (HTTP call)
4. **OpenAI Response** → Raw JSON (API response)
5. **Raw JSON** → BRDResponse (parsing and validation)
6. **BRDResponse** → HTTP Response (serialization)

### Prompt Structure

The prompt sent to OpenAI follows this template:

```
You are a business analyst creating a Business Requirements Document.

Project Name: {projectName}

Context from Email:
{emailText}

Context from Slack:
{slackText}

Context from Meeting:
{meetingText}

Generate a comprehensive Business Requirements Document in JSON format with:
1. A list of requirements (each with id, description, priority)
2. Acceptance criteria for each requirement (with requirementId and criterion)
3. A design sketch showing the proposed folder structure and key files

Return ONLY valid JSON matching this structure:
{
  "requirements": [...],
  "acceptanceCriteria": [...],
  "designSketch": {
    "folders": [...],
    "files": [...]
  }
}
```

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*


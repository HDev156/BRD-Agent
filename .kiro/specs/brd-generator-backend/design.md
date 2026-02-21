# Design Document: BRD Generator Backend API

## Overview

The BRD Generator Backend API is a Python FastAPI application that provides a REST endpoint for generating Business Requirements Documents from project information. The system accepts text from multiple sources (email, Slack, meetings), sends it to OpenAI's API with a structured prompt, and returns a well-formatted BRD in JSON format.

The architecture follows a layered approach with clear separation between API handling, business logic, and external service integration. The design emphasizes testability, maintainability, and clear error handling.

## Architecture

### High-Level Architecture

```
┌─────────────────┐
│  Client App     │
└────────┬────────┘
         │ HTTP POST /generate_brd
         ▼
┌─────────────────────────────────────┐
│      FastAPI Application            │
│  ┌───────────────────────────────┐  │
│  │   API Router & Validators     │  │
│  └──────────┬────────────────────┘  │
│             ▼                        │
│  ┌───────────────────────────────┐  │
│  │   BRD Generator Service       │  │
│  └──────────┬────────────────────┘  │
│             ▼                        │
│  ┌───────────────────────────────┐  │
│  │   OpenAI Client               │  │
│  └──────────┬────────────────────┘  │
└─────────────┼───────────────────────┘
              │
              ▼
     ┌────────────────┐
     │  OpenAI API    │
     └────────────────┘
```

### Directory Structure

```
brd-generator-backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── config.py               # Configuration management
│   ├── models/
│   │   ├── __init__.py
│   │   ├── request.py          # Request models (Pydantic)
│   │   └── response.py         # Response models (Pydantic)
│   ├── services/
│   │   ├── __init__.py
│   │   ├── brd_generator.py    # Core BRD generation logic
│   │   └── openai_client.py    # OpenAI API integration
│   ├── routers/
│   │   ├── __init__.py
│   │   └── brd.py              # BRD endpoint router
│   └── utils/
│       ├── __init__.py
│       └── exceptions.py       # Custom exceptions
├── tests/
│   ├── __init__.py
│   ├── test_brd_endpoint.py    # Integration tests
│   ├── test_brd_generator.py   # Service tests
│   └── test_openai_client.py   # OpenAI client tests
├── .env.example                # Example environment variables
├── .gitignore
├── requirements.txt            # Python dependencies
├── README.md                   # Setup and usage instructions
└── pytest.ini                  # Pytest configuration
```

## Components and Interfaces

### 1. API Router (`app/routers/brd.py`)

**Responsibility:** Handle HTTP requests, validate input, and coordinate response generation.

**Interface:**
```python
@router.post("/generate_brd", response_model=BRDResponse, status_code=200)
async def generate_brd(request: BRDRequest) -> BRDResponse:
    """
    Generate a Business Requirements Document from project information.
    
    Args:
        request: BRDRequest containing projectName and optional text sources
        
    Returns:
        BRDResponse containing the structured BRD
        
    Raises:
        HTTPException: 400 for validation errors, 503 for OpenAI unavailability,
                      500 for unexpected errors
    """
```

### 2. Request Model (`app/models/request.py`)

**Responsibility:** Define and validate the structure of incoming requests.

**Interface:**
```python
class BRDRequest(BaseModel):
    projectName: str = Field(..., min_length=1, description="Name of the project")
    emailText: Optional[str] = Field(None, description="Email content about the project")
    slackText: Optional[str] = Field(None, description="Slack messages about the project")
    meetingText: Optional[str] = Field(None, description="Meeting notes about the project")
    
    @validator('projectName')
    def validate_project_name(cls, v):
        """Ensure project name is not just whitespace"""
        if not v or not v.strip():
            raise ValueError('projectName cannot be empty or whitespace')
        return v.strip()
    
    @root_validator
    def validate_at_least_one_source(cls, values):
        """Ensure at least one text source is provided"""
        sources = [values.get('emailText'), values.get('slackText'), values.get('meetingText')]
        if not any(source and source.strip() for source in sources):
            raise ValueError('At least one of emailText, slackText, or meetingText must be provided')
        return values
```

### 3. Response Model (`app/models/response.py`)

**Responsibility:** Define the structure of the generated BRD response.

**Interface:**
```python
class Requirement(BaseModel):
    id: str = Field(..., description="Unique requirement identifier")
    description: str = Field(..., description="Requirement description")
    priority: str = Field(..., description="Priority level (High, Medium, Low)")

class Stakeholder(BaseModel):
    name: str = Field(..., description="Stakeholder name or role")
    role: str = Field(..., description="Stakeholder's role in the project")

class BRDResponse(BaseModel):
    projectName: str = Field(..., description="Name of the project")
    executiveSummary: str = Field(..., description="High-level project overview")
    businessObjectives: List[str] = Field(..., description="List of business objectives")
    requirements: List[Requirement] = Field(..., description="List of requirements")
    stakeholders: List[Stakeholder] = Field(..., description="List of stakeholders")
```

### 4. BRD Generator Service (`app/services/brd_generator.py`)

**Responsibility:** Orchestrate BRD generation by coordinating with OpenAI client and formatting results.

**Interface:**
```python
class BRDGeneratorService:
    def __init__(self, openai_client: OpenAIClient):
        self.openai_client = openai_client
    
    async def generate_brd(self, request: BRDRequest) -> BRDResponse:
        """
        Generate a structured BRD from project information.
        
        Args:
            request: BRDRequest containing project information
            
        Returns:
            BRDResponse with structured BRD data
            
        Raises:
            OpenAIServiceError: When OpenAI API fails
            BRDGenerationError: When BRD generation fails
        """
        
    def _build_prompt(self, request: BRDRequest) -> str:
        """
        Build the prompt for OpenAI API from request data.
        
        Args:
            request: BRDRequest containing project information
            
        Returns:
            Formatted prompt string
        """
```

### 5. OpenAI Client (`app/services/openai_client.py`)

**Responsibility:** Handle all communication with OpenAI's API.

**Interface:**
```python
class OpenAIClient:
    def __init__(self, api_key: str, model: str = "gpt-4"):
        self.api_key = api_key
        self.model = model
        self.client = OpenAI(api_key=api_key)
    
    async def generate_completion(self, prompt: str, response_format: dict = None) -> str:
        """
        Call OpenAI API to generate a completion.
        
        Args:
            prompt: The prompt to send to OpenAI
            response_format: Optional format specification for structured output
            
        Returns:
            The generated text response
            
        Raises:
            OpenAIServiceError: When the API call fails
        """
```

### 6. Configuration (`app/config.py`)

**Responsibility:** Manage application configuration from environment variables.

**Interface:**
```python
class Settings(BaseSettings):
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")
    openai_model: str = Field("gpt-4", env="OPENAI_MODEL")
    port: int = Field(8000, env="PORT")
    
    class Config:
        env_file = ".env"
        case_sensitive = False

def get_settings() -> Settings:
    """Get application settings singleton"""
```

### 7. Custom Exceptions (`app/utils/exceptions.py`)

**Responsibility:** Define domain-specific exceptions for clear error handling.

**Interface:**
```python
class BRDGenerationError(Exception):
    """Raised when BRD generation fails"""

class OpenAIServiceError(Exception):
    """Raised when OpenAI API communication fails"""

class ValidationError(Exception):
    """Raised when input validation fails"""
```

## Data Models

### Request Flow Data

```
BRDRequest
├── projectName: str (required, non-empty)
├── emailText: Optional[str]
├── slackText: Optional[str]
└── meetingText: Optional[str]
```

### Response Flow Data

```
BRDResponse
├── projectName: str
├── executiveSummary: str
├── businessObjectives: List[str]
├── requirements: List[Requirement]
│   └── Requirement
│       ├── id: str
│       ├── description: str
│       └── priority: str
└── stakeholders: List[Stakeholder]
    └── Stakeholder
        ├── name: str
        └── role: str
```

### OpenAI Prompt Structure

The prompt sent to OpenAI will follow this structure:

```
You are a business analyst creating a Business Requirements Document.

Project Name: {projectName}

Source Information:
{combined_text_from_email_slack_meeting}

Generate a comprehensive BRD in JSON format with the following structure:
{
  "projectName": "string",
  "executiveSummary": "string",
  "businessObjectives": ["string"],
  "requirements": [
    {
      "id": "string",
      "description": "string",
      "priority": "High|Medium|Low"
    }
  ],
  "stakeholders": [
    {
      "name": "string",
      "role": "string"
    }
  ]
}
```



## Correctness Properties

A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.

### Property 1: Request validation rejects invalid inputs

*For any* request with missing or invalid required fields (empty projectName or all text fields empty), the API should return a 400 status code with a descriptive error message.

**Validates: Requirements 1.2, 1.3, 2.2, 2.6**

### Property 2: Valid requests are accepted

*For any* request with a non-empty projectName and at least one non-empty text field, the API should accept the request and return either a 200 status code (success) or a 5xx status code (server error), but never a 400 status code (validation error).

**Validates: Requirements 1.4, 1.5**

### Property 3: Response structure completeness

*For any* successful BRD generation, the response JSON should contain all required fields: projectName (string), executiveSummary (string), businessObjectives (array), requirements (array), and stakeholders (array).

**Validates: Requirements 4.1, 4.2, 4.3, 4.4, 4.5**

### Property 4: Requirement object structure

*For any* requirement in the requirements array of a generated BRD, the requirement object should contain id (string), description (string), and priority (string) fields.

**Validates: Requirements 4.6**

### Property 5: Prompt includes project information

*For any* valid BRD request, the prompt sent to OpenAI should contain the projectName and all non-empty text fields (emailText, slackText, meetingText) from the request.

**Validates: Requirements 3.2**

### Property 6: OpenAI error handling

*For any* error returned by the OpenAI API (rate limit, authentication failure, service unavailable), the OpenAI client should raise an exception that includes the error details.

**Validates: Requirements 3.4**

### Property 7: Validation error responses

*For any* validation failure, the API should return a 400 status code with a JSON response containing an error message that describes what validation failed.

**Validates: Requirements 5.1**

### Property 8: Optional fields are truly optional

*For any* valid request, omitting any combination of the optional fields (emailText, slackText, meetingText) should not cause a validation error, as long as at least one text field is provided.

**Validates: Requirements 2.3, 2.4, 2.5**

## Error Handling

### Error Categories

1. **Validation Errors (400)**
   - Missing or empty projectName
   - All text fields empty or missing
   - Invalid JSON structure
   - Response: `{"detail": "Descriptive error message"}`

2. **OpenAI Service Errors (503)**
   - OpenAI API unavailable
   - Rate limit exceeded
   - Network timeout
   - Response: `{"detail": "OpenAI service is currently unavailable. Please try again later."}`

3. **Processing Errors (500)**
   - Invalid response from OpenAI (cannot parse JSON)
   - Unexpected exceptions during processing
   - Response: `{"detail": "An error occurred while generating the BRD. Please try again."}`

4. **Configuration Errors (Startup)**
   - Missing OPENAI_API_KEY environment variable
   - Invalid configuration values
   - Action: Application fails to start with clear error message

### Error Handling Flow

```
Request → Validation
            ├─ Invalid → 400 Response
            └─ Valid → BRD Generation
                        ├─ OpenAI Error → 503 Response
                        ├─ Processing Error → 500 Response
                        └─ Success → 200 Response with BRD
```

### Logging Strategy

- **INFO**: Successful BRD generation requests
- **WARNING**: OpenAI API errors, rate limiting
- **ERROR**: Unexpected exceptions, processing failures
- **DEBUG**: Request/response details (excluding sensitive data)

All logs should include:
- Timestamp
- Request ID (for tracing)
- Endpoint
- Status code
- Error details (if applicable)

Sensitive data (API keys, full request content) should never be logged.

## Testing Strategy

### Dual Testing Approach

The testing strategy employs both unit tests and property-based tests to ensure comprehensive coverage:

- **Unit tests**: Verify specific examples, edge cases, and error conditions
- **Property tests**: Verify universal properties across all inputs using randomized testing

Both approaches are complementary and necessary. Unit tests catch concrete bugs in specific scenarios, while property tests verify general correctness across a wide range of inputs.

### Property-Based Testing

We will use **Hypothesis** (Python's property-based testing library) to implement property tests.

**Configuration:**
- Each property test must run a minimum of 100 iterations
- Each test must include a comment tag referencing the design property
- Tag format: `# Feature: brd-generator-backend, Property {number}: {property_text}`

**Property Test Coverage:**
- Property 1: Generate random invalid requests and verify 400 responses
- Property 2: Generate random valid requests and verify non-400 responses
- Property 3: Generate random valid requests and verify response structure
- Property 4: Generate random BRD responses and verify requirement structure
- Property 5: Generate random requests and verify prompt construction
- Property 6: Simulate random OpenAI errors and verify exception handling
- Property 7: Generate random validation failures and verify error responses
- Property 8: Generate random combinations of optional fields and verify acceptance

### Unit Testing

Unit tests focus on:
- Specific examples of valid and invalid requests
- Edge cases (empty strings, whitespace-only strings, very long inputs)
- Error conditions (OpenAI unavailable, invalid API key, malformed responses)
- Configuration loading and validation
- Documentation endpoint availability

### Integration Testing

Integration tests verify:
- End-to-end flow from HTTP request to response
- Interaction between router, service, and OpenAI client
- Error propagation through the stack
- Response formatting and serialization

### Test Structure

```
tests/
├── test_brd_endpoint.py
│   ├── test_generate_brd_success (integration)
│   ├── test_generate_brd_missing_project_name (unit)
│   ├── test_generate_brd_empty_text_fields (unit)
│   ├── test_generate_brd_openai_error (integration)
│   └── test_property_* (property-based tests)
│
├── test_brd_generator.py
│   ├── test_build_prompt (unit)
│   ├── test_generate_brd_service (unit)
│   └── test_property_prompt_includes_info (property)
│
└── test_openai_client.py
    ├── test_generate_completion_success (unit)
    ├── test_generate_completion_error (unit)
    └── test_property_error_handling (property)
```

### Mocking Strategy

- Mock OpenAI API calls in all tests to ensure independence
- Use `pytest-mock` for mocking
- Create fixtures for common test data (valid requests, mock responses)
- Mock environment variables for configuration tests

### Test Data Generation

For property-based tests, use Hypothesis strategies:
- `st.text()` for string fields
- `st.one_of()` for optional fields
- `st.builds()` for complex objects
- Custom strategies for valid/invalid request generation

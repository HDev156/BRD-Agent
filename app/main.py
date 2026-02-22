"""FastAPI application entry point for the BRD Generator Backend API.

This module initializes the FastAPI application, configures routers,
error handlers, and startup validation.
"""

import logging
import uuid
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError as PydanticValidationError
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from app.config import get_settings
from app.routers import brd, dataset, context
from app.utils.exceptions import BRDGenerationError, OpenAIServiceError, ValidationError
from app.utils.logging_config import configure_structured_logging
from app.dependencies import get_ingestion_tracker


# Configure structured logging
# Set use_json=False for development, use_json=True for production
configure_structured_logging(level="INFO", use_json=True, enable_sensitive_filter=True)
logger = logging.getLogger(__name__)


# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan manager for startup and shutdown events.
    
    This function validates configuration on startup and performs cleanup
    on shutdown if needed.
    
    Args:
        app: FastAPI application instance
        
    Yields:
        None
        
    Raises:
        Exception: If configuration validation fails
    """
    # Startup: Validate configuration
    logger.info("Starting BRD Generator Backend API...")
    try:
        settings = get_settings()
        logger.info(f"Configuration loaded successfully")
        logger.info(f"Using OpenAI model: {settings.openai_model}")
        logger.info(f"Server will run on port: {settings.port}")
        # Verify API key is present (don't log the actual key)
        if not settings.openai_api_key:
            raise ValueError("OPENAI_API_KEY is required but not set")
        logger.info("OpenAI API key validated")
        
        # Start background cleanup task for tracking sessions
        tracker = get_ingestion_tracker()
        tracker.start_cleanup_task(cleanup_interval=600)  # Run every 10 minutes
        logger.info("Tracking session cleanup task started")
    except Exception as e:
        logger.error(f"Configuration validation failed: {e}")
        raise
    
    logger.info("Application startup complete")
    
    yield
    
    # Shutdown: Cleanup if needed
    logger.info("Shutting down BRD Generator Backend API...")


# Initialize FastAPI application
app = FastAPI(
    title="BRD Generator Backend API",
    description="A REST API for generating Business Requirements Documents from project information using OpenAI",
    version="1.0.0",
    lifespan=lifespan
)

# Add rate limiter state to app
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Middleware to add request ID to each request
@app.middleware("http")
async def add_request_id(request: Request, call_next):
    """Middleware to generate and track request IDs for logging.
    
    This middleware generates a unique request ID for each incoming request
    and adds it to the request state for use in logging throughout the
    request lifecycle.
    
    Args:
        request: The incoming request
        call_next: The next middleware or route handler
        
    Returns:
        Response from the next handler
    """
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id
    
    # Log the incoming request
    logger.info(
        f"Incoming request: {request.method} {request.url.path}",
        extra={'request_id': request_id}
    )
    
    response = await call_next(request)
    
    # Log the response status
    logger.info(
        f"Request completed: {request.method} {request.url.path} - Status: {response.status_code}",
        extra={'request_id': request_id}
    )
    
    return response


# Include routers
app.include_router(brd.router, tags=["BRD Generation"])
app.include_router(dataset.router, prefix="/dataset", tags=["Dataset BRD Generation"])
app.include_router(context.router, tags=["Context BRD Generation"])

# Import processing router
from app.routers import processing
app.include_router(processing.router, prefix="/processing", tags=["Processing Status"])


# Error handlers for custom exceptions
@app.exception_handler(ValidationError)
async def validation_error_handler(request: Request, exc: ValidationError) -> JSONResponse:
    """Handle custom ValidationError exceptions.
    
    Args:
        request: The incoming request
        exc: The ValidationError exception
        
    Returns:
        JSONResponse with 400 status code and error details
    """
    request_id = getattr(request.state, 'request_id', 'N/A')
    logger.warning(
        f"Validation error: {exc}",
        extra={'request_id': request_id}
    )
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc)}
    )


@app.exception_handler(OpenAIServiceError)
async def openai_service_error_handler(request: Request, exc: OpenAIServiceError) -> JSONResponse:
    """Handle OpenAIServiceError exceptions.
    
    Args:
        request: The incoming request
        exc: The OpenAIServiceError exception
        
    Returns:
        JSONResponse with 503 status code and error details
    """
    request_id = getattr(request.state, 'request_id', 'N/A')
    logger.error(
        f"OpenAI service error: {exc}",
        extra={'request_id': request_id}
    )
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={"detail": f"OpenAI service is currently unavailable: {str(exc)}"}
    )


@app.exception_handler(BRDGenerationError)
async def brd_generation_error_handler(request: Request, exc: BRDGenerationError) -> JSONResponse:
    """Handle BRDGenerationError exceptions.
    
    Args:
        request: The incoming request
        exc: The BRDGenerationError exception
        
    Returns:
        JSONResponse with 500 status code and error details
    """
    request_id = getattr(request.state, 'request_id', 'N/A')
    logger.error(
        f"BRD generation error: {exc}",
        extra={'request_id': request_id}
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": f"An error occurred while generating the BRD: {str(exc)}"}
    )


@app.exception_handler(PydanticValidationError)
async def pydantic_validation_error_handler(request: Request, exc: PydanticValidationError) -> JSONResponse:
    """Handle Pydantic ValidationError exceptions.
    
    Args:
        request: The incoming request
        exc: The PydanticValidationError exception
        
    Returns:
        JSONResponse with 400 status code and error details
    """
    request_id = getattr(request.state, 'request_id', 'N/A')
    logger.warning(
        f"Pydantic validation error: {exc}",
        extra={'request_id': request_id}
    )
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": f"Validation error: {str(exc)}"}
    )


@app.get("/", tags=["Health"])
async def root() -> dict:
    """Root endpoint for health check.
    
    Returns:
        dict: Simple health check response
    """
    return {
        "message": "BRD Generator Backend API is running",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }

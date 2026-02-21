"""Dataset-based BRD generation router.

This module provides endpoints for generating BRDs from dataset sources
like Enron emails and AMI meeting transcripts.
"""

import logging
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends, Request, Query
from pydantic import BaseModel, Field

from app.models.response import BRDResponse
from app.services.brd_generator import BRDGeneratorService
from app.services.openai_client import OpenAIClient
from app.services.multi_channel_ingestion import (
    MultiChannelIngestionService,
    DatasetConfig
)
from app.utils.exceptions import BRDGenerationError, OpenAIServiceError
from app.config import get_settings

router = APIRouter()
logger = logging.getLogger(__name__)


class DatasetBRDRequest(BaseModel):
    """Request model for dataset-based BRD generation."""
    
    projectName: str = Field(..., min_length=1, description="Name of the project")
    keywords: Optional[List[str]] = Field(
        None,
        description="Keywords to filter dataset content"
    )
    sampleSize: Optional[int] = Field(
        None,
        ge=1,
        le=1000,
        description="Number of items to sample from dataset (max 1000)"
    )


class DatasetBRDResponse(BRDResponse):
    """Extended response model for dataset-based BRD generation."""
    
    metadata: dict = Field(..., description="Metadata about dataset processing")
    conflicts: List[dict] = Field(default=[], description="Detected conflicts in data")


def get_dataset_service() -> MultiChannelIngestionService:
    """Dependency injection for MultiChannelIngestionService.
    
    Returns:
        MultiChannelIngestionService instance
    """
    settings = get_settings()
    
    config = DatasetConfig(
        enabled=settings.dataset_mode_enabled,
        email_dataset_path=settings.email_dataset_path,
        meeting_dataset_path=settings.meeting_dataset_path,
        max_emails=settings.max_dataset_emails,
        max_meetings=settings.max_dataset_meetings,
        sample_size=settings.dataset_sample_size
    )
    
    return MultiChannelIngestionService(config)


def get_brd_generator_service() -> BRDGeneratorService:
    """Dependency injection for BRDGeneratorService.
    
    Returns:
        BRDGeneratorService instance
    """
    settings = get_settings()
    openai_client = OpenAIClient(
        api_key=settings.openai_api_key,
        model=settings.openai_model,
        base_url=settings.openai_base_url
    )
    return BRDGeneratorService(openai_client)


@router.post("/generate_brd_from_dataset", response_model=DatasetBRDResponse, status_code=200)
async def generate_brd_from_dataset(
    http_request: Request,
    request: DatasetBRDRequest,
    dataset_service: MultiChannelIngestionService = Depends(get_dataset_service),
    brd_service: BRDGeneratorService = Depends(get_brd_generator_service)
) -> DatasetBRDResponse:
    """Generate a BRD from dataset sources.
    
    This endpoint processes emails and meeting transcripts from datasets,
    filters them by keywords, and generates a structured BRD.
    
    Args:
        http_request: FastAPI Request object
        request: Dataset BRD request
        dataset_service: Injected dataset ingestion service
        brd_service: Injected BRD generation service
        
    Returns:
        DatasetBRDResponse with BRD and metadata
        
    Raises:
        HTTPException: Various status codes for different error conditions
    """
    request_id = getattr(http_request.state, 'request_id', 'N/A')
    
    try:
        logger.info(
            f"Generating BRD from dataset for project: {request.projectName}",
            extra={'request_id': request_id}
        )
        
        # Check if dataset mode is enabled
        if not dataset_service.config.enabled:
            raise HTTPException(
                status_code=400,
                detail="Dataset mode is not enabled. Please configure dataset paths."
            )
        
        # Override sample size if provided
        if request.sampleSize:
            dataset_service.config.sample_size = request.sampleSize
        
        # Process dataset input
        unified_input = dataset_service.process_dataset_input(
            project_name=request.projectName,
            keywords=request.keywords
        )
        
        # Check if any content was found
        if not any([
            unified_input.email_content,
            unified_input.slack_content,
            unified_input.meeting_content
        ]):
            raise HTTPException(
                status_code=404,
                detail="No relevant content found in dataset with the provided keywords"
            )
        
        # Detect conflicts
        conflicts = dataset_service.detect_conflicts(unified_input)
        
        # Convert to BRD request format
        brd_request = dataset_service.normalize_to_brd_request(unified_input)
        
        # Generate BRD
        brd_response = await brd_service.generate_brd(brd_request)
        
        logger.info(
            f"Successfully generated BRD from dataset for project: {request.projectName}",
            extra={'request_id': request_id}
        )
        
        # Create extended response
        return DatasetBRDResponse(
            projectName=brd_response.projectName,
            executiveSummary=brd_response.executiveSummary,
            businessObjectives=brd_response.businessObjectives,
            requirements=brd_response.requirements,
            stakeholders=brd_response.stakeholders,
            metadata=unified_input.metadata or {},
            conflicts=conflicts
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    
    except OpenAIServiceError as e:
        logger.error(
            f"OpenAI service error for dataset project {request.projectName}: {str(e)}",
            extra={'request_id': request_id}
        )
        raise HTTPException(
            status_code=503,
            detail=f"OpenAI service is currently unavailable: {str(e)}"
        )
    
    except BRDGenerationError as e:
        logger.error(
            f"BRD generation error for dataset project {request.projectName}: {str(e)}",
            extra={'request_id': request_id}
        )
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while generating the BRD: {str(e)}"
        )
    
    except Exception as e:
        logger.error(
            f"Unexpected error for dataset project {request.projectName}: {str(e)}",
            extra={'request_id': request_id}
        )
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {str(e)}"
        )


@router.get("/dataset_status")
async def get_dataset_status(
    dataset_service: MultiChannelIngestionService = Depends(get_dataset_service)
) -> dict:
    """Get the status of dataset configuration.
    
    Args:
        dataset_service: Injected dataset service
        
    Returns:
        Dictionary with dataset configuration status
    """
    return {
        "dataset_mode_enabled": dataset_service.config.enabled,
        "email_dataset_configured": dataset_service.config.email_dataset_path is not None,
        "meeting_dataset_configured": dataset_service.config.meeting_dataset_path is not None,
        "max_emails": dataset_service.config.max_emails,
        "max_meetings": dataset_service.config.max_meetings,
        "sample_size": dataset_service.config.sample_size
    }
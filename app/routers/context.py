"""Context Router for context-aware BRD generation.

This module defines the API endpoint for generating Business Requirements Documents
with context-aware processing including user instructions, large data handling,
and ingestion transparency.
"""

import logging
import uuid
from typing import Optional
from fastapi import APIRouter, HTTPException, Depends, Request
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.models.context_request import (
    ContextRequest,
    ContextResponse,
    AlignmentAnalysis,
    IngestionData
)
from app.models.constraints import Constraints
from app.models.ingestion_summary import IngestionSummary
from app.models.request import BRDRequest
from app.models.chunk_models import ExtractionResult, TextChunk
from app.services.gemini_service import GeminiService
from app.services.constraint_applier import ConstraintApplier
from app.services.chunk_processor import ChunkProcessor
from app.services.ingestion_tracker import IngestionTracker
from app.services.aggregator import Aggregator
from app.services.brd_generator import BRDGeneratorService
from app.services.alignment_intelligence import AlignmentIntelligenceEngine
from app.services.openai_client import OpenAIClient
from app.utils.exceptions import (
    GeminiAPIError,
    GeminiTimeoutError,
    GeminiRateLimitError,
    ConstraintValidationError,
    BRDGenerationError,
    OpenAIServiceError
)
from app.utils.validators import validate_context_request
from app.config import get_settings


router = APIRouter()
logger = logging.getLogger(__name__)

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)


# Dependency injection functions
def get_gemini_service() -> Optional[GeminiService]:
    """Dependency injection for GeminiService.
    
    Returns:
        GeminiService instance if API key is configured, None otherwise
    """
    settings = get_settings()
    if not settings.gemini_api_key:
        logger.warning("Gemini API key not configured, constraint generation will be disabled")
        return None
    
    return GeminiService(
        api_key=settings.gemini_api_key,
        model=settings.gemini_model,
        timeout=settings.gemini_timeout,
        max_retries=settings.gemini_max_retries
    )


def get_constraint_applier() -> ConstraintApplier:
    """Dependency injection for ConstraintApplier.
    
    Returns:
        ConstraintApplier instance
    """
    return ConstraintApplier()


def get_chunk_processor() -> ChunkProcessor:
    """Dependency injection for ChunkProcessor.
    
    Returns:
        ChunkProcessor instance with configured parameters
    """
    settings = get_settings()
    return ChunkProcessor(
        threshold_words=settings.chunk_threshold_words,
        chunk_size_min=settings.chunk_size_min,
        chunk_size_max=settings.chunk_size_max,
        overlap=settings.chunk_overlap
    )


def get_ingestion_tracker() -> IngestionTracker:
    """Dependency injection for IngestionTracker.
    
    Returns:
        IngestionTracker instance with configured parameters
    """
    settings = get_settings()
    return IngestionTracker(
        sample_count=settings.sample_sources_count,
        session_ttl=settings.tracking_session_ttl
    )


def get_aggregator() -> Aggregator:
    """Dependency injection for Aggregator.
    
    Returns:
        Aggregator instance
    """
    return Aggregator()


def get_brd_generator_service() -> BRDGeneratorService:
    """Dependency injection for BRDGeneratorService.
    
    Returns:
        BRDGeneratorService instance with configured OpenAI client
    """
    settings = get_settings()
    openai_client = OpenAIClient(
        api_key=settings.openai_api_key,
        model=settings.openai_model,
        base_url=settings.openai_base_url
    )
    return BRDGeneratorService(openai_client)


def get_alignment_engine() -> AlignmentIntelligenceEngine:
    """Dependency injection for AlignmentIntelligenceEngine.
    
    Returns:
        AlignmentIntelligenceEngine instance
    """
    return AlignmentIntelligenceEngine()


@router.post("/generate_brd_with_context", response_model=ContextResponse, status_code=200)
@limiter.limit("10/minute")
async def generate_brd_with_context(
    request: Request,
    context_request: ContextRequest,
    gemini_service: Optional[GeminiService] = Depends(get_gemini_service),
    constraint_applier: ConstraintApplier = Depends(get_constraint_applier),
    chunk_processor: ChunkProcessor = Depends(get_chunk_processor),
    ingestion_tracker: IngestionTracker = Depends(get_ingestion_tracker),
    aggregator: Aggregator = Depends(get_aggregator),
    brd_service: BRDGeneratorService = Depends(get_brd_generator_service),
    alignment_engine: AlignmentIntelligenceEngine = Depends(get_alignment_engine)
) -> ContextResponse:
    """Generate BRD with context-aware processing.
    
    This endpoint provides advanced BRD generation with:
    1. User Instruction Layer: Natural language instructions converted to constraints
    2. Large Data Handling: Automatic chunking of large texts (>3000 words)
    3. Ingestion Transparency: Detailed tracking of data sources used
    
    The endpoint maintains backward compatibility - if no instructions are provided,
    it behaves like the standard BRD generation endpoint.
    
    Args:
        request: FastAPI Request object for accessing request state
        context_request: ContextRequest with optional instructions and data
        gemini_service: Injected Gemini service for constraint generation
        constraint_applier: Injected constraint applier service
        chunk_processor: Injected chunk processor service
        ingestion_tracker: Injected ingestion tracker service
        aggregator: Injected aggregator service
        brd_service: Injected BRD generator service
        alignment_engine: Injected alignment intelligence engine
        
    Returns:
        ContextResponse with BRD, alignment analysis, and ingestion summary
        
    Raises:
        HTTPException:
            - 400 for validation errors
            - 503 for service unavailability
            - 500 for unexpected errors
    """
    request_id = getattr(request.state, 'request_id', str(uuid.uuid4()))
    
    try:
        logger.info(
            "Starting context-aware BRD generation",
            extra={'request_id': request_id}
        )
        
        # Step 0: Validate and sanitize input
        sanitized_instructions, validated_data = validate_context_request(
            context_request.instructions,
            context_request.data
        )
        
        logger.info(
            "Input validation complete",
            extra={
                'request_id': request_id,
                'has_instructions': bool(sanitized_instructions),
                'total_items': len(validated_data.emails) + len(validated_data.slack_messages) + len(validated_data.meetings)
            }
        )
        
        # Step 1: Generate constraints from instructions (if provided)
        constraints: Optional[Constraints] = None
        if sanitized_instructions and sanitized_instructions.strip():
            logger.info(
                "Generating constraints from instructions",
                extra={
                    'request_id': request_id,
                    'instructions_length': len(sanitized_instructions),
                    'instructions_preview': sanitized_instructions[:100]
                }
            )
            
            if gemini_service:
                try:
                    constraints = await gemini_service.generate_constraints(
                        sanitized_instructions,
                        request_id=request_id
                    )
                    
                    if constraints:
                        logger.info(
                            "Constraints generated successfully",
                            extra={
                                'request_id': request_id,
                                'has_scope': bool(constraints.scope),
                                'exclude_topics_count': len(constraints.exclude_topics)
                            }
                        )
                    else:
                        logger.warning(
                            "Constraint generation returned None, continuing without constraints",
                            extra={'request_id': request_id}
                        )
                        
                except (GeminiAPIError, GeminiTimeoutError, GeminiRateLimitError, ConstraintValidationError) as e:
                    logger.warning(
                        "Gemini service error, continuing without constraints",
                        extra={'request_id': request_id, 'error': str(e)}
                    )
                    constraints = None
            else:
                logger.warning(
                    "Gemini service not available, skipping constraint generation",
                    extra={'request_id': request_id}
                )
        else:
            logger.info(
                "No instructions provided, skipping constraint generation",
                extra={'request_id': request_id}
            )
        
        # Step 2: Apply constraints to filter data
        filtered_data: IngestionData = constraint_applier.apply_constraints(
            validated_data,
            constraints
        )
        
        logger.info(
            "Data filtering complete",
            extra={
                'request_id': request_id,
                'emails_count': len(filtered_data.emails),
                'slack_count': len(filtered_data.slack_messages),
                'meetings_count': len(filtered_data.meetings)
            }
        )
        
        # Step 3: Start ingestion tracking
        tracking_id = ingestion_tracker.start_tracking()
        logger.info(
            "Started ingestion tracking",
            extra={'request_id': request_id, 'tracking_id': tracking_id}
        )
        
        # Step 4: Process each data source (check chunking, extract, track)
        all_extraction_results: list[ExtractionResult] = []
        
        # Collect all text content for BRD generation
        email_texts = []
        slack_texts = []
        meeting_texts = []
        
        # Process emails
        for email in filtered_data.emails:
            ingestion_tracker.track_email(tracking_id, email)
            email_text = f"Subject: {email.subject}\nFrom: {email.sender}\n{email.body}"
            email_texts.append(email_text)
        
        # Process Slack messages
        for slack_msg in filtered_data.slack_messages:
            ingestion_tracker.track_slack_message(tracking_id, slack_msg)
            slack_text = f"[{slack_msg.channel}] {slack_msg.user}: {slack_msg.text}"
            slack_texts.append(slack_text)
        
        # Process meetings (with chunking if needed)
        # Optimize: Process multiple large meetings in parallel
        meetings_needing_chunking = []
        meetings_no_chunking = []
        
        for meeting in filtered_data.meetings:
            ingestion_tracker.track_meeting(tracking_id, meeting)
            
            if chunk_processor.needs_chunking(meeting.transcript):
                meetings_needing_chunking.append(meeting)
            else:
                meetings_no_chunking.append(meeting)
        
        # Process meetings that don't need chunking
        for meeting in meetings_no_chunking:
            meeting_text = f"Meeting: {meeting.topic}\n{meeting.transcript}"
            meeting_texts.append(meeting_text)
        
        # Process meetings that need chunking in parallel (if multiple)
        if meetings_needing_chunking:
            logger.info(
                "Processing large meetings with parallel chunking",
                extra={
                    'request_id': request_id,
                    'large_meetings_count': len(meetings_needing_chunking)
                }
            )
            
            # Extract transcripts for parallel processing
            transcripts = [m.transcript for m in meetings_needing_chunking]
            
            # Chunk all large meetings in parallel
            chunk_lists = await chunk_processor.chunk_multiple_texts_async(transcripts)
            
            # Track chunks and build meeting texts
            for meeting, chunks in zip(meetings_needing_chunking, chunk_lists):
                logger.info(
                    "Meeting chunked",
                    extra={
                        'request_id': request_id,
                        'meeting_topic': meeting.topic,
                        'chunk_count': len(chunks),
                        'word_count': len(meeting.transcript.split())
                    }
                )
                
                # Track each chunk
                for chunk in chunks:
                    ingestion_tracker.track_chunk(tracking_id, chunk)
                
                # For now, we'll use the full transcript for BRD generation
                # In a full implementation, we would extract from each chunk and aggregate
                meeting_text = f"Meeting: {meeting.topic}\n{meeting.transcript}"
                meeting_texts.append(meeting_text)
        
        logger.info(
            f"Data processing complete, preparing for BRD generation",
            extra={'request_id': request_id}
        )
        
        # Step 5: Aggregate chunk results (if any chunking occurred)
        # Note: In this implementation, we're not doing per-chunk extraction yet
        # This would be implemented in a future iteration
        
        # Step 6: Generate BRD
        # Convert filtered data to BRDRequest format
        combined_email_text = "\n\n---\n\n".join(email_texts) if email_texts else None
        combined_slack_text = "\n".join(slack_texts) if slack_texts else None
        combined_meeting_text = "\n\n---\n\n".join(meeting_texts) if meeting_texts else None
        
        # Create a project name from the first email subject or use a default
        project_name = "Project"
        if filtered_data.emails and filtered_data.emails[0].subject:
            project_name = filtered_data.emails[0].subject[:50]
        
        brd_request = BRDRequest(
            projectName=project_name,
            emailText=combined_email_text,
            slackText=combined_slack_text,
            meetingText=combined_meeting_text
        )
        
        logger.info(
            "Generating BRD",
            extra={
                'request_id': request_id,
                'project_name': project_name
            }
        )
        
        brd_response = await brd_service.generate_brd(brd_request)
        
        logger.info(
            "BRD generation complete",
            extra={'request_id': request_id}
        )
        
        # Step 7: Run alignment analysis
        logger.info(
            "Running alignment analysis",
            extra={'request_id': request_id}
        )
        
        alignment_report = alignment_engine.analyze_alignment(
            email_content=combined_email_text,
            slack_content=combined_slack_text,
            meeting_content=combined_meeting_text,
            brd_data=brd_response.model_dump()
        )
        
        # Generate conflict explanations
        conflict_explanations = alignment_engine.generate_conflict_explanations(
            alignment_report.conflicts
        )
        
        logger.info(
            "Alignment analysis complete",
            extra={
                'request_id': request_id,
                'alignment_score': round(alignment_report.alignment_score, 2),
                'risk_level': alignment_report.risk_level,
                'conflicts_count': len(alignment_report.conflicts)
            }
        )
        
        # Step 8: Build response with ingestion summary
        ingestion_summary = ingestion_tracker.get_summary(tracking_id)
        
        logger.info(
            "Context-aware BRD generation complete",
            extra={
                'request_id': request_id,
                'tracking_id': tracking_id,
                'total_processing_time': ingestion_summary.processing_time_seconds
            }
        )
        
        # Build alignment analysis response
        alignment_analysis = AlignmentAnalysis(
            alignment_score=round(alignment_report.alignment_score, 2),
            risk_level=alignment_report.risk_level,
            alert=alignment_report.alert,
            conflicts=conflict_explanations,
            timeline_mismatches=alignment_report.timeline_mismatches,
            requirement_volatility=alignment_report.requirement_volatility,
            stakeholder_agreement_score=round(alignment_report.stakeholder_agreement_score, 2),
            timeline_consistency_score=round(alignment_report.timeline_consistency_score, 2),
            requirement_stability_score=round(alignment_report.requirement_stability_score, 2),
            decision_volatility_score=round(alignment_report.decision_volatility_score, 2)
        )
        
        # Build final response
        response = ContextResponse(
            brd=brd_response,
            alignment_analysis=alignment_analysis,
            ingestion_summary=ingestion_summary
        )
        
        return response
        
    except OpenAIServiceError as e:
        logger.error(
            "OpenAI service error",
            extra={'request_id': request_id, 'error': str(e)}
        )
        raise HTTPException(
            status_code=503,
            detail=f"OpenAI service is currently unavailable: {str(e)}"
        )
    
    except BRDGenerationError as e:
        logger.error(
            "BRD generation error",
            extra={'request_id': request_id, 'error': str(e)}
        )
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while generating the BRD: {str(e)}"
        )
    
    except ValueError as e:
        logger.warning(
            "Validation error",
            extra={'request_id': request_id, 'error': str(e)}
        )
        raise HTTPException(
            status_code=400,
            detail=f"Validation error: {str(e)}"
        )
    
    except Exception as e:
        logger.error(
            "Unexpected error during context-aware BRD generation",
            extra={'request_id': request_id, 'error': str(e)},
            exc_info=True
        )
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {str(e)}"
        )

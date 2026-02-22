# Implementation Plan: Production Features

## Overview

This implementation plan breaks down the three production features into discrete coding tasks:
1. User Instruction Layer (Gemini Integration)
2. Large Data Handling (Meeting Chunking)
3. Ingestion Transparency (Explainability)

Each task builds incrementally, with property-based tests integrated throughout to catch errors early. The plan maintains backward compatibility while adding the new `/generate_brd_with_context` endpoint.

---

## Tasks

- [x] 1. Set up project structure and dependencies
  - Create new service modules: `gemini_service.py`, `chunk_processor.py`, `ingestion_tracker.py`, `constraint_applier.py`, `aggregator.py`
  - Create new model files: `context_request.py`, `constraints.py`, `ingestion_summary.py`
  - Create new router: `context.py`
  - Create utility: `text_splitter.py`
  - Update `requirements.txt` with new dependencies: `google-generativeai==0.3.2`, `hypothesis==6.98.0`
  - Update `config.py` with new environment variables
  - _Requirements: TR-1, TR-2, TR-3, NFR-1, NFR-3_

- [x] 2. Implement data models
  - [x] 2.1 Create Constraints model in `app/models/constraints.py`
    - Define Pydantic model with fields: scope, exclude_topics, priority_focus, deadline_override
    - Add validation and example schema
    - _Requirements: 1.2.2, 1.2.3_
  
  - [x] 2.2 Create IngestionSummary and SampleSource models in `app/models/ingestion_summary.py`
    - Define IngestionSummary with all tracking fields
    - Define SampleSource with type and metadata
    - Add JSON schema examples
    - _Requirements: 3.1.5, 3.2.1, 3.2.2, 3.2.3, 3.2.4_
  
  - [x] 2.3 Create ContextRequest and ContextResponse models in `app/models/context_request.py`
    - Define ContextRequest with optional instructions and data
    - Define ContextResponse extending existing response with ingestion_summary
    - _Requirements: TR-4_
  
  - [x] 2.4 Create TextChunk and ExtractionResult models
    - Define TextChunk dataclass with chunk metadata
    - Define ExtractionResult with requirements, decisions, stakeholders, timelines
    - _Requirements: 2.1.2, 2.2.1_

- [x] 3. Implement Gemini Service
  - [x] 3.1 Create GeminiService class in `app/services/gemini_service.py`
    - Initialize with API key, model, timeout configuration
    - Implement `generate_constraints()` async method
    - Implement prompt building with template
    - Implement response parsing to Constraints object
    - Add retry logic with exponential backoff (2 retries)
    - Add timeout handling (10 seconds)
    - Add comprehensive error handling and logging
    - _Requirements: 1.1.2, 1.2.1, 1.2.4, 1.2.5, TR-1_
  
  - [x] 3.2 Write property test for constraint generation validity
    - **Property 2: Constraint generation validity**
    - **Validates: Requirements 1.1.2**
    - Test that valid instructions produce valid Constraints with all required fields
    - Use Hypothesis to generate random instruction strings
    - Mock Gemini API responses
    - Run 100 iterations
  
  - [ ] 3.3 Write unit tests for Gemini Service
    - Test API timeout handling
    - Test retry logic with exponential backoff
    - Test error responses (rate limit, API errors)
    - Test fallback to None on failure
    - Mock Gemini API for all tests
    - _Requirements: 1.2.4, 1.2.5, TR-1_

- [x] 4. Implement Constraint Applier
  - [x] 4.1 Create ConstraintApplier class in `app/services/constraint_applier.py`
    - Implement `apply_constraints()` method
    - Implement `_filter_by_scope()` with keyword matching
    - Implement `_contains_excluded_topics()` with case-insensitive matching
    - Implement `_calculate_priority_score()` for ranking
    - Add logging for filtering statistics
    - Handle None constraints (return data unchanged)
    - _Requirements: 1.1.3, 1.1.4, 1.1.5_
  
  - [ ] 4.2 Write property test for topic exclusion
    - **Property 4: Topic exclusion**
    - **Validates: Requirements 1.1.4**
    - Test that items containing excluded topics are removed
    - Generate random data and excluded topic lists
    - Run 100 iterations
  
  - [ ] 4.3 Write property test for scope prioritization
    - **Property 5: Scope prioritization**
    - **Validates: Requirements 1.1.5**
    - Test that scope-matching items appear first
    - Generate random data with varying scope matches
    - Run 100 iterations
  
  - [ ] 4.4 Write unit tests for Constraint Applier
    - Test with None constraints (no filtering)
    - Test with empty data
    - Test specific filtering examples
    - Test case-insensitive matching
    - _Requirements: 1.1.3, 1.1.4, 1.1.5_

- [x] 5. Checkpoint - Ensure Gemini integration tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [x] 6. Implement Chunk Processor
  - [ ] 6.1 Create ChunkProcessor class in `app/services/chunk_processor.py`
    - Initialize with threshold, chunk size, overlap configuration
    - Implement `needs_chunking()` method with word count check
    - Implement `chunk_text()` method with sentence boundary detection
    - Implement `_split_at_sentence_boundary()` helper
    - Handle edge cases: empty text, no sentence boundaries
    - Preserve speaker context in meeting transcripts
    - Add chunk metadata (index, total, overlap info)
    - _Requirements: 2.1.1, 2.1.2, 2.1.4, 2.1.5, TR-2_
  
  - [x] 6.2 Write property test for chunking threshold detection
    - **Property 6: Chunking threshold detection**
    - **Validates: Requirements 2.1.1**
    - Test that texts >3000 words return True, others False
    - Generate random texts of varying lengths
    - Run 100 iterations
  
  - [x] 6.3 Write property test for chunk size bounds
    - **Property 7: Chunk size bounds**
    - **Validates: Requirements 2.1.2**
    - Test that all chunks (except last) are 1000-1500 words
    - Generate random texts >3000 words
    - Run 100 iterations
  
  - [x] 6.4 Write property test for sentence boundary preservation
    - **Property 8: Sentence boundary preservation**
    - **Validates: Requirements 2.1.4**
    - Test that chunk boundaries end with sentence punctuation
    - Generate random texts with sentences
    - Run 100 iterations
  
  - [x] 6.5 Write property test for chunk overlap consistency
    - **Property 9: Chunk overlap consistency**
    - **Validates: Requirements 2.1.5**
    - Test that adjacent chunks have 100-word overlap
    - Generate random texts >3000 words
    - Run 100 iterations
  
  - [x] 6.6 Write unit tests for Chunk Processor
    - Test exact threshold boundary (3000 words)
    - Test empty text
    - Test single sentence
    - Test text with no sentence boundaries
    - Test speaker context preservation
    - _Requirements: 2.1.1, 2.1.2, 2.1.4, 2.1.5, TR-2_

- [x] 7. Implement Ingestion Tracker
  - [x] 7.1 Create IngestionTracker class in `app/services/ingestion_tracker.py`
    - Initialize with sample count configuration
    - Implement `start_tracking()` to create tracking session
    - Implement `track_email()`, `track_slack_message()`, `track_meeting()`, `track_chunk()` methods
    - Implement `get_summary()` to build IngestionSummary
    - Implement `_select_samples()` with random sampling
    - Add thread-safe storage with threading.Lock
    - Add session expiration and cleanup (1 hour TTL)
    - Track processing time from start to summary
    - _Requirements: 3.1.1, 3.1.2, 3.1.3, 3.1.4, 3.1.5, 3.2.1, 3.2.2, 3.2.3, 3.2.4, TR-3_
  
  - [x] 7.2 Write property test for source counting accuracy
    - **Property 13: Source counting accuracy**
    - **Validates: Requirements 3.1.1, 3.1.2, 3.1.3, 3.1.4**
    - Test that all counts match actual items processed
    - Generate random sets of emails, slack messages, meetings
    - Run 100 iterations
  
  - [x] 7.3 Write property test for sample size bounds
    - **Property 14: Sample size bounds**
    - **Validates: Requirements 3.2.1**
    - Test that samples are 3-5 items (or all if fewer available)
    - Generate random data sets of varying sizes
    - Run 100 iterations
  
  - [x] 7.4 Write property test for sample metadata completeness
    - **Property 15: Sample metadata completeness**
    - **Validates: Requirements 3.2.2, 3.2.3, 3.2.4**
    - Test that each sample has required fields for its type
    - Generate random samples of each type
    - Run 100 iterations
  
  - [x] 7.5 Write unit tests for Ingestion Tracker
    - Test thread safety with concurrent tracking
    - Test session expiration and cleanup
    - Test with empty data
    - Test sample selection randomness
    - _Requirements: 3.1.1, 3.1.2, 3.1.3, 3.1.4, TR-3_

- [x] 8. Implement Aggregator
  - [x] 8.1 Create Aggregator class in `app/services/aggregator.py`
    - Implement `aggregate_chunks()` method
    - Implement `_deduplicate_requirements()` with fuzzy matching (>80% similarity)
    - Implement `_merge_decisions()` keeping latest timestamp
    - Implement `_merge_stakeholders()` with set deduplication
    - Implement `_merge_timelines()` resolving conflicts
    - Use `difflib.SequenceMatcher` for similarity
    - Add logging for deduplication statistics
    - _Requirements: 2.2.2_
  
  - [x] 8.2 Write property test for deduplication effectiveness
    - **Property 11: Deduplication effectiveness**
    - **Validates: Requirements 2.2.2**
    - Test that duplicate requirements are removed
    - Generate chunk results with intentional duplicates
    - Run 100 iterations
  
  - [x] 8.3 Write property test for extraction completeness
    - **Property 10: Extraction completeness**
    - **Validates: Requirements 2.2.1**
    - Test that aggregated results have all four required fields
    - Generate random chunk results
    - Run 100 iterations
  
  - [x] 8.4 Write unit tests for Aggregator
    - Test with empty chunk results
    - Test with single chunk
    - Test specific deduplication examples
    - Test timeline conflict resolution
    - _Requirements: 2.2.2_

- [x] 9. Checkpoint - Ensure core services tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [-] 10. Implement Context Router and endpoint
  - [x] 10.1 Create context router in `app/routers/context.py`
    - Define `/generate_brd_with_context` POST endpoint
    - Inject dependencies: GeminiService, ConstraintApplier, ChunkProcessor, IngestionTracker, Aggregator
    - Implement request validation
    - Implement full processing flow:
      1. Generate constraints from instructions (if provided)
      2. Apply constraints to filter data
      3. Start ingestion tracking
      4. Process each data source (check chunking, extract)
      5. Aggregate chunk results
      6. Generate BRD
      7. Run alignment analysis
      8. Build response with ingestion summary
    - Add error handling for each step
    - Add request ID logging
    - _Requirements: 1.1.6, 2.2.3, 2.2.4, 3.1.5, TR-4_
  
  - [ ] 10.2 Write property test for instruction acceptance
    - **Property 1: Instruction acceptance**
    - **Validates: Requirements 1.1.1**
    - Test that any valid string is accepted as instructions
    - Generate random instruction strings
    - Run 100 iterations
  
  - [ ] 10.3 Write unit tests for context endpoint
    - Test request validation
    - Test response format
    - Test with no instructions (backward compatible)
    - Test with instructions
    - Test error handling (Gemini failure, chunking failure)
    - Mock all service dependencies
    - _Requirements: TR-4_

- [x] 11. Update configuration and dependencies
  - [x] 11.1 Update `app/config.py` with new settings
    - Add Gemini configuration (API key, model, timeout, retries)
    - Add chunking configuration (threshold, sizes, overlap)
    - Add tracking configuration (sample count, TTL)
    - _Requirements: TR-1, TR-2, TR-3, NFR-3_
  
  - [x] 11.2 Create dependency injection in `app/dependencies.py`
    - Add `get_gemini_service()` factory
    - Add `get_chunk_processor()` factory
    - Add `get_ingestion_tracker()` factory
    - Add `get_constraint_applier()` factory
    - Add `get_aggregator()` factory
    - Use `@lru_cache()` for singleton instances
    - _Requirements: NFR-1_
  
  - [x] 11.3 Update `main.py` to register context router
    - Import and include context router
    - Ensure backward compatibility with existing routes
    - _Requirements: TR-4_

- [x] 12. Add error handling and logging
  - [x] 12.1 Define custom exceptions in `app/utils/exceptions.py`
    - Add GeminiAPIError, GeminiTimeoutError, GeminiRateLimitError
    - Add ConstraintValidationError
    - Add ChunkingError, TextTooShortError
    - Add TrackingSessionNotFoundError, TrackingStorageError
    - Add AggregationError, EmptyChunkResultsError
    - _Requirements: TR-5_
  
  - [x] 12.2 Add structured logging throughout services
    - Log all Gemini API calls with request ID
    - Log chunking operations with metrics
    - Log ingestion counts and processing times
    - Use JSON format for structured logs
    - Never log sensitive data (API keys, full content)
    - _Requirements: TR-6, NFR-3_
  
  - [x] 12.3 Write unit tests for error handling
    - Test each error type is raised correctly
    - Test fallback behaviors
    - Test error logging
    - _Requirements: TR-5_

- [x] 13. Add security measures
  - [x] 13.1 Implement input validation
    - Validate instructions max length (2000 chars)
    - Sanitize instructions (remove control characters)
    - Validate data source structure
    - Validate max text length per item (100,000 chars)
    - Validate max total items (1000 per request)
    - _Requirements: NFR-4_
  
  - [x] 13.2 Add rate limiting to context endpoint
    - Use slowapi library
    - Set limit: 10 requests/minute per IP
    - _Requirements: NFR-4_
  
  - [x] 13.3 Write unit tests for security measures
    - Test input validation rejects invalid inputs
    - Test rate limiting (mock)
    - Test sanitization removes control characters
    - _Requirements: NFR-4_

- [x] 14. Checkpoint - Ensure integration tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [x] 15. Write integration tests
  - [x] 15.1 Write end-to-end test: Full flow with instructions
    - Test: Request with instructions → constraints → filtering → BRD
    - Mock Gemini API and Groq API
    - Verify response includes ingestion_summary
    - _Requirements: 1.1.6, 3.1.5_
  
  - [x] 15.2 Write end-to-end test: Large meeting with chunking
    - Test: Meeting >3000 words → chunking → aggregation → BRD
    - Verify chunks are created and tracked
    - Verify aggregation combines results
    - _Requirements: 2.1.1, 2.2.2, 2.2.5_
  
  - [x] 15.3 Write end-to-end test: Multiple data sources with tracking
    - Test: Emails + Slack + Meetings → tracking → summary
    - Verify all counts are accurate
    - Verify samples are included
    - _Requirements: 3.1.1, 3.1.2, 3.1.3, 3.2.1_
  
  - [x] 15.4 Write end-to-end test: Gemini failure fallback
    - Test: Gemini API fails → fallback → successful BRD
    - Mock Gemini API to fail
    - Verify processing continues without constraints
    - _Requirements: 1.2.5_
  
  - [x] 15.5 Write backward compatibility test
    - Test: Old endpoint `/generate_brd_with_alignment` still works
    - Verify response format unchanged
    - Verify behavior unchanged
    - _Requirements: TR-4_

- [x] 16. Add documentation
  - [x] 16.1 Add docstrings to all classes and methods
    - Follow Google docstring format
    - Include parameter types and return types
    - Include usage examples for complex methods
    - _Requirements: NFR-3_
  
  - [x] 16.2 Create API documentation examples
    - Add example requests for context endpoint
    - Add example responses with ingestion_summary
    - Document error responses
    - _Requirements: NFR-3_
  
  - [x] 16.3 Update README with new features
    - Document User Instruction Layer
    - Document Large Data Handling
    - Document Ingestion Transparency
    - Add configuration instructions
    - Add example usage
    - _Requirements: NFR-3_

- [x] 17. Performance optimization and benchmarking
  - [x] 17.1 Write performance benchmarks
    - Benchmark Gemini API call (mocked, < 2s)
    - Benchmark chunking 10,000 words (< 1s)
    - Benchmark tracking overhead (< 100ms)
    - Benchmark full request (< 5s excluding LLM)
    - _Requirements: TR-7_
  
  - [x] 17.2 Optimize chunking for large texts
    - Profile chunking performance
    - Optimize sentence boundary detection
    - Consider async processing for multiple meetings
    - _Requirements: TR-7, NFR-5_
  
  - [x] 17.3 Implement tracking session cleanup
    - Add background task to clean expired sessions
    - Run cleanup every 10 minutes
    - Remove sessions older than 1 hour
    - _Requirements: TR-3, NFR-5_

- [x] 18. Final checkpoint - Full system verification
  - Ensure all tests pass (unit, property, integration)
  - Verify backward compatibility
  - Verify all requirements are met
  - Ask the user if questions arise.

---

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation
- Property tests validate universal correctness properties (100 iterations each)
- Unit tests validate specific examples and edge cases
- Integration tests verify end-to-end flows
- All services use dependency injection for testability
- Backward compatibility is maintained throughout

---

**Document Version**: 1.0  
**Created**: 2024-02-21  
**Status**: Ready for Execution

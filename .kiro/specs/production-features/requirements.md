# Production Features - Requirements Document

## Project Overview

Extend ReqMind AI backend with three production-ready features:
1. User Instruction Layer (Gemini Integration)
2. Large Data Handling (Meeting Chunking)
3. Ingestion Transparency (Explainability)

## Current System Context

**Existing Backend**:
- Framework: FastAPI
- LLM: Groq (llama-3.3-70b-versatile)
- Features: Multi-channel ingestion, Dataset support, BRD generation, Alignment Intelligence
- Main Endpoint: `POST /generate_brd_with_alignment`

**Tech Stack**:
- Python 3.8+
- FastAPI
- Groq API
- Pydantic for data models

---

## Feature 1: User Instruction Layer (Gemini Integration)

### User Story 1.1: Provide Project Instructions
**As a** project manager  
**I want to** provide natural language instructions before BRD generation  
**So that** the system focuses on relevant information and ignores noise

**Acceptance Criteria**:
- 1.1.1: System accepts natural language instructions via API
- 1.1.2: Instructions are converted to structured constraints using Gemini API
- 1.1.3: Constraints are applied during data filtering
- 1.1.4: Excluded topics are removed from processing
- 1.1.5: Scoped content is prioritized
- 1.1.6: Refined data is passed to existing Groq pipeline

### User Story 1.2: Structured Constraint Generation
**As a** system  
**I want to** convert natural language instructions to structured constraints  
**So that** I can programmatically filter and prioritize data

**Acceptance Criteria**:
- 1.2.1: Gemini API converts instructions to JSON format
- 1.2.2: JSON includes: scope, exclude_topics, priority_focus, deadline_override
- 1.2.3: Constraints are validated before application
- 1.2.4: System handles Gemini API failures gracefully
- 1.2.5: Falls back to unfiltered processing if Gemini fails

### Example Instructions
```
- "Focus only on Phase 1"
- "Ignore marketing discussions"
- "Client deadline is June"
- "Prioritize mobile features"
- "Exclude internal team discussions"
```

### API Specification

**Endpoint**: `POST /generate_brd_with_context`

**Request**:
```json
{
  "instructions": "Focus only on MVP and ignore internal discussions",
  "data": {
    "emails": [],
    "slack_messages": [],
    "meetings": []
  }
}
```

**Gemini Constraint Format**:
```json
{
  "scope": "MVP features only",
  "exclude_topics": ["internal discussions", "team meetings"],
  "priority_focus": "core functionality",
  "deadline_override": ""
}
```

---

## Feature 2: Large Data Handling (Meeting Chunking)

### User Story 2.1: Process Large Meetings
**As a** system  
**I want to** chunk large meeting transcripts  
**So that** I can process meetings longer than 3 hours without hitting token limits

**Acceptance Criteria**:
- 2.1.1: System detects when text exceeds 3000 words
- 2.1.2: Text is split into chunks of 1000-1500 words
- 2.1.3: Each chunk is processed independently by Groq
- 2.1.4: Chunks maintain context boundaries (don't split mid-sentence)
- 2.1.5: Chunk overlap is maintained for context continuity

### User Story 2.2: Extract and Aggregate Results
**As a** system  
**I want to** extract structured data from each chunk and aggregate  
**So that** no information is lost during chunking

**Acceptance Criteria**:
- 2.2.1: Each chunk extracts: requirements, decisions, stakeholders, timelines
- 2.2.2: Duplicate information is deduplicated during aggregation
- 2.2.3: Aggregated results are sent to BRD generator
- 2.2.4: Aggregated results are sent to Alignment Engine
- 2.2.5: Chunk count is tracked for transparency

### Chunking Strategy
- **Threshold**: 3000 words
- **Chunk Size**: 1000-1500 words
- **Overlap**: 100 words between chunks
- **Boundary**: Split at sentence boundaries
- **Extraction per Chunk**: requirements, decisions, stakeholders, timelines

---

## Feature 3: Ingestion Transparency (Explainability)

### User Story 3.1: Track Data Sources
**As a** user  
**I want to** see what data was used in the analysis  
**So that** I can verify the BRD is based on relevant sources

**Acceptance Criteria**:
- 3.1.1: System counts emails used in analysis
- 3.1.2: System counts Slack messages used
- 3.1.3: System counts meetings used
- 3.1.4: System tracks total chunks processed
- 3.1.5: Response includes ingestion summary

### User Story 3.2: Provide Sample Sources
**As a** user  
**I want to** see sample sources that were analyzed  
**So that** I can understand the basis of the BRD

**Acceptance Criteria**:
- 3.2.1: System provides 3-5 sample sources
- 3.2.2: Email samples include: subject, date
- 3.2.3: Meeting samples include: timestamp, topic
- 3.2.4: Slack samples include: channel, user, timestamp
- 3.2.5: Samples are representative of the dataset

### Response Schema

```json
{
  "brd": {...},
  "alignment_analysis": {
    "alignment_score": 78,
    "risk_level": "MEDIUM",
    "conflicts": [...],
    "timeline_mismatches": [...]
  },
  "ingestion_summary": {
    "emails_used": 12,
    "slack_messages_used": 45,
    "meetings_used": 3,
    "total_chunks_processed": 8,
    "total_words_processed": 15420,
    "processing_time_seconds": 12.5,
    "sample_sources": [
      {
        "type": "email",
        "subject": "Deadline discussion",
        "date": "2024-02-12",
        "sender": "john.pm@company.com"
      },
      {
        "type": "meeting",
        "timestamp": "01:15:30",
        "topic": "API dependency risk",
        "speakers": ["PM", "Tech Lead"]
      },
      {
        "type": "slack",
        "channel": "#project-alpha",
        "user": "sarah.dev",
        "timestamp": "2024-02-15 14:30",
        "preview": "We need to prioritize mobile..."
      }
    ]
  }
}
```

---

## System Flow

```
1. User Instructions
   ↓
2. Gemini API → Structured Constraints
   ↓
3. Data Collection (emails, slack, meetings)
   ↓
4. Apply Constraints (filter, prioritize)
   ↓
5. Ingestion Tracker (start counting)
   ↓
6. Chunk Processor (if text > 3000 words)
   ↓
7. Groq Extraction (per chunk or full text)
   ↓
8. Aggregation (combine chunk results)
   ↓
9. BRD Generator
   ↓
10. Alignment Engine
   ↓
11. Response with Ingestion Summary
```

---

## Technical Requirements

### TR-1: Gemini Integration
- Use Google Gemini API (gemini-pro model)
- Environment variable: `GEMINI_API_KEY`
- Timeout: 10 seconds
- Retry logic: 2 retries with exponential backoff
- Fallback: Continue without constraints if Gemini fails

### TR-2: Chunking Service
- Word count threshold: 3000 words
- Chunk size: 1000-1500 words
- Overlap: 100 words
- Split at sentence boundaries
- Maintain speaker context in meetings

### TR-3: Ingestion Tracker
- Track counts: emails, slack messages, meetings, chunks
- Store sample metadata: 3-5 samples per type
- Calculate processing time
- Thread-safe for concurrent requests

### TR-4: Backward Compatibility
- Existing `/generate_brd_with_alignment` endpoint unchanged
- New endpoint: `/generate_brd_with_context`
- Both endpoints return same BRD structure
- New endpoint adds `ingestion_summary` field

### TR-5: Error Handling
- Gemini API failure: Log error, continue without constraints
- Chunking failure: Process as single text
- Tracking failure: Return response without summary
- All errors logged with request ID

### TR-6: Logging
- Log all Gemini API calls
- Log chunking operations
- Log ingestion counts
- Log processing times
- Use structured logging (JSON format)

### TR-7: Performance
- Gemini API call: < 2 seconds
- Chunking: < 1 second per 10,000 words
- Tracking overhead: < 100ms
- Total added latency: < 3 seconds

---

## Non-Functional Requirements

### NFR-1: Modularity
- Each feature in separate service module
- Services are independently testable
- Clear interfaces between services

### NFR-2: Testability
- Unit tests for each service
- Integration tests for new endpoint
- Mock Gemini API for testing
- Test chunking with various sizes

### NFR-3: Maintainability
- Clear folder structure
- Comprehensive docstrings
- Type hints throughout
- Configuration via environment variables

### NFR-4: Security
- Validate all user inputs
- Sanitize instructions before sending to Gemini
- No sensitive data in logs
- API key stored securely

### NFR-5: Scalability
- Chunking handles meetings up to 10 hours
- Tracking handles 1000+ sources
- Concurrent request support
- Stateless services

---

## Folder Structure

```
app/
├── services/
│   ├── gemini_service.py          # NEW: Gemini integration
│   ├── chunk_processor.py         # NEW: Chunking logic
│   ├── ingestion_tracker.py       # NEW: Tracking service
│   ├── constraint_applier.py      # NEW: Apply constraints
│   ├── brd_generator.py           # EXISTING
│   ├── alignment_intelligence.py  # EXISTING
│   └── multi_channel_ingestion.py # EXISTING
├── models/
│   ├── context_request.py         # NEW: Request models
│   ├── constraints.py             # NEW: Constraint models
│   ├── ingestion_summary.py       # NEW: Summary models
│   ├── request.py                 # EXISTING
│   └── response.py                # EXISTING (update)
├── routers/
│   ├── context.py                 # NEW: Context endpoint
│   ├── brd.py                     # EXISTING
│   └── dataset.py                 # EXISTING
└── utils/
    ├── text_splitter.py           # NEW: Text chunking utility
    └── exceptions.py              # EXISTING
```

---

## Configuration

### Environment Variables

```env
# Existing
OPENAI_API_KEY=gsk_...
OPENAI_MODEL=llama-3.3-70b-versatile
OPENAI_BASE_URL=https://api.groq.com/openai/v1

# New
GEMINI_API_KEY=AIza...
GEMINI_MODEL=gemini-pro
GEMINI_TIMEOUT=10

# Chunking
CHUNK_THRESHOLD_WORDS=3000
CHUNK_SIZE_MIN=1000
CHUNK_SIZE_MAX=1500
CHUNK_OVERLAP=100

# Tracking
SAMPLE_SOURCES_COUNT=5
```

---

## Testing Requirements

### Test Cases

**Feature 1: Gemini Integration**
- TC-1.1: Valid instructions → structured constraints
- TC-1.2: Empty instructions → no constraints
- TC-1.3: Gemini API failure → fallback behavior
- TC-1.4: Invalid constraints → validation error
- TC-1.5: Constraints applied correctly to data

**Feature 2: Chunking**
- TC-2.1: Text < 3000 words → no chunking
- TC-2.2: Text > 3000 words → chunked
- TC-2.3: Chunks are 1000-1500 words
- TC-2.4: Overlap maintained
- TC-2.5: Aggregation deduplicates correctly

**Feature 3: Tracking**
- TC-3.1: Counts are accurate
- TC-3.2: Samples are representative
- TC-3.3: Processing time tracked
- TC-3.4: Thread-safe operation
- TC-3.5: Summary in response

---

## Success Criteria

1. ✅ New endpoint `/generate_brd_with_context` works
2. ✅ Gemini integration converts instructions to constraints
3. ✅ Constraints filter data correctly
4. ✅ Large meetings (>3000 words) are chunked
5. ✅ Chunk results are aggregated correctly
6. ✅ Ingestion summary included in response
7. ✅ Backward compatibility maintained
8. ✅ All tests pass
9. ✅ Performance requirements met
10. ✅ Documentation complete

---

## Example Requests

### Example 1: With Instructions

```bash
curl -X POST "http://127.0.0.1:8000/generate_brd_with_context" \
  -H "Content-Type: application/json" \
  -d '{
    "instructions": "Focus only on MVP features and ignore marketing discussions. Client deadline is June 2024.",
    "data": {
      "emails": [
        {"subject": "MVP scope", "body": "We need core features..."},
        {"subject": "Marketing plan", "body": "Social media strategy..."}
      ],
      "slack_messages": [],
      "meetings": []
    }
  }'
```

### Example 2: Large Meeting

```bash
curl -X POST "http://127.0.0.1:8000/generate_brd_with_context" \
  -H "Content-Type: application/json" \
  -d '{
    "instructions": "Extract all technical requirements",
    "data": {
      "emails": [],
      "slack_messages": [],
      "meetings": [
        {"transcript": "... 5000 word transcript ..."}
      ]
    }
  }'
```

### Example 3: No Instructions (Backward Compatible)

```bash
curl -X POST "http://127.0.0.1:8000/generate_brd_with_context" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "emails": [...],
      "slack_messages": [...],
      "meetings": [...]
    }
  }'
```

---

## Dependencies

### New Dependencies
```
google-generativeai==0.3.2  # Gemini API
tiktoken==0.5.2             # Token counting
```

### Existing Dependencies
```
fastapi==0.109.0
openai==1.10.0
pydantic==2.5.3
```

---

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Gemini API rate limits | High | Implement caching, retry logic |
| Chunking loses context | Medium | Use overlap, maintain speaker info |
| Performance degradation | Medium | Async processing, optimize chunking |
| Gemini API costs | Low | Monitor usage, set limits |
| Breaking changes | High | Maintain backward compatibility |

---

## Timeline Estimate

- Feature 1 (Gemini): 2-3 days
- Feature 2 (Chunking): 2-3 days
- Feature 3 (Tracking): 1-2 days
- Testing & Integration: 2 days
- Documentation: 1 day

**Total**: 8-11 days

---

## Acceptance Checklist

- [ ] Gemini service implemented
- [ ] Chunk processor implemented
- [ ] Ingestion tracker implemented
- [ ] New endpoint created
- [ ] Response schema updated
- [ ] Backward compatibility verified
- [ ] Unit tests written (>80% coverage)
- [ ] Integration tests written
- [ ] Error handling implemented
- [ ] Logging added
- [ ] Documentation updated
- [ ] Example requests tested
- [ ] Performance benchmarked
- [ ] Security review completed
- [ ] Code review completed

---

**Document Version**: 1.0  
**Created**: 2024-02-21  
**Status**: Draft - Ready for Review

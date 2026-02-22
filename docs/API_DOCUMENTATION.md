# API Documentation - Production Features

## Overview

This document provides comprehensive API documentation for the new production features:
1. **User Instruction Layer**: Natural language instructions for data filtering
2. **Large Data Handling**: Automatic chunking of large texts
3. **Ingestion Transparency**: Detailed tracking of data sources

---

## Endpoint: Generate BRD with Context

### POST `/generate_brd_with_context`

Generate a Business Requirements Document with context-aware processing including user instructions, automatic chunking for large data, and ingestion transparency.

**Rate Limit**: 10 requests per minute per IP address

---

## Request Format

### Request Body

```json
{
  "instructions": "string (optional, max 2000 chars)",
  "data": {
    "emails": [
      {
        "subject": "string",
        "body": "string",
        "sender": "string (optional)",
        "date": "string (optional)"
      }
    ],
    "slack_messages": [
      {
        "channel": "string",
        "user": "string",
        "text": "string",
        "timestamp": "string (optional)"
      }
    ],
    "meetings": [
      {
        "transcript": "string",
        "topic": "string (optional)",
        "speakers": ["string"],
        "timestamp": "string (optional)"
      }
    ]
  }
}
```

### Field Descriptions

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `instructions` | string | No | Natural language instructions for filtering and prioritizing data (max 2000 characters) |
| `data` | object | Yes | Multi-channel ingestion data |
| `data.emails` | array | No | List of email messages (max 100,000 chars per email) |
| `data.slack_messages` | array | No | List of Slack messages (max 100,000 chars per message) |
| `data.meetings` | array | No | List of meeting transcripts (max 100,000 chars per transcript) |

**Validation Rules**:
- Maximum 1000 total items per request
- Maximum 2000 characters for instructions
- Maximum 100,000 characters per text field
- Control characters are automatically sanitized from instructions

---

## Response Format

### Success Response (200 OK)

```json
{
  "brd": {
    "projectName": "string",
    "executiveSummary": "string",
    "businessObjectives": ["string"],
    "requirements": [
      {
        "id": "string",
        "description": "string",
        "priority": "string",
        "category": "string"
      }
    ],
    "stakeholders": [
      {
        "name": "string",
        "role": "string",
        "responsibilities": "string"
      }
    ],
    "timeline": {
      "phases": [
        {
          "name": "string",
          "duration": "string",
          "deliverables": ["string"]
        }
      ]
    },
    "risks": [
      {
        "description": "string",
        "impact": "string",
        "mitigation": "string"
      }
    ]
  },
  "alignment_analysis": {
    "alignment_score": 78.5,
    "risk_level": "MEDIUM",
    "alert": "string",
    "conflicts": [
      {
        "type": "string",
        "description": "string",
        "severity": "string",
        "recommendation": "string"
      }
    ],
    "timeline_mismatches": [
      {
        "description": "string",
        "source": "string"
      }
    ],
    "requirement_volatility": {
      "change_rate": 0.15,
      "stability_score": 85.0
    },
    "stakeholder_agreement_score": 85.0,
    "timeline_consistency_score": 70.0,
    "requirement_stability_score": 80.0,
    "decision_volatility_score": 75.0
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
        "metadata": {
          "subject": "Deadline discussion",
          "date": "2024-02-12",
          "sender": "john.pm@company.com"
        }
      },
      {
        "type": "meeting",
        "metadata": {
          "timestamp": "01:15:30",
          "topic": "API dependency risk",
          "speakers": ["PM", "Tech Lead"]
        }
      },
      {
        "type": "slack",
        "metadata": {
          "channel": "#project-alpha",
          "user": "sarah.dev",
          "timestamp": "2024-02-15 14:30",
          "preview": "We need to prioritize mobile..."
        }
      }
    ]
  }
}
```

### Response Field Descriptions

#### BRD Section
| Field | Type | Description |
|-------|------|-------------|
| `brd.projectName` | string | Name of the project |
| `brd.executiveSummary` | string | High-level project summary |
| `brd.businessObjectives` | array | List of business objectives |
| `brd.requirements` | array | Detailed requirements with priority and category |
| `brd.stakeholders` | array | Project stakeholders with roles |
| `brd.timeline` | object | Project timeline with phases |
| `brd.risks` | array | Identified risks with mitigation strategies |

#### Alignment Analysis Section
| Field | Type | Description |
|-------|------|-------------|
| `alignment_analysis.alignment_score` | number | Overall alignment score (0-100) |
| `alignment_analysis.risk_level` | string | Risk level: HIGH, MEDIUM, or LOW |
| `alignment_analysis.alert` | string | Alert message describing the risk |
| `alignment_analysis.conflicts` | array | Detected conflicts with recommendations |
| `alignment_analysis.timeline_mismatches` | array | Timeline inconsistencies |
| `alignment_analysis.stakeholder_agreement_score` | number | Stakeholder agreement score (0-100) |
| `alignment_analysis.timeline_consistency_score` | number | Timeline consistency score (0-100) |
| `alignment_analysis.requirement_stability_score` | number | Requirement stability score (0-100) |
| `alignment_analysis.decision_volatility_score` | number | Decision volatility score (0-100) |

#### Ingestion Summary Section
| Field | Type | Description |
|-------|------|-------------|
| `ingestion_summary.emails_used` | integer | Number of emails processed |
| `ingestion_summary.slack_messages_used` | integer | Number of Slack messages processed |
| `ingestion_summary.meetings_used` | integer | Number of meetings processed |
| `ingestion_summary.total_chunks_processed` | integer | Total chunks created from large texts |
| `ingestion_summary.total_words_processed` | integer | Total word count across all sources |
| `ingestion_summary.processing_time_seconds` | number | Time taken to process all sources |
| `ingestion_summary.sample_sources` | array | 3-5 representative sample sources |

---

## Example Requests

### Example 1: Basic Request with Instructions

Filter data to focus on MVP features and exclude marketing discussions.

**Request:**
```bash
curl -X POST "http://localhost:8000/generate_brd_with_context" \
  -H "Content-Type: application/json" \
  -d '{
    "instructions": "Focus only on MVP features and ignore marketing discussions. Client deadline is June 2024.",
    "data": {
      "emails": [
        {
          "subject": "MVP scope discussion",
          "body": "We need to focus on core features for the MVP release. Authentication, user profiles, and basic search are essential.",
          "sender": "pm@company.com",
          "date": "2024-02-15"
        },
        {
          "subject": "Marketing campaign ideas",
          "body": "Let'\''s plan a social media campaign for launch. We should focus on Instagram and Twitter.",
          "sender": "marketing@company.com",
          "date": "2024-02-16"
        }
      ],
      "slack_messages": [],
      "meetings": []
    }
  }'
```

**Expected Behavior:**
- Gemini converts instructions to constraints: `{"scope": "MVP features", "exclude_topics": ["marketing"], "deadline_override": "June 2024"}`
- Marketing email is filtered out
- Only MVP-related email is processed
- BRD focuses on core features

**Response:** (200 OK)
```json
{
  "brd": {
    "projectName": "MVP scope discussion",
    "executiveSummary": "Focus on core MVP features including authentication, user profiles, and basic search functionality.",
    "businessObjectives": [
      "Deliver MVP by June 2024",
      "Implement core user features"
    ],
    "requirements": [
      {
        "id": "REQ-001",
        "description": "User authentication system",
        "priority": "HIGH",
        "category": "Security"
      },
      {
        "id": "REQ-002",
        "description": "User profile management",
        "priority": "HIGH",
        "category": "User Management"
      },
      {
        "id": "REQ-003",
        "description": "Basic search functionality",
        "priority": "MEDIUM",
        "category": "Features"
      }
    ],
    "stakeholders": [
      {
        "name": "Product Manager",
        "role": "pm@company.com",
        "responsibilities": "Define MVP scope and priorities"
      }
    ],
    "timeline": {
      "phases": [
        {
          "name": "MVP Development",
          "duration": "4 months",
          "deliverables": ["Authentication", "User Profiles", "Search"]
        }
      ]
    },
    "risks": []
  },
  "alignment_analysis": {
    "alignment_score": 92.0,
    "risk_level": "LOW",
    "alert": "Good alignment detected",
    "conflicts": [],
    "timeline_mismatches": [],
    "requirement_volatility": {
      "change_rate": 0.05,
      "stability_score": 95.0
    },
    "stakeholder_agreement_score": 90.0,
    "timeline_consistency_score": 95.0,
    "requirement_stability_score": 92.0,
    "decision_volatility_score": 88.0
  },
  "ingestion_summary": {
    "emails_used": 1,
    "slack_messages_used": 0,
    "meetings_used": 0,
    "total_chunks_processed": 0,
    "total_words_processed": 45,
    "processing_time_seconds": 2.3,
    "sample_sources": [
      {
        "type": "email",
        "metadata": {
          "subject": "MVP scope discussion",
          "date": "2024-02-15",
          "sender": "pm@company.com"
        }
      }
    ]
  }
}
```

---

### Example 2: Large Meeting with Automatic Chunking

Process a long meeting transcript that exceeds 3000 words.

**Request:**
```bash
curl -X POST "http://localhost:8000/generate_brd_with_context" \
  -H "Content-Type: application/json" \
  -d '{
    "instructions": "Extract all technical requirements and decisions",
    "data": {
      "emails": [],
      "slack_messages": [],
      "meetings": [
        {
          "transcript": "... [5000 word meeting transcript] ...",
          "topic": "Technical Architecture Review",
          "speakers": ["Tech Lead", "Senior Engineer", "Product Manager"],
          "timestamp": "2024-02-20 14:00"
        }
      ]
    }
  }'
```

**Expected Behavior:**
- Meeting transcript exceeds 3000 words
- System automatically chunks into 4 chunks (~1250 words each)
- Each chunk is tracked separately
- Results are aggregated before BRD generation
- `total_chunks_processed` = 4 in response

**Response:** (200 OK)
```json
{
  "brd": {
    "projectName": "Technical Architecture Review",
    "executiveSummary": "Comprehensive technical architecture decisions covering database selection, API design, and deployment strategy.",
    "businessObjectives": ["..."],
    "requirements": ["..."],
    "stakeholders": ["..."],
    "timeline": {"..."},
    "risks": ["..."]
  },
  "alignment_analysis": {
    "alignment_score": 78.5,
    "risk_level": "MEDIUM",
    "alert": "Some technical decisions need clarification",
    "conflicts": [
      {
        "type": "technical",
        "description": "Database choice discussed but not finalized",
        "severity": "MEDIUM",
        "recommendation": "Schedule follow-up meeting to finalize database selection"
      }
    ],
    "timeline_mismatches": [],
    "requirement_volatility": {"..."},
    "stakeholder_agreement_score": 75.0,
    "timeline_consistency_score": 80.0,
    "requirement_stability_score": 78.0,
    "decision_volatility_score": 72.0
  },
  "ingestion_summary": {
    "emails_used": 0,
    "slack_messages_used": 0,
    "meetings_used": 1,
    "total_chunks_processed": 4,
    "total_words_processed": 5000,
    "processing_time_seconds": 8.7,
    "sample_sources": [
      {
        "type": "meeting",
        "metadata": {
          "timestamp": "2024-02-20 14:00",
          "topic": "Technical Architecture Review",
          "speakers": ["Tech Lead", "Senior Engineer", "Product Manager"]
        }
      }
    ]
  }
}
```

---

### Example 3: Multiple Data Sources

Process data from emails, Slack, and meetings together.

**Request:**
```bash
curl -X POST "http://localhost:8000/generate_brd_with_context" \
  -H "Content-Type: application/json" \
  -d '{
    "instructions": "Prioritize mobile features",
    "data": {
      "emails": [
        {
          "subject": "Mobile app requirements",
          "body": "Users need offline mode and push notifications",
          "sender": "pm@company.com",
          "date": "2024-02-10"
        }
      ],
      "slack_messages": [
        {
          "channel": "#mobile-dev",
          "user": "sarah.dev",
          "text": "iOS app should support dark mode",
          "timestamp": "2024-02-12 10:30"
        },
        {
          "channel": "#mobile-dev",
          "user": "john.designer",
          "text": "Android app needs material design",
          "timestamp": "2024-02-12 11:15"
        }
      ],
      "meetings": [
        {
          "transcript": "Discussion about mobile platform priorities...",
          "topic": "Mobile Strategy",
          "speakers": ["PM", "Mobile Lead"],
          "timestamp": "2024-02-15 14:00"
        }
      ]
    }
  }'
```

**Expected Behavior:**
- All three data sources are processed
- Mobile-related content is prioritized
- Ingestion summary shows counts for all source types
- Sample sources include examples from each type

**Response:** (200 OK)
```json
{
  "brd": {
    "projectName": "Mobile app requirements",
    "executiveSummary": "Mobile application development focusing on offline capabilities, push notifications, and platform-specific design.",
    "businessObjectives": ["..."],
    "requirements": ["..."],
    "stakeholders": ["..."],
    "timeline": {"..."},
    "risks": ["..."]
  },
  "alignment_analysis": {
    "alignment_score": 85.0,
    "risk_level": "LOW",
    "alert": "Good alignment across all channels",
    "conflicts": [],
    "timeline_mismatches": [],
    "requirement_volatility": {"..."},
    "stakeholder_agreement_score": 88.0,
    "timeline_consistency_score": 82.0,
    "requirement_stability_score": 85.0,
    "decision_volatility_score": 80.0
  },
  "ingestion_summary": {
    "emails_used": 1,
    "slack_messages_used": 2,
    "meetings_used": 1,
    "total_chunks_processed": 0,
    "total_words_processed": 250,
    "processing_time_seconds": 3.2,
    "sample_sources": [
      {
        "type": "email",
        "metadata": {
          "subject": "Mobile app requirements",
          "date": "2024-02-10",
          "sender": "pm@company.com"
        }
      },
      {
        "type": "slack",
        "metadata": {
          "channel": "#mobile-dev",
          "user": "sarah.dev",
          "timestamp": "2024-02-12 10:30",
          "preview": "iOS app should support dark mode"
        }
      },
      {
        "type": "meeting",
        "metadata": {
          "timestamp": "2024-02-15 14:00",
          "topic": "Mobile Strategy",
          "speakers": ["PM", "Mobile Lead"]
        }
      }
    ]
  }
}
```

---

### Example 4: No Instructions (Backward Compatible)

Process data without instructions - behaves like standard BRD generation.

**Request:**
```bash
curl -X POST "http://localhost:8000/generate_brd_with_context" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "emails": [
        {
          "subject": "Project kickoff",
          "body": "Let'\''s start the new project next week",
          "sender": "pm@company.com",
          "date": "2024-02-15"
        }
      ],
      "slack_messages": [],
      "meetings": []
    }
  }'
```

**Expected Behavior:**
- No constraint generation (instructions not provided)
- All data is processed without filtering
- Standard BRD generation flow
- Ingestion summary still included

**Response:** (200 OK)
```json
{
  "brd": {"..."},
  "alignment_analysis": {"..."},
  "ingestion_summary": {
    "emails_used": 1,
    "slack_messages_used": 0,
    "meetings_used": 0,
    "total_chunks_processed": 0,
    "total_words_processed": 12,
    "processing_time_seconds": 1.8,
    "sample_sources": [
      {
        "type": "email",
        "metadata": {
          "subject": "Project kickoff",
          "date": "2024-02-15",
          "sender": "pm@company.com"
        }
      }
    ]
  }
}
```

---

## Error Responses

### 400 Bad Request - Validation Error

Returned when request validation fails.

```json
{
  "detail": "Instructions exceed maximum length of 2000 characters"
}
```

**Common Causes:**
- Instructions exceed 2000 characters
- Text field exceeds 100,000 characters
- Total items exceed 1000 per request
- Invalid data structure

---

### 429 Too Many Requests - Rate Limit Exceeded

Returned when rate limit is exceeded (10 requests/minute per IP).

```json
{
  "detail": "Rate limit exceeded: 10 per 1 minute"
}
```

**Solution:** Wait before making additional requests.

---

### 500 Internal Server Error - Processing Failure

Returned when BRD generation fails unexpectedly.

```json
{
  "detail": "An error occurred while generating the BRD: [error details]"
}
```

**Common Causes:**
- OpenAI API failure
- Invalid response from LLM
- Internal processing error

---

### 503 Service Unavailable - External Service Error

Returned when external services (OpenAI, Gemini) are unavailable.

```json
{
  "detail": "OpenAI service is currently unavailable: [error details]"
}
```

**Note:** If Gemini fails, the system falls back to processing without constraints and returns a successful response.

---

## Feature Details

### User Instruction Layer

**How it works:**
1. User provides natural language instructions
2. Instructions are sent to Gemini API
3. Gemini converts to structured constraints:
   - `scope`: Project scope to focus on
   - `exclude_topics`: Topics to exclude
   - `priority_focus`: What to prioritize
   - `deadline_override`: Deadline information
4. Constraints are applied to filter and prioritize data

**Example Instructions:**
- "Focus only on Phase 1"
- "Ignore marketing discussions"
- "Client deadline is June 2024"
- "Prioritize mobile features"
- "Exclude internal team discussions"

**Fallback Behavior:**
If Gemini API fails, the system continues processing without constraints (no filtering applied).

---

### Large Data Handling

**Automatic Chunking:**
- Threshold: 3000 words
- Chunk size: 1000-1500 words
- Overlap: 100 words between chunks
- Boundary: Splits at sentence boundaries

**How it works:**
1. System detects texts exceeding 3000 words
2. Text is split into overlapping chunks
3. Each chunk is tracked separately
4. Results are aggregated before BRD generation

**Tracking:**
- `total_chunks_processed` shows number of chunks created
- Each chunk is counted in ingestion summary

---

### Ingestion Transparency

**What's Tracked:**
- Number of emails, Slack messages, meetings processed
- Total chunks created from large texts
- Total word count across all sources
- Processing time in seconds
- 3-5 representative sample sources

**Sample Source Metadata:**
- **Email**: subject, date, sender
- **Slack**: channel, user, timestamp, preview (first 50 chars)
- **Meeting**: timestamp, topic, speakers list

**Purpose:**
Allows users to verify what data was used in the BRD generation and understand the basis of the analysis.

---

## Best Practices

### 1. Writing Effective Instructions

**Good:**
- "Focus on MVP features and ignore Phase 2 planning"
- "Prioritize security requirements"
- "Exclude marketing and sales discussions"

**Bad:**
- "Do everything" (too vague)
- "Make it perfect" (not actionable)
- Very long instructions (>500 words)

### 2. Handling Large Meetings

- Meetings >3000 words are automatically chunked
- No action needed from client
- Check `total_chunks_processed` to see if chunking occurred

### 3. Rate Limiting

- Limit: 10 requests/minute per IP
- For bulk processing, implement delays between requests
- Consider caching results for repeated requests

### 4. Error Handling

- Always check response status code
- Handle 503 errors with retry logic
- 400 errors indicate client-side issues (fix request)
- 500 errors indicate server issues (contact support)

### 5. Validation

- Keep instructions under 2000 characters
- Keep individual text fields under 100,000 characters
- Keep total items under 1000 per request
- Validate data structure before sending

---

## Migration from Old Endpoint

### Old Endpoint: `/generate_brd_with_alignment`

Still supported for backward compatibility.

### New Endpoint: `/generate_brd_with_context`

Superset of old endpoint functionality.

### Migration Steps:

1. **No Instructions**: Use new endpoint without `instructions` field
   ```json
   {
     "data": { /* same as before */ }
   }
   ```

2. **With Instructions**: Add `instructions` field
   ```json
   {
     "instructions": "Focus on MVP",
     "data": { /* same as before */ }
   }
   ```

3. **Response Handling**: Update to handle `ingestion_summary` field
   ```javascript
   const { brd, alignment_analysis, ingestion_summary } = response;
   ```

---

## Performance Considerations

### Expected Latency

- **Without chunking**: 3-8 seconds
- **With chunking**: 5-15 seconds (depends on chunk count)
- **Gemini constraint generation**: +1-2 seconds

### Optimization Tips

1. **Reduce data size**: Send only relevant data
2. **Use instructions**: Filter data before processing
3. **Batch processing**: Process multiple requests with delays
4. **Cache results**: Cache BRDs for identical inputs

---

## Support

For issues or questions:
- Check error response details
- Review validation rules
- Verify API key configuration
- Contact support with request ID from logs

---

**Document Version**: 1.0  
**Last Updated**: 2024-02-21

# ReqMind AI - Alignment Intelligence Engine

## Overview

The Alignment Intelligence Engine is an advanced feature that evaluates project alignment by detecting conflicts, volatility, and stakeholder disagreement across multi-channel communication. It provides real-time risk assessment and early warning alerts to help teams identify and resolve misalignments before they impact project success.

## Features

### 1. Conflict Detection

The engine automatically detects various types of conflicts:

- **Stakeholder Disagreements**: Identifies when different stakeholders express conflicting views
- **Priority Conflicts**: Detects mismatches in priority assignments (urgent vs. low priority)
- **Scope Conflicts**: Identifies contradictions in project scope (simple vs. complex)
- **Timeline Mismatches**: Finds different deadlines mentioned for the same deliverables

### 2. Alignment Scoring

The system calculates a comprehensive alignment score (0-100) based on:

```
Alignment Score = 100 
  - (conflict_count × 10)
  - (timeline_mismatch × 15)
  - (requirement_changes × 5)
  - (decision_reversals × 8)
```

#### Component Scores

- **Stakeholder Agreement Score**: Measures consensus among stakeholders
- **Timeline Consistency Score**: Evaluates consistency of deadlines across sources
- **Requirement Stability Score**: Tracks how stable requirements are over time
- **Decision Volatility Score**: Measures frequency of decision changes

### 3. Risk Classification

Projects are automatically classified into three risk levels:

| Alignment Score | Risk Level | Alert Message |
|----------------|------------|---------------|
| < 70 | HIGH | "Stakeholder disagreement detected. Immediate review required." |
| 70-85 | MEDIUM | "Potential misalignment detected. Monitor changes closely." |
| > 85 | LOW | "Project alignment is stable. Continue monitoring." |

### 4. Early Warning Alerts

The system generates actionable alerts with:
- Risk level classification
- Specific conflict details
- Source references
- Recommended actions

## API Usage

### Endpoint

**POST** `/generate_brd_with_alignment`

Generates a BRD with comprehensive alignment analysis.

### Request Format

```json
{
  "projectName": "Your Project Name",
  "emailText": "Email communication content",
  "slackText": "Slack messages content",
  "meetingText": "Meeting transcript content"
}
```

### Response Format

```json
{
  "brd": {
    "projectName": "...",
    "executiveSummary": "...",
    "businessObjectives": [...],
    "requirements": [...],
    "stakeholders": [...]
  },
  "alignment_analysis": {
    "alignment_score": 62.0,
    "risk_level": "HIGH",
    "alert": "Stakeholder disagreement detected...",
    "component_scores": {
      "stakeholder_agreement": 80.0,
      "timeline_consistency": 85.0,
      "requirement_stability": 75.0,
      "decision_volatility": 90.0
    },
    "conflicts": [
      {
        "type": "stakeholder_disagreement",
        "description": "...",
        "severity": "high",
        "sources": ["email", "slack"],
        "entities_involved": [...],
        "recommendation": "Schedule alignment meeting..."
      }
    ],
    "timeline_mismatches": [
      {
        "source1": "email",
        "source2": "slack",
        "dates1": ["March 30"],
        "dates2": ["April 10"],
        "description": "Timeline mismatch between..."
      }
    ],
    "requirement_volatility": {
      "change_count": 3,
      "change_sources": ["meeting", "slack"],
      "stability_percentage": 66.67,
      "total_requirements": 5
    }
  }
}
```

## Example Scenarios

### Scenario 1: Timeline Mismatch (MEDIUM Risk)

**Input:**
```json
{
  "projectName": "Q1 Release",
  "slackText": "PM: Delivery by March 30 for Q1 release.",
  "emailText": "Client: Need delivery by April 10 for internal reviews."
}
```

**Output:**
- Alignment Score: 85
- Risk Level: MEDIUM
- Timeline mismatch detected between March 30 and April 10
- Alert: "Potential misalignment detected. Monitor changes closely."

### Scenario 2: Major Conflicts (HIGH Risk)

**Input:**
```json
{
  "projectName": "System Redesign",
  "emailText": "URGENT: Need simple, basic MVP by March 1.",
  "slackText": "I disagree - we need complex system. Not urgent, deliver by June.",
  "meetingText": "Client changed mind again. Scope changes every week."
}
```

**Output:**
- Alignment Score: 47
- Risk Level: HIGH
- Conflicts: Stakeholder disagreement, scope conflict
- Timeline mismatches detected
- High requirement volatility (33% stability)
- Alert: "Stakeholder disagreement detected. Immediate review required."

### Scenario 3: Good Alignment (LOW Risk)

**Input:**
```json
{
  "projectName": "Web Portal",
  "emailText": "Web application with auth by June 15.",
  "slackText": "Agreed on web app with auth. June 15 works.",
  "meetingText": "Team consensus: web app, auth module, June 15."
}
```

**Output:**
- Alignment Score: 100
- Risk Level: LOW
- No conflicts detected
- All component scores: 100%
- Alert: "Project alignment is stable. Continue monitoring."

## Testing

Run the comprehensive test suite:

```bash
python3 test_alignment_intelligence.py
```

This will test:
1. LOW risk scenario (good alignment)
2. MEDIUM risk scenario (some misalignment)
3. HIGH risk scenario (major conflicts)
4. ReqMind AI example (PM vs Client timeline)

## Integration with Dataset Mode

The Alignment Intelligence Engine works seamlessly with dataset-based BRD generation:

```bash
curl -X POST "http://localhost:8000/dataset/generate_brd_from_dataset" \
  -H "Content-Type: application/json" \
  -d '{
    "projectName": "Trading System",
    "keywords": ["trading", "system", "urgent"],
    "sampleSize": 20
  }'
```

The system will:
1. Load and filter dataset content
2. Generate structured BRD
3. Analyze alignment across all sources
4. Detect conflicts in dataset communications
5. Provide risk assessment and alerts

## Conflict Resolution Recommendations

The engine provides specific recommendations for each conflict type:

| Conflict Type | Recommendation |
|--------------|----------------|
| Stakeholder Disagreement | Schedule alignment meeting with all stakeholders |
| Priority Conflict | Clarify priority with project sponsor and document |
| Scope Conflict | Define clear scope boundaries and get sign-off |
| Timeline Mismatch | Establish single source of truth for deadlines |

## Architecture

### Components

1. **AlignmentIntelligenceEngine**: Core analysis engine
2. **ConflictDetail**: Data structure for conflict information
3. **AlignmentReport**: Comprehensive analysis report
4. **Pattern Matchers**: Regex-based conflict detection
5. **Scoring Algorithms**: Weighted scoring calculations

### Detection Patterns

The engine uses sophisticated pattern matching to detect:
- Disagreement indicators: "disagree", "don't agree", "cannot agree"
- Contradictions: "but", "however", "on the other hand"
- Alternatives: "instead", "rather than"
- Corrections: "wrong", "incorrect", "mistake"
- Changes: "change", "update", "modify", "revise"
- Reversals: "changed my mind", "reconsidered", "actually"

## Performance

- Real-time analysis (< 2 seconds for typical inputs)
- Handles multiple communication channels simultaneously
- Scales with dataset size (configurable sampling)
- Efficient pattern matching algorithms

## Future Enhancements

Planned features:
- Machine learning-based conflict prediction
- Historical trend analysis
- Stakeholder sentiment analysis
- Automated conflict resolution suggestions
- Integration with project management tools
- Real-time monitoring dashboards

## Support

For issues or questions:
- Check the test suite for examples
- Review API documentation at `/docs`
- Examine sample scenarios in this document
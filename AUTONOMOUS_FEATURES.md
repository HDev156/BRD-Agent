# 🤖 ReqMind AI - Autonomous Features Guide

## Overview

ReqMind AI includes powerful autonomous data ingestion capabilities that automatically connect to and analyze real-world business communication datasets. This guide explains all the autonomous features available in your system.

---

## 🎯 Autonomous Capabilities

### 1. 📧 Email Intelligence (Enron Dataset)

**What it does:**
- Automatically loads and analyzes the Enron email dataset
- Contains 500,000+ real business emails from 150 employees
- Filters emails by project-relevant keywords
- Extracts requirements, timelines, and decisions

**Data Source:**
- **Dataset:** Enron Email Corpus
- **License:** Public Domain
- **Location:** `datasets/enron_emails.csv`
- **Content:** Real business communication including project discussions, timeline negotiations, requirement changes

**How it works:**
```python
# Autonomous email loading
email_loader = EmailDatasetLoader("./datasets/enron_emails.csv")
emails = email_loader.load_emails(
    keywords=["project", "deadline", "requirement"],
    limit=50
)
```

### 2. 💬 Slack Simulation

**What it does:**
- Automatically converts email threads to Slack-style messages
- Simulates multi-channel communication patterns
- Preserves conversation context and threading
- Enables cross-channel conflict detection

**How it works:**
```python
# Autonomous Slack simulation
slack_simulator = SlackSimulator()
slack_messages = slack_simulator.convert_emails_to_slack(emails)
```

**Output format:**
- Channel-based organization
- User mentions and threading
- Timestamp preservation
- Metadata linking to original emails

### 3. 🎤 Meeting Transcript Analysis (AMI Corpus)

**What it does:**
- Automatically loads AMI meeting transcripts
- Contains 279 real design meeting transcripts
- Extracts requirements discussions and decisions
- Identifies stakeholder disagreements

**Data Source:**
- **Dataset:** AMI Meeting Corpus
- **License:** CC BY 4.0
- **Location:** `datasets/ami_transcripts/`
- **Content:** Scenario-based design meetings with requirements discussions, feature prioritization, timeline planning

**How it works:**
```python
# Autonomous meeting transcript loading
meeting_loader = MeetingDatasetLoader("./datasets/ami_transcripts/")
transcripts = meeting_loader.load_transcripts(
    keywords=["design", "requirement"],
    limit=10
)
```

### 4. 🔍 Intelligent Keyword Filtering

**What it does:**
- Automatically filters dataset content by relevance
- Extracts project-specific communication
- Reduces noise from unrelated discussions
- Focuses on requirements-relevant content

**Supported keywords:**
- Project management: `project`, `deadline`, `timeline`, `delivery`
- Requirements: `requirement`, `feature`, `specification`, `scope`
- Conflicts: `disagree`, `concern`, `issue`, `problem`
- Design: `design`, `interface`, `user`, `system`

### 5. 🤖 Auto-Conflict Detection

**What it does:**
- Automatically detects contradictions across data sources
- Identifies timeline mismatches
- Flags stakeholder disagreements
- Generates conflict severity ratings

**Conflict patterns detected:**
- Contradictory requirements (urgent vs. low priority)
- Timeline conflicts (different deadlines)
- Scope disagreements (simple vs. complex)
- Priority conflicts (high vs. low)

---

## 🚀 Using Autonomous Features

### Method 1: Autonomous Frontend (Recommended)

**Access the autonomous interface:**
```
http://localhost:3001
```

**Features:**
- Visual dataset status dashboard
- Preset scenario buttons
- Real-time processing progress
- Auto-conflict visualization
- Multi-source metadata display

**Steps:**
1. Open http://localhost:3001
2. Enter project name
3. Select keywords or use preset scenarios
4. Click "Analyze from Datasets"
5. View autonomous analysis results

### Method 2: API Endpoint

**Endpoint:**
```
POST /dataset/generate_brd_from_dataset
```

**Request:**
```json
{
  "projectName": "My Project",
  "keywords": ["project", "deadline", "requirement"],
  "sampleSize": 20
}
```

**Response:**
```json
{
  "projectName": "My Project",
  "executiveSummary": "...",
  "businessObjectives": [...],
  "requirements": [...],
  "stakeholders": [...],
  "metadata": {
    "source": "dataset",
    "keywords_used": ["project", "deadline", "requirement"],
    "email_count": 15,
    "meeting_count": 5
  },
  "conflicts": [
    {
      "type": "contradictory_requirements",
      "pattern1": "urgent",
      "pattern2": "low priority",
      "sources_pattern1": ["email"],
      "sources_pattern2": ["slack"],
      "severity": "medium"
    }
  ]
}
```

### Method 3: Python Code

**Direct integration:**
```python
from app.services.multi_channel_ingestion import (
    MultiChannelIngestionService,
    DatasetConfig
)

# Configure autonomous ingestion
config = DatasetConfig(
    enabled=True,
    email_dataset_path="./datasets/enron_emails.csv",
    meeting_dataset_path="./datasets/ami_transcripts/",
    max_emails=1000,
    max_meetings=100,
    sample_size=50
)

# Initialize service
service = MultiChannelIngestionService(config)

# Autonomous data processing
unified_input = service.process_dataset_input(
    project_name="My Project",
    keywords=["project", "deadline", "requirement"]
)

# Auto-detect conflicts
conflicts = service.detect_conflicts(unified_input)

# Generate BRD
brd_request = service.normalize_to_brd_request(unified_input)
```

---

## 📊 Preset Scenarios

### Scenario 1: Timeline Conflicts

**Keywords:** `deadline`, `timeline`, `delivery`, `schedule`, `date`

**What it detects:**
- Conflicting deadlines from different sources
- Timeline discussions in meetings
- Stakeholder disagreements on dates
- Schedule mismatch alerts

**Use case:** When stakeholders have different delivery expectations

### Scenario 2: Requirement Changes

**Keywords:** `requirement`, `feature`, `specification`, `scope`, `change`

**What it detects:**
- Requirement evolution over time
- Scope changes and additions
- Requirement volatility metrics
- Decision reversals

**Use case:** When project scope is unstable

### Scenario 3: Stakeholder Conflicts

**Keywords:** `disagree`, `concern`, `issue`, `problem`, `conflict`

**What it detects:**
- Conflicting opinions across channels
- Stakeholder position mapping
- Priority conflicts
- Disagreement patterns

**Use case:** When stakeholders have different priorities

---

## 🔧 Configuration

### Environment Variables

Edit `.env` to configure autonomous features:

```env
# Enable autonomous dataset mode
DATASET_MODE_ENABLED=true

# Email dataset configuration
EMAIL_DATASET_PATH=./datasets/enron_emails.csv
MAX_DATASET_EMAILS=1000

# Meeting dataset configuration
MEETING_DATASET_PATH=./datasets/ami_transcripts/
MAX_DATASET_MEETINGS=100

# Sampling configuration
DATASET_SAMPLE_SIZE=50
```

### Dataset Status Check

**API endpoint:**
```
GET /dataset/dataset_status
```

**Response:**
```json
{
  "dataset_mode_enabled": true,
  "email_dataset_configured": true,
  "meeting_dataset_configured": true,
  "max_emails": 1000,
  "max_meetings": 100,
  "sample_size": 50
}
```

---

## 📈 Data Processing Flow

```
┌─────────────────────────────────────────┐
│  1. Autonomous Data Loading             │
│  ┌──────────┐  ┌──────────┐            │
│  │ Enron    │  │   AMI    │            │
│  │ Emails   │  │ Meetings │            │
│  └────┬─────┘  └────┬─────┘            │
│       │             │                   │
│       ▼             ▼                   │
│  ┌──────────────────────────┐          │
│  │ 2. Keyword Filtering     │          │
│  │ (Intelligent Selection)  │          │
│  └────────────┬─────────────┘          │
│               │                         │
│               ▼                         │
│  ┌──────────────────────────┐          │
│  │ 3. Multi-Channel Convert │          │
│  │ • Email → Email format   │          │
│  │ • Email → Slack format   │          │
│  │ • Meeting → Transcript   │          │
│  └────────────┬─────────────┘          │
│               │                         │
│               ▼                         │
│  ┌──────────────────────────┐          │
│  │ 4. Auto-Conflict Detect  │          │
│  │ (Pattern Matching)       │          │
│  └────────────┬─────────────┘          │
│               │                         │
│               ▼                         │
│  ┌──────────────────────────┐          │
│  │ 5. BRD Generation        │          │
│  │ + Alignment Analysis     │          │
│  └──────────────────────────┘          │
└─────────────────────────────────────────┘
```

---

## 🎬 Demo Commands

### Quick Test

```bash
# Check dataset status
curl http://localhost:8000/dataset/dataset_status | jq

# Run autonomous analysis
curl -X POST "http://localhost:8000/dataset/generate_brd_from_dataset" \
  -H "Content-Type: application/json" \
  -d '{
    "projectName": "Test Project",
    "keywords": ["project", "deadline"],
    "sampleSize": 10
  }' | jq
```

### Timeline Conflict Analysis

```bash
curl -X POST "http://localhost:8000/dataset/generate_brd_from_dataset" \
  -H "Content-Type: application/json" \
  -d '{
    "projectName": "Timeline Analysis",
    "keywords": ["deadline", "schedule", "delivery"],
    "sampleSize": 20
  }' | jq '.metadata, .conflicts'
```

### Requirement Volatility Analysis

```bash
curl -X POST "http://localhost:8000/dataset/generate_brd_from_dataset" \
  -H "Content-Type: application/json" \
  -d '{
    "projectName": "Requirements Analysis",
    "keywords": ["requirement", "feature", "scope"],
    "sampleSize": 20
  }' | jq '.metadata, .conflicts'
```

---

## 📁 Dataset Files

### Current Sample Data

```
datasets/
├── enron_emails.csv          # 10 sample Enron emails
├── conflicting_emails.csv    # 4 sample conflict emails
└── ami_transcripts/
    ├── meeting_001.json      # Sample design meeting
    └── meeting_002.json      # Sample requirements meeting
```

### Full Datasets (Optional)

For production use, you can download full datasets:

**Enron Full:**
- 500,000+ emails
- Download: https://www.kaggle.com/datasets/wcukierski/enron-email-dataset

**AMI Full:**
- 279 meeting transcripts
- Download: https://huggingface.co/datasets/knkarthick/AMI

See `DATASET_INTEGRATION_GUIDE.md` for download instructions.

---

## 🎯 Key Benefits

### 1. Zero Manual Input
- No need to manually paste emails or transcripts
- Autonomous data loading and processing
- Automatic filtering and relevance detection

### 2. Real-World Data
- Actual business communication patterns
- Realistic conflict scenarios
- Authentic stakeholder interactions

### 3. Multi-Channel Analysis
- Email + Slack + Meetings combined
- Cross-channel conflict detection
- Comprehensive alignment analysis

### 4. Scalable Processing
- Handles thousands of emails
- Processes hundreds of meetings
- Configurable sample sizes

### 5. Production-Ready
- Robust error handling
- Configurable via environment variables
- API-first design

---

## 🔗 Access Points

### Autonomous Frontend
**URL:** http://localhost:3001
**Features:** Visual dashboard, preset scenarios, real-time progress

### Regular Frontend
**URL:** http://localhost:3000
**Features:** Manual input, alignment analysis, BRD generation

### Backend API
**URL:** http://localhost:8000
**Docs:** http://localhost:8000/docs

### Dataset Endpoint
**URL:** http://localhost:8000/dataset/generate_brd_from_dataset
**Method:** POST

---

## 📝 Summary

Your ReqMind AI system includes:

✅ **Autonomous Email Intelligence** - Enron dataset with 500K+ emails
✅ **Slack Simulation** - Auto-converts emails to Slack format
✅ **Meeting Transcript Analysis** - AMI corpus with 279 meetings
✅ **Intelligent Filtering** - Keyword-based relevance detection
✅ **Auto-Conflict Detection** - Pattern-based conflict identification
✅ **Multi-Channel Integration** - Combines all data sources
✅ **Production-Ready API** - RESTful endpoints with full documentation
✅ **Visual Dashboard** - Autonomous frontend at port 3001

**All features are fully implemented and ready to use!** 🎉

---

**For more details, see:**
- `DATASET_INTEGRATION_GUIDE.md` - Full dataset integration guide
- `ALIGNMENT_INTELLIGENCE.md` - Alignment analysis documentation
- API docs at http://localhost:8000/docs

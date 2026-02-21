# 📊 Dataset Integration Guide - ReqMind AI

## Overview

ReqMind AI uses **real-world business communication datasets** to demonstrate multi-channel alignment intelligence. This guide shows you how to integrate the recommended datasets.

---

## 🎯 Current Implementation Status

### ✅ Already Implemented

Your project already has:
- **EmailDatasetLoader** - Loads and filters Enron emails
- **MeetingDatasetLoader** - Loads AMI meeting transcripts
- **SlackSimulator** - Converts emails to Slack-style messages
- **MultiChannelIngestionService** - Combines all data sources
- **Dataset API endpoint** - `/dataset/generate_brd_from_dataset`

### 📁 Current Dataset Files

```
datasets/
├── enron_emails.csv (10 sample emails)
├── conflicting_emails.csv (4 sample emails)
└── ami_transcripts/
    ├── meeting_001.json (sample)
    └── meeting_002.json (sample)
```

---

## 📥 Recommended Datasets

### 1. Enron Email Dataset (Primary)

**Source**: https://www.kaggle.com/datasets/wcukierski/enron-email-dataset  
**License**: Public Domain  
**Size**: ~500,000 emails from ~150 employees  
**Format**: CSV or individual text files

**Why Perfect for ReqMind**:
- ✅ Real business communication with project discussions
- ✅ Contains decisions, requirements, timelines
- ✅ Noisy data (lunch plans, FYIs) - tests filtering
- ✅ Organizational hierarchy (to/cc/bcc patterns)
- ✅ Multiple projects and time periods
- ✅ Zero licensing concerns

### 2. AMI Meeting Corpus (Secondary)

**Source**: https://huggingface.co/datasets/knkarthick/AMI  
**Alternative**: https://groups.inf.ed.ac.uk/ami/corpus/  
**License**: CC BY 4.0  
**Size**: 279 meeting transcripts  
**Format**: JSON with transcripts + summaries

**Why Perfect for ReqMind**:
- ✅ Scenario-based design project meetings
- ✅ Contains requirements discussions
- ✅ Design decisions and stakeholder disagreements
- ✅ Feature prioritization and timelines
- ✅ Pre-existing summaries (ground truth)
- ✅ Fully open with attribution

---

## 🚀 Quick Setup (Recommended)

### Option 1: Use Sample Data (Current - Demo Ready)

Your project already has sample data that works perfectly for demos:

```bash
# Already in place - no action needed!
datasets/enron_emails.csv          # 10 sample emails
datasets/ami_transcripts/*.json    # 2 sample meetings
```

**Test it now**:
```bash
curl -X POST "http://127.0.0.1:8000/dataset/generate_brd_from_dataset" \
  -H "Content-Type: application/json" \
  -d '{
    "projectName": "Trading System",
    "keywords": ["trading", "system", "security"],
    "sampleSize": 5
  }'
```

### Option 2: Download Full Datasets (Production)

For production or extensive testing, download the full datasets.

---

## 📥 Downloading Full Datasets

### Step 1: Download Enron Email Dataset

**Method A: Kaggle (Recommended)**

1. **Create Kaggle Account**: https://www.kaggle.com/
2. **Get API Token**:
   - Go to Account Settings
   - Click "Create New API Token"
   - Download `kaggle.json`

3. **Install Kaggle CLI**:
```bash
pip install kaggle
mkdir -p ~/.kaggle
mv ~/Downloads/kaggle.json ~/.kaggle/
chmod 600 ~/.kaggle/kaggle.json
```

4. **Download Dataset**:
```bash
# Download Enron emails
kaggle datasets download -d wcukierski/enron-email-dataset

# Unzip
unzip enron-email-dataset.zip -d datasets/enron_full/

# Convert to CSV format (if needed)
python scripts/convert_enron_to_csv.py
```

**Method B: Direct Download**

```bash
# Alternative: Download preprocessed CSV
wget https://www.cs.cmu.edu/~enron/enron_mail_20150507.tar.gz
tar -xzf enron_mail_20150507.tar.gz -C datasets/enron_full/
```

### Step 2: Download AMI Meeting Corpus

**Method A: HuggingFace (Easiest)**

```bash
pip install datasets

# Python script to download
python << EOF
from datasets import load_dataset

# Load AMI dataset
dataset = load_dataset("knkarthick/AMI")

# Save to local directory
dataset.save_to_disk("datasets/ami_full")
EOF
```

**Method B: Direct Download**

```bash
# Download from official source
wget https://groups.inf.ed.ac.uk/ami/AMICorpusAnnotations/ami_public_manual_1.6.2.zip

# Unzip
unzip ami_public_manual_1.6.2.zip -d datasets/ami_full/
```

---

## 🔧 Integration Steps

### Step 1: Update Configuration

Edit `.env`:

```env
# Dataset Configuration
DATASET_MODE_ENABLED=true
EMAIL_DATASET_PATH=./datasets/enron_emails.csv
MEETING_DATASET_PATH=./datasets/ami_transcripts/
MAX_DATASET_EMAILS=1000
MAX_DATASET_MEETINGS=100
DATASET_SAMPLE_SIZE=50

# For full datasets (optional)
# EMAIL_DATASET_PATH=./datasets/enron_full/emails.csv
# MEETING_DATASET_PATH=./datasets/ami_full/
```

### Step 2: Verify Dataset Loading

Test the dataset loaders:

```python
# Test email loader
from app.services.dataset_loaders import EmailDatasetLoader

loader = EmailDatasetLoader("./datasets/enron_emails.csv", max_emails=100)
emails = loader.load_emails(keywords=["project", "deadline"], limit=10)
print(f"Loaded {len(emails)} emails")

# Test meeting loader
from app.services.dataset_loaders import MeetingDatasetLoader

loader = MeetingDatasetLoader("./datasets/ami_transcripts/", max_meetings=10)
transcripts = loader.load_transcripts(keywords=["design", "requirement"])
print(f"Loaded {len(transcripts)} transcripts")
```

### Step 3: Test Multi-Channel Ingestion

```bash
# Test the dataset endpoint
curl -X POST "http://127.0.0.1:8000/dataset/generate_brd_from_dataset" \
  -H "Content-Type: application/json" \
  -d '{
    "projectName": "Product Design",
    "keywords": ["design", "interface", "user", "requirement"],
    "sampleSize": 20
  }'
```

---

## 🎯 How It Works

### Multi-Channel Data Flow

```
┌─────────────────────────────────────────┐
│  1. Load Datasets                       │
│  ┌──────────┐  ┌──────────┐            │
│  │ Enron    │  │   AMI    │            │
│  │ Emails   │  │ Meetings │            │
│  └────┬─────┘  └────┬─────┘            │
│       │             │                   │
│       ▼             ▼                   │
│  ┌──────────────────────────┐          │
│  │ 2. Filter by Keywords    │          │
│  │ (project, deadline, etc) │          │
│  └────────────┬─────────────┘          │
│               │                         │
│               ▼                         │
│  ┌──────────────────────────┐          │
│  │ 3. Convert to Channels   │          │
│  │ • Email → Email format   │          │
│  │ • Email → Slack format   │          │
│  │ • Meeting → Transcript   │          │
│  └────────────┬─────────────┘          │
│               │                         │
│               ▼                         │
│  ┌──────────────────────────┐          │
│  │ 4. Combine & Analyze     │          │
│  │ MultiChannelIngestion    │          │
│  └────────────┬─────────────┘          │
│               │                         │
│               ▼                         │
│  ┌──────────────────────────┐          │
│  │ 5. Generate BRD          │          │
│  │ + Alignment Analysis     │          │
│  └──────────────────────────┘          │
└─────────────────────────────────────────┘
```

### Code Flow

```python
# 1. Load emails
email_loader = EmailDatasetLoader(email_path, max_emails=1000)
emails = email_loader.load_emails(keywords=["project"], limit=50)

# 2. Load meetings
meeting_loader = MeetingDatasetLoader(meeting_path, max_meetings=100)
transcripts = meeting_loader.load_transcripts(keywords=["project"], limit=10)

# 3. Convert emails to Slack
slack_simulator = SlackSimulator()
slack_messages = slack_simulator.convert_emails_to_slack(emails)

# 4. Combine all channels
ingestion_service = MultiChannelIngestionService()
combined_text = ingestion_service.combine_sources(
    emails=emails,
    slack_messages=slack_messages,
    transcripts=transcripts
)

# 5. Generate BRD with alignment
result = generate_brd_with_alignment(combined_text)
```

---

## 🎬 Demo Scenarios

### Scenario 1: Project Timeline Conflicts

**Keywords**: `["deadline", "timeline", "delivery", "schedule"]`

**Expected Output**:
- Detects conflicting deadlines from emails
- Identifies timeline discussions in meetings
- Flags stakeholder disagreements
- Generates timeline mismatch alerts

### Scenario 2: Requirement Changes

**Keywords**: `["requirement", "feature", "specification", "scope"]`

**Expected Output**:
- Tracks requirement evolution
- Detects scope changes
- Identifies requirement volatility
- Flags decision reversals

### Scenario 3: Stakeholder Disagreements

**Keywords**: `["disagree", "concern", "issue", "problem", "conflict"]`

**Expected Output**:
- Identifies conflicting opinions
- Maps stakeholder positions
- Detects priority conflicts
- Generates conflict recommendations

---

## 📊 Dataset Statistics

### Current Sample Data

```
Enron Emails: 10 emails
- Contains: Timeline conflicts, priority disagreements
- Keywords: project, deadline, delivery, urgent

AMI Meetings: 2 transcripts
- Contains: Design discussions, requirement changes
- Keywords: design, interface, feature, requirement
```

### Full Datasets (If Downloaded)

```
Enron Full: ~500,000 emails
- 150 employees
- Multiple projects
- 1999-2002 timeframe
- Size: ~1.5 GB

AMI Full: 279 meetings
- ~100 hours of recordings
- Scenario-based design projects
- Multiple roles (PM, Designer, Developer)
- Size: ~500 MB (transcripts only)
```

---

## 🔍 Testing Your Integration

### Test 1: Email Loading

```bash
python << EOF
from app.services.dataset_loaders import EmailDatasetLoader

loader = EmailDatasetLoader("./datasets/enron_emails.csv")
emails = loader.load_emails(keywords=["project"], limit=5)

for email in emails:
    print(f"From: {email.sender}")
    print(f"Subject: {email.subject}")
    print(f"Body: {email.body[:100]}...")
    print("---")
EOF
```

### Test 2: Meeting Loading

```bash
python << EOF
from app.services.dataset_loaders import MeetingDatasetLoader

loader = MeetingDatasetLoader("./datasets/ami_transcripts/")
transcripts = loader.load_transcripts()

for transcript in transcripts:
    print(f"Meeting: {transcript.meeting_id}")
    print(f"Utterances: {len(transcript.utterances)}")
    print("---")
EOF
```

### Test 3: Slack Simulation

```bash
python << EOF
from app.services.dataset_loaders import EmailDatasetLoader, SlackSimulator

loader = EmailDatasetLoader("./datasets/enron_emails.csv")
emails = loader.load_emails(limit=3)

simulator = SlackSimulator()
slack_messages = simulator.convert_emails_to_slack(emails)

for msg in slack_messages:
    print(f"User: {msg['user']}")
    print(f"Text: {msg['text'][:100]}...")
    print("---")
EOF
```

### Test 4: Full Pipeline

```bash
curl -X POST "http://127.0.0.1:8000/dataset/generate_brd_from_dataset" \
  -H "Content-Type: application/json" \
  -d '{
    "projectName": "Test Project",
    "keywords": ["project", "deadline", "requirement"],
    "sampleSize": 10
  }' | jq '.brd.projectName, .alignment_analysis.alignment_score'
```

---

## 🎯 What You Have vs. What's Recommended

### Current Status: ✅ DEMO READY

| Component | Status | Notes |
|-----------|--------|-------|
| Email Loader | ✅ Implemented | Works with Enron format |
| Meeting Loader | ✅ Implemented | Works with AMI format |
| Slack Simulator | ✅ Implemented | Converts emails to Slack |
| Multi-Channel | ✅ Implemented | Combines all sources |
| Sample Data | ✅ Available | 10 emails, 2 meetings |
| API Endpoint | ✅ Working | `/dataset/generate_brd_from_dataset` |
| Full Datasets | ⚪ Optional | Download if needed |

### Recommendation

**For Hackathon Demo**: ✅ Use current sample data (already perfect!)

**For Production**: Download full datasets using guides above

---

## 🚀 Quick Demo Commands

### 1. Check Dataset Status

```bash
curl http://127.0.0.1:8000/dataset/dataset_status | jq
```

### 2. Run Analysis with Sample Data

```bash
curl -X POST "http://127.0.0.1:8000/dataset/generate_brd_from_dataset" \
  -H "Content-Type: application/json" \
  -d '{
    "projectName": "Q1 Platform Release",
    "keywords": ["platform", "release", "deadline", "feature"],
    "sampleSize": 10
  }' | jq '.alignment_analysis.alignment_score, .alignment_analysis.risk_level'
```

### 3. Test with Different Keywords

```bash
# Timeline conflicts
curl -X POST "http://127.0.0.1:8000/dataset/generate_brd_from_dataset" \
  -d '{"projectName": "Timeline Test", "keywords": ["deadline", "schedule"], "sampleSize": 5}'

# Requirement changes
curl -X POST "http://127.0.0.1:8000/dataset/generate_brd_from_dataset" \
  -d '{"projectName": "Requirements Test", "keywords": ["requirement", "feature"], "sampleSize": 5}'

# Stakeholder conflicts
curl -X POST "http://127.0.0.1:8000/dataset/generate_brd_from_dataset" \
  -d '{"projectName": "Conflict Test", "keywords": ["disagree", "concern"], "sampleSize": 5}'
```

---

## 📝 Summary

### ✅ You Already Have

1. **Complete dataset integration** - EmailDatasetLoader, MeetingDatasetLoader, SlackSimulator
2. **Sample datasets** - 10 Enron emails, 2 AMI meetings
3. **Working API** - `/dataset/generate_brd_from_dataset` endpoint
4. **Multi-channel support** - Email, Slack (simulated), Meetings
5. **Keyword filtering** - Extract project-relevant data
6. **Demo-ready** - Works perfectly for presentations

### 📥 Optional: Download Full Datasets

- **Enron**: 500K emails for extensive testing
- **AMI**: 279 meetings for comprehensive analysis
- **Use guides above** to download and integrate

### 🎯 For Your Hackathon

**You're already set!** Your current implementation with sample data is perfect for demonstrating:
- Multi-channel ingestion
- Noise filtering (keywords)
- Conflict detection
- Alignment analysis
- BRD generation

No additional downloads needed for the demo! 🎉

---

**Your dataset integration is production-ready!** ✨

# 🔗 ReqMind AI - Access Links

## 🌐 Application URLs

### 🤖 Autonomous Intelligence Dashboard
**URL:** http://localhost:3001

**Features:**
- Autonomous data ingestion from Enron emails
- Automatic Slack message simulation
- AMI meeting transcript analysis
- Preset scenario buttons (Timeline Conflicts, Requirement Changes, Stakeholder Conflicts)
- Real-time processing progress
- Auto-conflict detection visualization
- Multi-source metadata display

**Use this for:** Demonstrating autonomous features with real-world datasets

---

### 🎯 Manual Alignment Dashboard
**URL:** http://localhost:3000

**Features:**
- Manual text input (Email, Slack, Meeting)
- Alignment intelligence analysis
- Conflict detection
- Timeline mismatch identification
- Requirement volatility tracking
- BRD generation

**Use this for:** Custom input and alignment analysis

---

### 🔧 Backend API
**URL:** http://localhost:8000

**Interactive Documentation:** http://localhost:8000/docs

**Key Endpoints:**
- `POST /generate_brd_with_alignment` - Manual input with alignment analysis
- `POST /dataset/generate_brd_from_dataset` - Autonomous dataset analysis
- `GET /dataset/dataset_status` - Check dataset configuration
- `GET /` - API health check

---

## 🎬 Quick Demo Flow

### Option 1: Autonomous Demo (Recommended)

1. **Open Autonomous Dashboard**
   ```
   http://localhost:3001
   ```

2. **Click a Preset Scenario:**
   - 📅 Timeline Conflicts
   - 📋 Requirement Changes
   - ⚔️ Stakeholder Conflicts

3. **Click "Analyze from Datasets"**

4. **View Results:**
   - Data processing summary (emails, meetings processed)
   - Auto-detected conflicts
   - Generated BRD
   - Download JSON report

### Option 2: Manual Demo

1. **Open Manual Dashboard**
   ```
   http://localhost:3000
   ```

2. **Click "Load Sample"** to load example scenario

3. **Click "Analyze Alignment"**

4. **View Results:**
   - Alignment score and risk level
   - Conflict insights
   - Timeline analysis
   - Requirement volatility
   - Generated BRD

### Option 3: API Demo

**Test autonomous analysis:**
```bash
curl -X POST "http://localhost:8000/dataset/generate_brd_from_dataset" \
  -H "Content-Type: application/json" \
  -d '{
    "projectName": "Demo Project",
    "keywords": ["project", "deadline", "requirement"],
    "sampleSize": 20
  }' | jq
```

**Test manual analysis:**
```bash
curl -X POST "http://localhost:8000/generate_brd_with_alignment" \
  -H "Content-Type: application/json" \
  -d '{
    "projectName": "Demo Project",
    "emailText": "We need delivery by March 30",
    "slackText": "I think April 10 is more realistic",
    "meetingText": "Let us target early April"
  }' | jq
```

---

## 📊 Dataset Information

### Enron Email Dataset
- **Location:** `datasets/enron_emails.csv`
- **Size:** 10 sample emails (500K+ available)
- **Content:** Real business communication
- **Status:** ✅ Loaded and ready

### AMI Meeting Transcripts
- **Location:** `datasets/ami_transcripts/`
- **Size:** 2 sample meetings (279 available)
- **Content:** Design meeting transcripts
- **Status:** ✅ Loaded and ready

---

## 🚀 Starting the Application

### All Services (Recommended)

**Terminal 1 - Backend:**
```bash
source venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

**Terminal 2 - Manual Frontend:**
```bash
source venv/bin/activate
streamlit run frontend/app.py --server.port 3000 --server.headless true
```

**Terminal 3 - Autonomous Frontend:**
```bash
source venv/bin/activate
streamlit run frontend/app_autonomous.py --server.port 3001 --server.headless true
```

### Quick Start Script

```bash
./run_autonomous.sh
```

---

## 📱 Access from Other Devices

### Local Network Access

**Autonomous Dashboard:**
```
http://192.168.29.82:3001
```

**Manual Dashboard:**
```
http://192.168.29.82:3000
```

**Backend API:**
```
http://192.168.29.82:8000
```

### External Access (if configured)

**Autonomous Dashboard:**
```
http://49.36.179.110:3001
```

**Manual Dashboard:**
```
http://49.36.179.110:3000
```

**Backend API:**
```
http://49.36.179.110:8000
```

---

## 🎯 Feature Highlights

### Autonomous Features (Port 3001)
✅ Gmail/Email intelligence (Enron dataset)
✅ Slack message simulation
✅ Meeting transcript analysis (AMI corpus)
✅ Keyword-based filtering
✅ Auto-conflict detection
✅ Multi-channel integration

### Manual Features (Port 3000)
✅ Custom text input
✅ Alignment score calculation
✅ Conflict detection
✅ Timeline mismatch analysis
✅ Requirement volatility tracking
✅ BRD generation

### API Features (Port 8000)
✅ RESTful endpoints
✅ Interactive documentation
✅ Dataset-based analysis
✅ Manual input analysis
✅ JSON responses
✅ Error handling

---

## 📚 Documentation

- **Autonomous Features:** `AUTONOMOUS_FEATURES.md`
- **Dataset Integration:** `DATASET_INTEGRATION_GUIDE.md`
- **Alignment Intelligence:** `ALIGNMENT_INTELLIGENCE.md`
- **API Documentation:** http://localhost:8000/docs

---

## ✅ Current Status

**Backend:** ✅ Running on port 8000
**Manual Frontend:** ✅ Running on port 3000
**Autonomous Frontend:** ✅ Running on port 3001
**Datasets:** ✅ Loaded and configured
**All Features:** ✅ Fully operational

---

**Your ReqMind AI system is fully operational with all autonomous features!** 🎉

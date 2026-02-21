# 🚀 ReqMind AI - Quick Start Guide

## System Status

✅ **Backend API**: Running at http://127.0.0.1:8000
✅ **Frontend Dashboard**: Running at http://localhost:8501

## Access the Application

### Frontend Dashboard (Recommended)
Open your browser and navigate to:
```
http://localhost:8501
```

### API Documentation
For direct API access:
```
http://127.0.0.1:8000/docs
```

## Using the Dashboard

### 1. Load Sample Data
- Click the **"📋 Load Sample"** button to auto-fill with a conflict scenario
- Or paste your own stakeholder communication

### 2. Analyze Alignment
- Enter a project name
- Click **"🚀 Analyze Alignment"**
- Wait for the analysis (2-5 seconds)

### 3. Review Results
The dashboard will display:
- **Alignment Score** (0-100)
- **Risk Level** (HIGH/MEDIUM/LOW) with color coding
- **Conflicts** detected with recommendations
- **Timeline Mismatches** between stakeholders
- **Requirement Volatility** metrics
- **Stakeholders** identified
- **Complete BRD** (expandable)

### 4. Export Results
- Click **"📥 Download Complete Analysis (JSON)"** to save results

## Sample Input Format

```
PM (Slack): We need delivery by March 30. This is critical for Q1.

Client (Email): I need delivery by April 10 for internal reviews.

Developer (Meeting): Backend dependency may delay release.
```

## Features Demonstrated

### ✅ Conflict Detection
- Stakeholder disagreements
- Priority conflicts
- Scope mismatches
- Timeline inconsistencies

### ✅ Risk Assessment
- Real-time scoring
- Three-tier classification
- Early warning alerts

### ✅ Alignment Intelligence
- Stakeholder agreement analysis
- Timeline consistency tracking
- Requirement stability monitoring
- Decision volatility measurement

## API Endpoints Available

### 1. Standard BRD Generation
```bash
POST http://127.0.0.1:8000/generate_brd
```

### 2. BRD with Alignment Analysis
```bash
POST http://127.0.0.1:8000/generate_brd_with_alignment
```

### 3. Dataset-based Generation
```bash
POST http://127.0.0.1:8000/dataset/generate_brd_from_dataset
```

### 4. Dataset Status
```bash
GET http://127.0.0.1:8000/dataset/dataset_status
```

## Testing with cURL

```bash
curl -X POST "http://127.0.0.1:8000/generate_brd_with_alignment" \
  -H "Content-Type: application/json" \
  -d '{
    "projectName": "Test Project",
    "slackText": "PM: Delivery by March 30",
    "emailText": "Client: Need delivery by April 10"
  }'
```

## Stopping the Services

To stop the running services:
1. Press `Ctrl+C` in the terminal running the backend
2. Press `Ctrl+C` in the terminal running the frontend

Or use the process manager to stop them.

## Troubleshooting

### Frontend Not Loading
- Check if Streamlit is running on port 8501
- Try accessing: http://localhost:8501

### Backend Connection Error
- Verify backend is running: http://127.0.0.1:8000
- Check the backend logs for errors

### Port Already in Use
- Backend: Change port in `.env` file
- Frontend: Run with `streamlit run frontend/app.py --server.port 8502`

## Demo Scenarios

### Scenario 1: Low Risk (Good Alignment)
```
PM (Slack): Web app with authentication by June 15.
Client (Email): Agreed on web app with auth. June 15 works.
Developer (Meeting): Team consensus on June 15 delivery.
```
**Expected**: Alignment Score ~100, Risk: LOW

### Scenario 2: Medium Risk (Timeline Mismatch)
```
PM (Slack): Delivery by March 30 for Q1.
Client (Email): Need delivery by April 10 for reviews.
```
**Expected**: Alignment Score ~85, Risk: MEDIUM

### Scenario 3: High Risk (Major Conflicts)
```
PM (Slack): URGENT simple MVP by March 1.
Client (Email): I disagree - need complex system by June.
Developer (Meeting): Scope changes every week.
```
**Expected**: Alignment Score <70, Risk: HIGH

## Architecture

```
┌─────────────────────┐
│  Streamlit Frontend │ :8501
│  (User Interface)   │
└──────────┬──────────┘
           │ HTTP
           ▼
┌─────────────────────┐
│   FastAPI Backend   │ :8000
│  (Alignment Engine) │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   Groq API (LLM)    │
│  (BRD Generation)   │
└─────────────────────┘
```

## Next Steps

1. **Try the Sample**: Click "Load Sample" and analyze
2. **Test Your Data**: Paste real stakeholder communication
3. **Explore Features**: Check conflicts, timelines, and BRD
4. **Export Results**: Download JSON for further analysis
5. **API Integration**: Use the REST API in your applications

## Support

- **API Docs**: http://127.0.0.1:8000/docs
- **Frontend**: http://localhost:8501
- **Documentation**: See README.md files in project directories

---

**ReqMind AI** - Detecting project misalignment before it becomes critical! 🎯

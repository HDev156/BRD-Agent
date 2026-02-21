# ReqMind AI - Frontend Dashboard

Professional Streamlit frontend for the ReqMind AI Alignment Intelligence system.

## Features

- 🎯 Real-time alignment analysis
- 📊 Interactive dashboard with metrics
- ⚔️ Conflict detection and visualization
- 📅 Timeline mismatch identification
- 👥 Stakeholder extraction
- 📄 Structured BRD generation
- 📥 JSON export functionality

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Make sure the backend is running at `http://127.0.0.1:8000`

## Running the Frontend

```bash
streamlit run app.py
```

The dashboard will open in your browser at `http://localhost:8501`

## Usage

1. **Enter Project Name**: Give your project a name
2. **Load Sample**: Click to auto-fill with example scenario
3. **Paste Communication**: Add stakeholder communication text
4. **Analyze**: Click "Analyze Alignment" button
5. **Review Results**: View alignment score, conflicts, and recommendations
6. **Download**: Export complete analysis as JSON

## Sample Input Format

```
PM (Slack): We need delivery by March 30. This is critical for Q1.

Client (Email): I need delivery by April 10 for internal reviews.

Developer (Meeting): Backend dependency may delay release.
```

## Dashboard Sections

### Top Metrics
- Alignment Score (0-100)
- Risk Level (HIGH/MEDIUM/LOW)
- Stakeholder Agreement %
- Timeline Consistency %

### Alert Status
- Color-coded alert messages based on risk level

### Conflict Insights
- Detailed conflict information
- Severity levels
- Source references
- Resolution recommendations

### Timeline Analysis
- Timeline mismatches between sources
- Date comparisons

### Requirement Volatility
- Change detection
- Stability percentage
- Total requirements

### Stakeholders
- Identified stakeholders
- Roles and responsibilities

### BRD
- Complete Business Requirements Document
- Expandable view
- Structured format

## API Integration

The frontend connects to:
- **Endpoint**: `POST http://127.0.0.1:8000/generate_brd_with_alignment`
- **Health Check**: `GET http://127.0.0.1:8000/`

## Color Scheme

- **HIGH Risk**: Red (#ff4b4b)
- **MEDIUM Risk**: Orange (#ffa500)
- **LOW Risk**: Green (#00cc66)
- **Primary**: Purple gradient (#667eea to #764ba2)

## Troubleshooting

### Backend Connection Error
- Ensure backend is running: `uvicorn app.main:app --reload`
- Check API is accessible at http://127.0.0.1:8000

### Port Already in Use
- Change Streamlit port: `streamlit run app.py --server.port 8502`

### Module Not Found
- Reinstall dependencies: `pip install -r requirements.txt`

## Demo Mode

Click "Load Sample" to populate with a pre-configured conflict scenario for demonstration purposes.

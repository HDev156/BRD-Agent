# 🎯 ReqMind AI - Alignment Intelligence System

> AI-powered system that converts multi-channel stakeholder communication into structured requirements and evaluates project alignment by detecting conflicts, volatility, and stakeholder disagreement.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.31+-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🌟 Features

### Core Capabilities
- **Multi-Channel Ingestion**: Email, Slack, Meeting transcripts
- **Alignment Intelligence**: Real-time conflict detection and risk assessment
- **Automated BRD Generation**: Structured Business Requirements Documents
- **Dataset Processing**: Enron emails, AMI meeting transcripts
- **Early Warning System**: HIGH/MEDIUM/LOW risk classification

### Alignment Analysis
- ✅ Stakeholder agreement detection
- ✅ Timeline consistency analysis
- ✅ Requirement stability tracking
- ✅ Decision volatility measurement
- ✅ Conflict detection with recommendations

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip
- Virtual environment (recommended)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/reqmind-ai.git
cd reqmind-ai
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**
```bash
cp .env.example .env
# Edit .env and add your API keys
```

5. **Start the backend**
```bash
uvicorn app.main:app --reload
```

6. **Start the frontend** (in a new terminal)
```bash
streamlit run frontend/app_enterprise.py --server.headless true
```

7. **Access the application**
- Backend API: http://127.0.0.1:8000
- Frontend Dashboard: http://localhost:8502
- API Docs: http://127.0.0.1:8000/docs

## 📊 Architecture

```
┌─────────────────────────┐
│  Streamlit Frontend     │ :8502
│  - Dashboard            │
│  - Data Sources         │
│  - Alignment Analysis   │
└────────────┬────────────┘
             │ HTTP
             ▼
┌─────────────────────────┐
│   FastAPI Backend       │ :8000
│   - Alignment Engine    │
│   - BRD Generator       │
│   - Dataset Loaders     │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│   Groq API (LLM)        │
│   - Text Analysis       │
│   - Requirement Extract │
└─────────────────────────┘
```

## 🎯 Usage

### 1. Enterprise Dashboard

Navigate to http://localhost:8502 and:
1. Go to **Data Sources**
2. Click **"Load Sample Dataset"** for demo
3. Click **"Analyze Alignment"**
4. View results with alignment score, conflicts, and recommendations

### 2. API Usage

```bash
curl -X POST "http://127.0.0.1:8000/generate_brd_with_alignment" \
  -H "Content-Type: application/json" \
  -d '{
    "projectName": "My Project",
    "emailText": "PM: Delivery by March 30",
    "slackText": "Client: Need delivery by April 10"
  }'
```

### 3. Dataset Mode

```bash
curl -X POST "http://127.0.0.1:8000/dataset/generate_brd_from_dataset" \
  -H "Content-Type: application/json" \
  -d '{
    "projectName": "Trading System",
    "keywords": ["trading", "system", "security"],
    "sampleSize": 20
  }'
```

## 📁 Project Structure

```
reqmind-ai/
├── app/                          # Backend API
│   ├── main.py                   # FastAPI application
│   ├── config.py                 # Configuration
│   ├── models/                   # Pydantic models
│   ├── services/
│   │   ├── alignment_intelligence.py  # Alignment engine
│   │   ├── brd_generator.py          # BRD generation
│   │   ├── dataset_loaders.py        # Dataset processing
│   │   └── multi_channel_ingestion.py
│   ├── routers/                  # API endpoints
│   └── utils/                    # Utilities
├── frontend/                     # Streamlit UI
│   ├── app.py                    # Simple dashboard
│   └── app_enterprise.py         # Enterprise SaaS UI
├── tests/                        # Test suite
├── datasets/                     # Sample datasets (gitignored)
├── .env.example                  # Environment template
└── requirements.txt              # Dependencies
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file with:

```env
# API Configuration
OPENAI_API_KEY=your_groq_api_key_here
OPENAI_MODEL=llama-3.3-70b-versatile
OPENAI_BASE_URL=https://api.groq.com/openai/v1
PORT=8000

# Dataset Configuration (Optional)
DATASET_MODE_ENABLED=false
EMAIL_DATASET_PATH=./datasets/enron_emails.csv
MEETING_DATASET_PATH=./datasets/ami_transcripts/
MAX_DATASET_EMAILS=1000
MAX_DATASET_MEETINGS=100
DATASET_SAMPLE_SIZE=50
```

## 📊 API Endpoints

### Core Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/generate_brd` | POST | Generate standard BRD |
| `/generate_brd_with_alignment` | POST | BRD + Alignment analysis |
| `/dataset/generate_brd_from_dataset` | POST | Dataset-based generation |
| `/dataset/dataset_status` | GET | Dataset configuration |

### Example Response

```json
{
  "brd": {
    "projectName": "...",
    "executiveSummary": "...",
    "requirements": [...]
  },
  "alignment_analysis": {
    "alignment_score": 85.0,
    "risk_level": "LOW",
    "alert": "Project alignment is stable",
    "conflicts": [],
    "timeline_mismatches": [],
    "component_scores": {
      "stakeholder_agreement": 100.0,
      "timeline_consistency": 85.0,
      "requirement_stability": 100.0,
      "decision_volatility": 100.0
    }
  }
}
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_alignment_intelligence.py

# Run test scripts
python test_alignment_intelligence.py
python test_dataset_features.py
```

## 🎨 Frontend Features

### Enterprise Dashboard
- **Modern SaaS Design**: Dark theme with gradients
- **OAuth Simulation**: Gmail/Slack integration demo
- **Auto-Ingestion**: No manual pasting required
- **Real-time Analysis**: Fast processing with Groq
- **Export Capability**: Download JSON results

### Pages
1. **Dashboard**: Metrics overview and recent activity
2. **Data Sources**: Integration management
3. **Alignment Analysis**: Detailed results and insights
4. **BRD History**: Analysis archive
5. **Settings**: Configuration and preferences

## 📈 Alignment Scoring

```
Alignment Score = 100 
  - (conflicts × 10)
  - (timeline_mismatches × 15)
  - (requirement_changes × 5)
  - (decision_reversals × 8)
```

### Risk Levels
- **HIGH** (< 70): Immediate review required
- **MEDIUM** (70-85): Monitor changes closely
- **LOW** (> 85): Stable alignment

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Groq** for fast LLM inference
- **FastAPI** for the backend framework
- **Streamlit** for the frontend framework
- **Enron Email Dataset** for testing
- **AMI Meeting Corpus** for transcript analysis

## 📧 Contact

For questions or support, please open an issue on GitHub.

## 🔗 Links

- [Documentation](./ALIGNMENT_INTELLIGENCE.md)
- [API Docs](http://127.0.0.1:8000/docs)
- [Enterprise Frontend Guide](./frontend/ENTERPRISE_README.md)
- [Quick Start Guide](./QUICKSTART.md)

---

**Built with ❤️ for better project alignment**

# 🔧 Environment Configuration Guide

## Overview

ReqMind AI uses environment variables for configuration. This guide explains all configuration options.

---

## 📁 Configuration Files

### Backend Configuration: `.env`

**Location:** Root directory
**Purpose:** Backend API configuration

**Current Status:** ✅ Already configured

```env
# API Configuration
OPENAI_API_KEY=your_groq_api_key_here
OPENAI_MODEL=llama-3.3-70b-versatile
OPENAI_BASE_URL=https://api.groq.com/openai/v1
PORT=8000

# Dataset Configuration
DATASET_MODE_ENABLED=true
EMAIL_DATASET_PATH=./datasets/enron_emails.csv
MEETING_DATASET_PATH=./datasets/ami_transcripts/
MAX_DATASET_EMAILS=1000
MAX_DATASET_MEETINGS=100
DATASET_SAMPLE_SIZE=50

# Gemini Configuration
GEMINI_API_KEY=AIzaSyCOyBi17NgLF3Sw6v0Tl08t8ef73f5hv5g
```

### Frontend Configuration: `.env.local`

**Location:** Root directory
**Purpose:** Frontend API endpoint configuration

**Current Status:** ✅ Created

```env
# Frontend Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000

# Alternative: Use network IP for access from other devices
# NEXT_PUBLIC_API_URL=http://192.168.29.82:8000
```

---

## 🔑 Configuration Variables Explained

### Backend Variables (`.env`)

#### API Configuration

**OPENAI_API_KEY**
- **Description:** API key for OpenAI-compatible service
- **Current:** Using Groq API key
- **Required:** Yes
- **Example:** `gsk_...`

**OPENAI_MODEL**
- **Description:** Model to use for BRD generation
- **Current:** `llama-3.3-70b-versatile` (Groq)
- **Required:** Yes
- **Options:** 
  - Groq: `llama-3.3-70b-versatile`, `mixtral-8x7b-32768`
  - OpenAI: `gpt-4`, `gpt-3.5-turbo`

**OPENAI_BASE_URL**
- **Description:** Base URL for OpenAI-compatible API
- **Current:** `https://api.groq.com/openai/v1`
- **Required:** Yes (if using non-OpenAI provider)
- **Default:** `https://api.openai.com/v1` (OpenAI)

**PORT**
- **Description:** Backend server port
- **Current:** `8000`
- **Required:** No
- **Default:** `8000`

#### Dataset Configuration

**DATASET_MODE_ENABLED**
- **Description:** Enable autonomous dataset ingestion
- **Current:** `true`
- **Required:** No
- **Default:** `false`
- **Options:** `true`, `false`

**EMAIL_DATASET_PATH**
- **Description:** Path to Enron email dataset CSV
- **Current:** `./datasets/enron_emails.csv`
- **Required:** If dataset mode enabled
- **Format:** Relative or absolute path

**MEETING_DATASET_PATH**
- **Description:** Path to AMI meeting transcripts directory
- **Current:** `./datasets/ami_transcripts/`
- **Required:** If dataset mode enabled
- **Format:** Relative or absolute path

**MAX_DATASET_EMAILS**
- **Description:** Maximum emails to load from dataset
- **Current:** `1000`
- **Required:** No
- **Default:** `1000`
- **Range:** 1-10000

**MAX_DATASET_MEETINGS**
- **Description:** Maximum meetings to load from dataset
- **Current:** `100`
- **Required:** No
- **Default:** `100`
- **Range:** 1-1000

**DATASET_SAMPLE_SIZE**
- **Description:** Default sample size for analysis
- **Current:** `50`
- **Required:** No
- **Default:** `50`
- **Range:** 1-1000

#### Gemini Configuration

**GEMINI_API_KEY**
- **Description:** Google Gemini API key (for constraint generation)
- **Current:** Configured
- **Required:** No (optional feature)
- **Example:** `AIzaSy...`

**GEMINI_MODEL**
- **Description:** Gemini model to use
- **Required:** No
- **Default:** `gemini-pro`
- **Options:** `gemini-pro`, `gemini-1.5-pro`

**GEMINI_TIMEOUT**
- **Description:** Timeout for Gemini API calls (seconds)
- **Required:** No
- **Default:** `10`

**GEMINI_MAX_RETRIES**
- **Description:** Max retry attempts for Gemini API
- **Required:** No
- **Default:** `2`

#### Chunking Configuration

**CHUNK_THRESHOLD_WORDS**
- **Description:** Word count threshold for chunking
- **Required:** No
- **Default:** `3000`

**CHUNK_SIZE_MIN**
- **Description:** Minimum chunk size in words
- **Required:** No
- **Default:** `1000`

**CHUNK_SIZE_MAX**
- **Description:** Maximum chunk size in words
- **Required:** No
- **Default:** `1500`

**CHUNK_OVERLAP**
- **Description:** Overlap between chunks in words
- **Required:** No
- **Default:** `100`

#### Tracking Configuration

**SAMPLE_SOURCES_COUNT**
- **Description:** Number of sample sources to track
- **Required:** No
- **Default:** `5`

**TRACKING_SESSION_TTL**
- **Description:** Session TTL in seconds
- **Required:** No
- **Default:** `3600` (1 hour)

### Frontend Variables (`.env.local`)

**NEXT_PUBLIC_API_URL**
- **Description:** Backend API URL for frontend
- **Current:** `http://localhost:8000`
- **Required:** Yes
- **Options:**
  - Local: `http://localhost:8000`
  - Network: `http://192.168.29.82:8000`
  - Production: `https://your-domain.com`

---

## 🚀 Setup Instructions

### First Time Setup

1. **Copy example file (if needed):**
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` with your API keys:**
   ```bash
   nano .env
   # or
   vim .env
   # or use your favorite editor
   ```

3. **Create `.env.local` for frontend:**
   ```bash
   echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
   ```

4. **Verify configuration:**
   ```bash
   # Check backend config
   cat .env
   
   # Check frontend config
   cat .env.local
   ```

### Current Setup Status

✅ **Backend (`.env`):** Fully configured
✅ **Frontend (`.env.local`):** Created
✅ **Dataset Mode:** Enabled
✅ **API Keys:** Configured (Groq + Gemini)

**You're ready to go!** No additional setup needed.

---

## 🔄 Switching API Providers

### Using OpenAI (GPT-4)

```env
OPENAI_API_KEY=sk-...your-openai-key...
OPENAI_MODEL=gpt-4
# Remove or comment out OPENAI_BASE_URL
```

### Using Groq (Current)

```env
OPENAI_API_KEY=gsk_...your-groq-key...
OPENAI_MODEL=llama-3.3-70b-versatile
OPENAI_BASE_URL=https://api.groq.com/openai/v1
```

### Using Azure OpenAI

```env
OPENAI_API_KEY=your-azure-key
OPENAI_MODEL=gpt-4
OPENAI_BASE_URL=https://your-resource.openai.azure.com/
```

---

## 🌐 Network Access Configuration

### For Local Development

```env
# .env.local
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### For Network Access (Other Devices)

```env
# .env.local
NEXT_PUBLIC_API_URL=http://192.168.29.82:8000
```

### For Production

```env
# .env.local
NEXT_PUBLIC_API_URL=https://api.yourdomain.com
```

---

## 🔒 Security Best Practices

### DO:
✅ Keep `.env` in `.gitignore`
✅ Use environment-specific files
✅ Rotate API keys regularly
✅ Use secrets management in production
✅ Limit API key permissions

### DON'T:
❌ Commit `.env` to version control
❌ Share API keys publicly
❌ Use production keys in development
❌ Hardcode sensitive values
❌ Expose keys in frontend code

---

## 🧪 Testing Configuration

### Test Backend Configuration

```bash
# Start backend
source venv/bin/activate
uvicorn app.main:app --reload

# Test API
curl http://localhost:8000/
```

### Test Dataset Configuration

```bash
# Check dataset status
curl http://localhost:8000/dataset/dataset_status | jq

# Expected output:
# {
#   "dataset_mode_enabled": true,
#   "email_dataset_configured": true,
#   "meeting_dataset_configured": true,
#   ...
# }
```

### Test Frontend Configuration

```bash
# Start frontend
streamlit run frontend/app.py --server.port 3000

# Open browser
open http://localhost:3000
```

---

## 🐛 Troubleshooting

### Issue: "OpenAI API key not found"

**Solution:**
```bash
# Check if .env exists
ls -la .env

# Verify OPENAI_API_KEY is set
grep OPENAI_API_KEY .env

# Restart backend after changes
```

### Issue: "Dataset mode not enabled"

**Solution:**
```bash
# Check dataset configuration
grep DATASET_MODE_ENABLED .env

# Should be: DATASET_MODE_ENABLED=true
# If false or missing, add it
echo "DATASET_MODE_ENABLED=true" >> .env
```

### Issue: "Cannot connect to backend"

**Solution:**
```bash
# Check if backend is running
curl http://localhost:8000/

# Check .env.local has correct URL
cat .env.local

# Should match backend port
```

### Issue: "Dataset files not found"

**Solution:**
```bash
# Check if dataset files exist
ls -la datasets/

# Verify paths in .env
grep DATASET_PATH .env

# Should point to existing files
```

---

## 📋 Configuration Checklist

### Backend Setup
- [x] `.env` file exists
- [x] `OPENAI_API_KEY` configured
- [x] `OPENAI_MODEL` set
- [x] `OPENAI_BASE_URL` set (if using Groq)
- [x] `DATASET_MODE_ENABLED=true`
- [x] Dataset paths configured
- [x] `GEMINI_API_KEY` configured

### Frontend Setup
- [x] `.env.local` file created
- [x] `NEXT_PUBLIC_API_URL` set
- [x] URL matches backend port

### Dataset Setup
- [x] `datasets/enron_emails.csv` exists
- [x] `datasets/ami_transcripts/` exists
- [x] Paths in `.env` are correct

### Verification
- [x] Backend starts without errors
- [x] Frontend connects to backend
- [x] Dataset status endpoint works
- [x] API documentation accessible

---

## 📚 Related Documentation

- **Quick Start:** `QUICK_START.md`
- **Autonomous Features:** `AUTONOMOUS_FEATURES.md`
- **Dataset Integration:** `DATASET_INTEGRATION_GUIDE.md`
- **API Documentation:** http://localhost:8000/docs

---

## ✅ Your Current Status

**Backend Configuration:** ✅ Complete
**Frontend Configuration:** ✅ Complete
**Dataset Configuration:** ✅ Complete
**API Keys:** ✅ Configured
**All Systems:** ✅ Operational

**You're fully configured and ready to use ReqMind AI!** 🎉

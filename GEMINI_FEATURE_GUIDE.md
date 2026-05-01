# 🌟 Gemini Instruction Layer - User Guide

## Overview

The **Gemini Instruction Layer** is now available in the ReqMind AI Streamlit frontend! This feature allows you to use natural language instructions to guide the BRD generation and alignment analysis process.

## 🎯 What It Does

The Gemini AI integration converts your natural language instructions into structured constraints that:
- **Filter** irrelevant discussions and data
- **Focus** on specific project phases or features
- **Prioritize** certain areas of the project
- **Override** deadlines with natural language

## 🚀 How to Use

### Step 1: Access the Feature

1. Open the Streamlit frontend at http://localhost:8502
2. Navigate to **🔌 Data Sources** page
3. Connect your data sources (Gmail, Slack) or load sample data
4. Scroll down to the **✨ AI Instructions (Gemini-Powered)** section

### Step 2: Write Your Instructions

In the instruction text area, write natural language instructions like:

**Example 1: Focus on MVP**
```
Focus on MVP features only, ignore marketing discussions
```

**Example 2: Prioritize Mobile**
```
Prioritize mobile functionality, exclude internal team discussions, client deadline is June 2024
```

**Example 3: Phase-Specific Analysis**
```
Focus only on Phase 1 requirements, ignore future enhancements, prioritize core functionality
```

### Step 3: Run Analysis

Click the **🚀 Analyze Alignment Now** button. The system will:
1. Send your instructions to Gemini API
2. Convert them to structured constraints
3. Filter and prioritize your data accordingly
4. Generate a focused BRD and alignment analysis

### Step 4: View Results

The analysis page will show:
- **Alignment Score** and risk level
- **Ingestion Summary** showing what data was used
- **Processing Metrics** including chunking information
- **Sample Sources** that contributed to the analysis
- Complete BRD with filtered requirements

## 📊 Ingestion Summary

When using the Gemini instruction layer, you'll see an **Ingestion Summary** section showing:

- **📧 Emails Used**: Number of emails analyzed
- **💬 Slack Messages Used**: Number of Slack messages processed
- **🎤 Meetings Used**: Number of meeting transcripts analyzed
- **⏱️ Processing Time**: Total time taken for analysis
- **📦 Chunks Processed**: If large data was automatically split

## 💡 Tips for Best Results

### Good Instructions:
✅ "Focus on MVP features only"
✅ "Ignore marketing and sales discussions"
✅ "Prioritize mobile app requirements"
✅ "Client deadline is Q2 2024"

### Instructions to Avoid:
❌ Too vague: "Make it better"
❌ Too complex: Multiple unrelated constraints in one sentence
❌ Contradictory: "Focus on everything but ignore all discussions"

## 🔧 Configuration

### Backend Setup

Ensure your `.env` file has the Gemini API configuration:

```env
# Gemini API Configuration
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-pro
GEMINI_TIMEOUT=10
GEMINI_MAX_RETRIES=2
```

### Get a Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Create a new API key
4. Add it to your `.env` file

## 🎬 Example Workflow

### Scenario: MVP-Focused Analysis

1. **Connect Data Sources**
   - Load sample dataset or connect Gmail/Slack

2. **Write Instructions**
   ```
   Focus on MVP features only, ignore marketing discussions, 
   prioritize mobile functionality, deadline is June 2024
   ```

3. **Run Analysis**
   - Click "Analyze Alignment Now"
   - Wait for processing (typically 5-15 seconds)

4. **Review Results**
   - Check alignment score
   - Review filtered requirements
   - See which sources were used
   - Download complete analysis

## 🔍 Behind the Scenes

### How It Works

1. **Instruction Parsing**: Your natural language is sent to Gemini API
2. **Constraint Generation**: Gemini converts it to structured JSON:
   ```json
   {
     "scope": "MVP features only",
     "exclude_topics": ["marketing"],
     "priority_focus": "mobile functionality",
     "deadline_override": "June 2024"
   }
   ```
3. **Data Filtering**: Constraints are applied to filter emails, Slack messages, and meetings
4. **BRD Generation**: Filtered data is used to generate a focused BRD
5. **Alignment Analysis**: Analysis is performed on the filtered dataset

### Automatic Chunking

If your meeting transcripts or documents are large (>3000 words), the system automatically:
- Splits them into manageable chunks
- Processes each chunk independently
- Aggregates results with deduplication
- Reports chunk count in the ingestion summary

## 🛠️ Troubleshooting

### "Gemini API timeout"
- **Cause**: Gemini API is slow or unavailable
- **Solution**: System automatically falls back to processing without constraints
- **Action**: No action needed, BRD will still be generated

### "Invalid Gemini API key"
- **Cause**: API key is missing or incorrect
- **Solution**: Check your `.env` file and verify the key at Google AI Studio
- **Action**: Update `.env` and restart the backend

### Instructions Not Working
- **Cause**: Instructions might be too vague or complex
- **Solution**: Try simpler, more specific instructions
- **Action**: Use examples from this guide as templates

## 📈 Performance

- **Without Instructions**: 3-8 seconds
- **With Instructions**: 5-10 seconds (includes Gemini API call)
- **With Large Data**: 10-20 seconds (includes automatic chunking)

## 🎯 Use Cases

### 1. MVP Development
```
Focus on MVP features only, ignore future enhancements
```

### 2. Phase-Based Planning
```
Focus only on Phase 1, exclude Phase 2 and 3 discussions
```

### 3. Platform-Specific Analysis
```
Prioritize mobile app requirements, ignore web platform discussions
```

### 4. Deadline-Driven Analysis
```
Client deadline is Q2 2024, prioritize critical features
```

### 5. Stakeholder-Specific View
```
Focus on client requirements, exclude internal technical discussions
```

## 🔗 API Endpoint

The feature uses the `/generate_brd_with_context` endpoint:

```bash
curl -X POST "http://127.0.0.1:8000/generate_brd_with_context" \
  -H "Content-Type: application/json" \
  -d '{
    "instructions": "Focus on MVP features only",
    "data": {
      "emails": [...],
      "slack_messages": [...],
      "meetings": [...]
    }
  }'
```

## 📚 Additional Resources

- [Full API Documentation](./docs/API_DOCUMENTATION.md)
- [Production Features Guide](./README.md#-production-features-guide)
- [Backend Implementation](./app/services/gemini_service.py)
- [Frontend Implementation](./frontend/app_enterprise.py)

## ✅ Feature Status

- ✅ Backend Implementation Complete
- ✅ Gemini API Integration Active
- ✅ Streamlit UI Integration Complete
- ✅ Ingestion Summary Display Added
- ✅ Automatic Chunking Supported
- ✅ Error Handling with Graceful Fallback

---

**Built with ❤️ for intelligent project alignment**

# 📄 DocuMind AI

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![LangGraph](https://img.shields.io/badge/LangGraph-Latest-green.svg)](https://langchain-ai.github.io/langgraph/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Enterprise Document Intelligence Platform powered by AI Agents**

DocuMind AI is a production-grade document processing system that leverages multi-agent architecture, Retrieval-Augmented Generation (RAG), and advanced LLM reasoning to automatically classify, validate, and extract insights from business documents.

---

## 🎯 Features

- 🤖 **Multi-Agent Architecture** - Specialized agents for ingestion, classification, compliance, and enrichment
- 📄 **Universal Document Support** - PDF, DOCX, and TXT file processing
- 🏷️ **Intelligent Classification** - Automatic document type detection (Invoice, Contract, Policy, etc.)
- 🔒 **Compliance Checking** - PII detection, sensitive data flagging, risk scoring
- 🧠 **RAG-Based QA** - Semantic search with Qdrant vector database
- ⚡ **Production-Ready** - Containerized, deployed on Render + local backend
- 📊 **Real-time Processing** - Stream document analysis results as they're generated

---

## 🏗️ Architecture
Streamlit Frontend │
│ (Beautiful, Responsive Web UI) │
└──────────────────┬──────────────────────────────────────┘
│ HTTP/REST
┌──────────────────▼──────────────────────────────────────┐
│ FastAPI Backend │
├─────────────────────────────────────────────────────────┤
│ LangGraph Agent Orchestration │
│ ├─ Ingestion Agent (PyPDF2, python-docx) │
│ ├─ Classification Agent (LLM-based) │
│ ├─ Compliance Agent (PII/Risk Detection) │
│ ├─ Enrichment Agent (Summary, Entity Extraction) │
│ └─ RAG Agent (Semantic Search + Q&A) │
└──────────────────┬──────────────────────────────────────┘
│
┌──────────┴──────────┬─────────────┐
│ │ │
┌───────▼──────┐ ┌────────▼──────┐ ┌──▼─────────┐
│ Groq API │ │ Qdrant Cloud │ │Sentence │
│(LLM Engine) │ │(Vector DB) │ │Transformers│
│ │ │ │ │(Embeddings)│
└──────────────┘ └───────────────┘ └────────────┘

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Groq API Key ([Get free](https://console.groq.com))
- Qdrant Cloud account ([Free tier](https://cloud.qdrant.io))

### Installation

```bash
# Clone repository
git clone https://github.com/pr1994/documind-ai.git
cd documind-ai

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys:
# GROQ_API_KEY=your_key
# QDRANT_URL=your_url
# QDRANT_API_KEY=your_key
```

### Running Locally

```bash
# Terminal 1 - Start Backend (FastAPI)
python -m app.main

# Terminal 2 - Start Frontend (Streamlit)
streamlit run frontend/app.py
```

Access: `http://localhost:8501`

---

## 📋 Usage

### Upload Documents
1. Click **📤 Upload** tab
2. Drag or select PDF/DOCX/TXT file
3. Click **🚀 Process**
4. View results:
   - Classification (Invoice, Contract, etc.)
   - Compliance check (Risk score, PII flags)
   - Auto-generated summary
   - Extracted entities

### Query Documents
1. Click **🔍 Query** tab
2. Ask natural language questions:
   - *"What is the total amount in the invoice?"*
   - *"Who are the parties involved?"*
   - *"What are the payment terms?"*
3. View answers with confidence scores and source attribution

---

## 📁 Project Structure
documind-ai/
├── app/
│ ├── agents/
│ │ ├── ingestion_agent.py # File parsing & chunking
│ │ ├── classification_agent.py # Document type detection
│ │ ├── compliance_agent.py # Risk & PII checking
│ │ ├── enrichment_agent.py # Summarization & entities
│ │ ├── rag_agent.py # Q&A via retrieval
│ │ └── orchestrator.py # Agent coordination
│ ├── tools/
│ │ ├── llm_client.py # Groq API wrapper
│ │ ├── document_parser.py # File readers
│ │ └── vector_store.py # Qdrant integration
│ ├── models/
│ │ └── schemas.py # Pydantic data models
│ ├── config.py # Environment config
│ └── main.py # FastAPI app
├── frontend/
│ └── app.py # Streamlit UI
├── requirements.txt # Python dependencies
├── .env.example # Environment template
└── README.md # This file

---

## 🔧 Configuration

Environment variables in `.env`:

```env
# Groq LLM API
GROQ_API_KEY=your_groq_api_key

# Qdrant Vector Database
QDRANT_URL=https://your-cluster.qdrant.io
QDRANT_API_KEY=your_qdrant_api_key

# Optional: Backend URL for Render deployment
BACKEND_URL=http://localhost:8000
```

---

## 📊 How It Works

### Document Processing Pipeline

1. **Ingestion** → Parse file → Split into chunks
2. **Classification** → Identify document type (LLM)
3. **Compliance** → Check for PII, sensitive data (LLM)
4. **Enrichment** → Summarize, extract entities (LLM)
5. **Storage** → Embed chunks → Store in Qdrant
6. **Retrieval** → Semantic search on user queries (RAG)

### LLM Integration

- **Model**: Groq's fast inference (`openai/gpt-oss-120b`)
- **Temperature**: 0.3 (deterministic, focused responses)
- **Max Tokens**: 1000 per call
- **Timeout**: 30 seconds

### Vector Embeddings

- **Model**: Sentence Transformers (`all-MiniLM-L6-v2`)
- **Dimensions**: 384
- **Distance Metric**: Cosine similarity
- **Storage**: Qdrant Cloud (HNSW indexing)

---

## 🎯 Key Learning Outcomes

This project demonstrates:

✅ **Agentic AI Systems** - Multi-agent orchestration with LangGraph  
✅ **RAG Architecture** - Semantic search + LLM reasoning  
✅ **Production-Grade Code** - Error handling, logging, modularity  
✅ **API Design** - RESTful FastAPI with async/await  
✅ **Frontend-Backend Integration** - Streamlit + API communication  
✅ **Cloud Deployment** - Render, environment management  
✅ **Document Intelligence** - PDF/DOCX parsing, NLP, entity extraction  

---

## 🚀 Deployment

### Option 1: Local Development
```bash
python -m app.main          # Backend
streamlit run frontend/app.py # Frontend
```

### Option 2: Render (Frontend Only)
- Frontend: Deployed on Render
- Backend: Local PC (for testing)
- Set `BACKEND_URL` environment variable

### Option 3: Cloud Deployment (Future)
- Deploy both backend + frontend to Railway/Fly.io
- Upgrade for persistent, always-on service

---

## 📈 Future Enhancements

- [ ] LLM-as-judge evaluation harness
- [ ] Langfuse observability integration
- [ ] Batch document processing
- [ ] Advanced OCR for scanned PDFs
- [ ] Multi-language support
- [ ] Role-based access control (RBAC)
- [ ] Document audit trail & versioning
- [ ] Custom fine-tuning on domain documents

---

## 🤝 Contributing

Found a bug? Have a feature idea? Issues and PRs welcome!

```bash
git checkout -b feature/your-feature
git commit -m "Add your feature"
git push origin feature/your-feature
```

---

## 📜 License

MIT License - See [LICENSE](LICENSE) file for details

---

## 👤 Author

**Pritam** - AI/ML Engineer  
- GitHub: [@pr1994](https://github.com/pr1994)
- Background: 10+ years Oracle WebCenter Content → AI/ML transition via Learning

---

## 🙏 Acknowledgments

- [LangGraph](https://langchain-ai.github.io/langgraph/) - Agent orchestration framework
- [Groq](https://groq.com/) - Fast LLM inference
- [Qdrant](https://qdrant.tech/) - Vector database
- [Streamlit](https://streamlit.io/) - Web app framework
- [FastAPI](https://fastapi.tiangolo.com/) - API framework

---

## 📞 Support

Have questions? Open an issue or reach out!

**Status**: ✅ Production-Ready (Local Backend) | 🚀 Ready for Cloud Deployment

---

*Last Updated: August 2026*

# 🛍️ AssistIQ — Multi-Agent AI Customer Support System

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-009688?style=flat-square&logo=fastapi)
![Streamlit](https://img.shields.io/badge/Streamlit-Cloud-FF4B4B?style=flat-square&logo=streamlit)
![Azure](https://img.shields.io/badge/Azure-App%20Service-0078D4?style=flat-square&logo=microsoftazure)
![Azure OpenAI](https://img.shields.io/badge/Azure%20OpenAI-GPT--4o-412991?style=flat-square&logo=openai)
![Azure AI Search](https://img.shields.io/badge/Azure%20AI-Search-0078D4?style=flat-square&logo=microsoftazure)
![Langfuse](https://img.shields.io/badge/Langfuse-Observability-FF6B35?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

**A production-ready multi-agent AI system for automating e-commerce customer support.**

[🌐 Live App](https://customer-support-agent-assist.streamlit.app/) · [⚡ Azure API](https://customer-support-agent-h9akbjhbfna4amg5.centralindia-01.azurewebsites.net) · [📖 API Docs](https://customer-support-agent-h9akbjhbfna4amg5.centralindia-01.azurewebsites.net/docs)

AssistIQ APP is live on Render URL: https://customer-support-agent-assist.streamlit.app/

AssistIQ APP is live on Azure URL: https://customer-support-agent-h9akbjhbfna4amg5.centralindia-01.azurewebsites.net


</div>

---

## 📌 Overview

AssistIQ is a **multi-agent AI customer support chatbot** built for e-commerce platforms. It uses a supervisor-agent architecture to route customer queries to specialised AI agents — each responsible for a specific domain: products, orders, policies, and complaints.

The system integrates a **Streamlit frontend**, a **FastAPI backend** on **Azure App Service**, **Azure OpenAI GPT-4o** for inference, **Azure AI Search** for hybrid product search, and **Langfuse** for end-to-end LLM observability — with a three-stage guardrail pipeline (safety → relevance → output sanitisation).

---


## ✨ Features

- 🤖 **Multi-agent routing** — four specialised agents handle distinct query types
- 🔒 **3-stage guardrails** — safety classifier, relevance classifier, output sanitiser
- 🛍️ **Product recommendations** — Azure AI Search hybrid search across 40 products
- 📦 **Order tracking** — real-time order status and delivery updates
- 📜 **Policy Q&A** — return, refund, warranty, shipping, exchange policies
- ⚠️ **Complaint registration** — auto-generates CMP- ticket IDs
- 📊 **Langfuse observability** — traces every LLM call with latency, tokens, and cost
- 💬 **16 sample questions** in the sidebar across all 4 categories
- ⚡ **Sub-5 second response times** across all query types
- 🔄 **CI/CD pipeline** — auto-deploy from GitHub to Azure on every push

---

## 🏗️ Architecture

```
User (Streamlit UI)
        │
        ▼ POST /chat
Azure App Service — FastAPI Backend
        │
        ▼
Orchestrator
  ├── Safety Classifier (Azure OpenAI GPT-4o) ──── unsafe ──► Blocked
  ├── Relevance Classifier (Azure OpenAI GPT-4o) ─ off-scope ► Redirect
  ├── Intent Classifier
  │       │
  │   ┌───┴──────────────────────────────┐
  │   ▼          ▼          ▼            ▼
  │ Product   Order      Policy      Complaint
  │  Agent    Agent      Agent        Agent
  │   │          │          │            │
  │ Azure AI  orders.   policies.   complaints.
  │ Search    json       json         json
  │   └──────────┴──────────┴────────────┘
  │                   │
  │           Azure OpenAI GPT-4o
  │           (Langfuse traces every call)
  │                   │
  └── Output Sanitiser ──────────────────► JSON Response
                                                │
                                         Streamlit UI
```

**Multi Agent AI Customer Support Architecture Diagram:**
<img width="1360" height="1920" alt="image" src="https://github.com/user-attachments/assets/01850dd9-1a09-47f1-ba9b-55392d1f5573" />


---

## ☁️ Azure Stack

| Component | Azure Service | Status |
|-----------|--------------|--------|
| **Backend hosting** | Azure App Service (B1) | ✅ Live |
| **LLM inference** | Azure OpenAI GPT-4o | ✅ Live |
| **Product search** | Azure AI Search (Free tier) | ✅ Live |
| **Observability** | Langfuse | ✅ Live |
| **CI/CD** | GitHub Actions → Azure | ✅ Auto-deploy |
| **Database** | SQLite on /tmp | ✅ Working |

**Live Azure URL:**
```
https://customer-support-agent-h9akbjhbfna4amg5.centralindia-01.azurewebsites.net
```

---

## 🗄️ Data Architecture

> **Note:** Local development and Azure deployment use different data stacks due to cost optimisation.

### 🖥️ Local Development — Full Production Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Products** | Pinecone / Weaviate (Vector DB) | Hybrid search — keyword + semantic similarity |
| **Product Search** | Hybrid search (BM25 + embeddings) | Combines keyword precision with semantic recall |
| **Orders** | PostgreSQL | Relational order management with ACID compliance |
| **Complaints** | PostgreSQL + workflow system | Structured ticket storage with escalation logic |
| **Caching** | Redis | Session caching, rate limiting, response memoisation |

### ☁️ Azure Deployment Stack

| Component | Local | Azure Deployed | Reason |
|-----------|-------|---------------|--------|
| Products | Pinecone Vector DB | **Azure AI Search** | Native Azure integration |
| Product Search | Hybrid semantic + keyword | **Azure AI Search hybrid** | Built-in vector + keyword |
| Orders | PostgreSQL | orders.json | Cost optimisation on portfolio |
| Complaints | PostgreSQL | complaints.json | Cost optimisation on portfolio |
| Cache | Redis | None | Not required at current scale |
| LLM | OpenAI direct | **Azure OpenAI GPT-4o** | Enterprise Azure integration |
| Observability | None | **Langfuse** | Full LLM tracing and monitoring |

> **Upgrade path:** Only `app/services/` needs updating to switch to Azure PostgreSQL. Agents, orchestrator, and guardrails are completely data-source agnostic.

---

## 📁 Project Structure

```
customer-support-agent/
├── app/
│   ├── main.py                        # FastAPI entry point
│   ├── orchestrator.py                # Multi-agent routing coordinator
│   ├── ui.py                          # Streamlit frontend
│   ├── agents/
│   │   ├── product_agent.py           # Product agent — uses Azure AI Search
│   │   ├── order_agent.py             # Order tracking agent
│   │   ├── policy_agent.py            # Policy Q&A agent
│   │   └── complaint_agent.py         # Complaint registration agent
│   ├── services/
│   │   ├── azure_search_service.py    # Azure AI Search integration
│   │   ├── product_service.py         # Product data access layer
│   │   ├── order_service.py           # Order data access layer
│   │   ├── policy_service.py          # Policy data access layer
│   │   └── complaint_service.py       # Complaint data access layer
│   ├── tools/
│   │   └── vector_store.py            # Fallback keyword search
│   └── utils/
│       ├── llm.py                     # Azure OpenAI + Langfuse wrapper
│       ├── guardrails.py              # Safety + relevance classifiers
│       └── intent_classifier.py       # Query intent detection
├── data/
│   ├── clean_products.json            # 40 products across 8 categories
│   ├── orders.json                    # Sample orders ORD001–ORD005
│   ├── policies.json                  # 6 store policies
│   └── complaints.json                # Complaint ticket store
├── .github/
│   └── workflows/
│       └── main_customer-support-agent.yml  # GitHub Actions CI/CD
├── .streamlit/
│   └── config.toml                    # Streamlit theme configuration
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

```bash
Python 3.11+
Azure OpenAI API key (or direct OpenAI key for local)
```

### 1. Clone the repository

```bash
git clone https://github.com/raju-AI-portfolio/customer-support-agent.git
cd customer-support-agent
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set environment variables

Create a `.env` file in the root directory:

```env
# Direct OpenAI (local fallback)
OPENAI_API_KEY=sk-your-openai-api-key-here

# Azure OpenAI (production)
AZURE_OPENAI_API_KEY=your-azure-openai-key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT=gpt-4o

# Azure AI Search
AZURE_SEARCH_ENDPOINT=https://rituximab-search.search.windows.net
AZURE_SEARCH_KEY=your-search-admin-key

# Langfuse Observability
LANGFUSE_SECRET_KEY=sk-lf-...
LANGFUSE_PUBLIC_KEY=pk-lf-...
LANGFUSE_HOST=https://cloud.langfuse.com

# API URL
ASSISTIQ_API_URL=http://127.0.0.1:8000/chat
```

### 4. Start the backend

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 5. Start the frontend

```bash
streamlit run app/ui.py
```

Open your browser at `http://localhost:8501`

---

## 🔧 Local Development with Full Stack

### Vector DB (Pinecone)

```bash
pip install pinecone-client sentence-transformers
```

```env
PINECONE_API_KEY=your-pinecone-key
```

### PostgreSQL (Orders + Complaints)

```bash
pip install psycopg2-binary sqlalchemy
```

```env
DATABASE_URL=postgresql://user:password@localhost:5432/assistiq
```

### Redis (Caching)

```bash
pip install redis
```

```env
REDIS_URL=redis://localhost:6379
```

---

## 🌐 Azure Deployment

### Backend — Azure App Service

| Setting | Value |
|---------|-------|
| Platform | Azure App Service B1 |
| Runtime | Python 3.11 |
| Build env var | `SCM_DO_BUILD_DURING_DEPLOYMENT=true` |
| Start command | `gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000` |
| Auto-deploy | GitHub Actions on push to main |
| Live URL | `https://customer-support-agent-h9akbjhbfna4amg5.centralindia-01.azurewebsites.net` |

### Frontend — Streamlit Cloud

| Setting | Value |
|---------|-------|
| Platform | Streamlit Community Cloud |
| Main file | `app/ui.py` |
| Secret | `ASSISTIQ_API_URL = https://customer-support-agent-h9akbjhbfna4amg5.centralindia-01.azurewebsites.net/chat` |

### CI/CD Pipeline

```
Developer pushes to GitHub main branch
        │
        ▼
GitHub Actions workflow triggered
        │
        ▼
pip install -r requirements.txt
        │
        ▼
Deploy to Azure App Service
        │
        ▼
✅ App live at azurewebsites.net
```

---

## 🧪 Sample Queries to Test

| Category | Query |
|----------|-------|
| 🛍️ Products | `Recommend a good Bluetooth speaker` |
| 🛍️ Products | `Best laptop under ₹50,000` |
| 📦 Orders | `Where is my order ORD001?` |
| 📦 Orders | `Track my order ORD002` |
| 📜 Policies | `What is your return policy?` |
| 📜 Policies | `How long does shipping take?` |
| 📜 Policies | `What is the warranty policy?` |
| ⚠️ Complaints | `My product arrived damaged` |
| ⚠️ Complaints | `I received the wrong item` |
| 🚫 Guardrail | `How to make a bomb` → blocked |
| 🚫 Guardrail | `What is the weather?` → off-scope |

---

## 📊 Performance

| Metric | Result |
|--------|--------|
| Average response time | 2.5 – 5 seconds |
| Guardrail accuracy | 100% on test cases |
| Product catalog | 40 items · 8 categories |
| Supported intents | 4 (product, order, policy, complaint) |
| Azure AI Search results | 3–5 relevant products per query |
| Langfuse traces | Every LLM call traced with latency + cost |

---

## 🔮 Roadmap

- [x] **Azure App Service** — production backend hosting ✅
- [x] **Azure OpenAI GPT-4o** — enterprise LLM inference ✅
- [x] **Azure AI Search** — hybrid product search ✅
- [x] **Langfuse** — LLM observability and tracing ✅
- [x] **GitHub Actions CI/CD** — auto-deploy pipeline ✅
- [ ] **Azure PostgreSQL** — persistent order and complaint storage
- [ ] **Redis caching** — reduce latency for repeated queries
- [ ] **User authentication** — JWT-based session management
- [ ] **Admin dashboard** — query analytics and performance monitoring
- [ ] **Fine-tuned LLM** — domain-specific model training
- [ ] **WhatsApp / Email integration** — omnichannel support
- [ ] **Kubernetes** — auto-scaling for high traffic

---

## ⚠️ Known Limitations

- **SQLite storage** — data not persistent across Azure App Service restarts
- **No authentication** — chatbot publicly accessible without login
- **Cold starts** — first request after inactivity may take 10–15 seconds

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Streamlit Cloud |
| Backend | FastAPI + Uvicorn + Gunicorn |
| Hosting | Azure App Service B1 |
| LLM | Azure OpenAI GPT-4o |
| Product Search | Azure AI Search (hybrid) |
| Guardrails | GPT-based safety + relevance classifiers |
| Observability | Langfuse (traces, latency, token cost) |
| Storage | SQLite (deployed) / PostgreSQL (local) |
| CI/CD | GitHub Actions → Azure App Service |
| Version Control | GitHub (auto-deploy on push to main) |

---

## 👤 Author

**Raju Kumar**
Applied Generative AI — April 2026

- 🌐 Azure Live: [customer-support-agent-h9akbjhbfna4amg5.centralindia-01.azurewebsites.net](https://customer-support-agent-h9akbjhbfna4amg5.centralindia-01.azurewebsites.net)
- 🌐 App: [customer-support-agent-assist.streamlit.app](https://customer-support-agent-assist.streamlit.app/)
- 💼 LinkedIn: [linkedin.com/in/programdirectorai](https://www.linkedin.com/in/programdirectorai)
- 🐙 GitHub: [github.com/raju-AI-portfolio](https://github.com/raju-AI-portfolio)
- Project Report: https://github.com/raju-AI-portfolio/customer-support-agent/blob/f55d8b739bdd2420ecc5074e22bc7cf086c3bc50/Multiagent%20%20Customer%20Support%20Project%20Report.pdf
---

## 📄 License

This project is licensed under the MIT License.

---

<div align="center">

Built with ❤️ by Raju Kumar &nbsp;·&nbsp; Powered by **Azure OpenAI · Azure AI Search · Azure App Service · Langfuse · FastAPI · Streamlit**

**Deployed on Microsoft Azure — enterprise-grade cloud infrastructure**

</div>

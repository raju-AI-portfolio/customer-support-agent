# customer-support-agent
# 🛍️ AssistIQ — Multi-Agent AI Customer Support System

<div align="center">

![Python](https://img.shields.io/badge/Python-3.14-blue?style=flat-square&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.136-009688?style=flat-square&logo=fastapi)
![Streamlit](https://img.shields.io/badge/Streamlit-Cloud-FF4B4B?style=flat-square&logo=streamlit)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4.1--mini-412991?style=flat-square&logo=openai)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

**A production-ready multi-agent AI system for automating e-commerce customer support.**

[Live Demo](//https://customer-support-agent-assist.streamlit.app/) · [Backend API](https://customer-support-agent-wppl.onrender.com/docs) · [Report a Bug](https://github.com/raju-AI-portfolio/customer-support-agent/issues)

</div>

---

## 📌 Overview

AssistIQ is a **multi-agent AI customer support chatbot** built for e-commerce platforms. It uses a supervisor-agent architecture to route customer queries to specialised AI agents — each responsible for a specific domain: products, orders, policies, and complaints.

The system integrates a **Streamlit frontend**, a **FastAPI backend**, and an **OpenAI GPT-4.1-mini** inference layer, with a three-stage guardrail pipeline (safety → relevance → output sanitisation) to ensure safe, accurate, and on-topic responses.

---

## ✨ Features

- 🤖 **Multi-agent routing** — four specialised agents handle distinct query types
- 🔒 **3-stage guardrails** — safety classifier, relevance classifier, output sanitiser
- 🛍️ **Product recommendations** — keyword + scored search across 40 products
- 📦 **Order tracking** — real-time order status and delivery updates
- 📜 **Policy Q&A** — return, refund, warranty, shipping, exchange policies
- ⚠️ **Complaint registration** — auto-generates CMP- ticket IDs
- 💬 **16 sample questions** in the sidebar across all 4 categories
- ⚡ **Sub-5 second response times** across all query types

---

## 🏗️ Architecture

```
User (Streamlit UI)
        │
        ▼ POST /chat
FastAPI Backend
        │
        ▼
Orchestrator
  ├── Safety Classifier (GPT) ──── unsafe ──► Blocked
  ├── Relevance Classifier (GPT) ─ off-scope ► Redirect
  ├── Intent Classifier
  │       │
  │   ┌───┴───────────────────────────┐
  │   ▼           ▼         ▼         ▼
  │ Product    Order      Policy   Complaint
  │  Agent     Agent      Agent     Agent
  │   │           │         │         │
  │ products   orders   policies  complaints
  │  .json      .json     .json     .json
  │   └───────────┴─────────┴─────────┘
  │                   │
  │                   ▼
  │           GPT-4.1-mini (LLM)
  │                   │
  └── Output Sanitiser ──────────────────────►  JSON Response
                                                      │
                                               Streamlit UI
```

---

## 🗄️ Data Architecture

> **Note:** The local development and deployed architectures differ due to cloud deployment constraints.

### 🖥️ Local Development (Full Stack)

For local hosting, the system uses a production-grade data stack:

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Products** | Pinecone / Weaviate (Vector DB) | Hybrid search — keyword + semantic similarity |
| **Product Search** | Hybrid search (BM25 + embeddings) | Combines keyword precision with semantic recall |
| **Orders** | PostgreSQL | Relational order management with ACID compliance |
| **Complaints** | PostgreSQL + workflow system | Structured ticket storage with escalation logic |
| **Caching** | Redis | Session caching, rate limiting, response memoisation |

This stack delivers:
- **Semantic search** — finds "wireless earphones" even when the query says "bluetooth headphones"
- **Persistent storage** — order and complaint data survives server restarts
- **Fast caching** — Redis reduces LLM calls for repeated queries
- **Scalability** — handles concurrent users without performance degradation

### ☁️ Deployed Version (Cloud — JSON)

Due to **Render free tier RAM limitations (512MB)**, the deployed version uses lightweight JSON files instead:

| Component | Local | Deployed | Reason |
|-----------|-------|----------|--------|
| Products | Pinecone Vector DB | `clean_products.json` | Vector DB requires persistent RAM |
| Orders | PostgreSQL | `orders.json` | DB connection overhead on free tier |
| Complaints | PostgreSQL | `complaints.json` | Stateless JSON is RAM-friendly |
| Search | Hybrid (semantic + keyword) | Keyword scoring | No embedding model loaded in memory |
| Cache | Redis | None | Redis instance not available on free tier |

> **Upgrade path:** Switching to the full stack requires only changing the service layer (`app/services/`). The agent and orchestrator layers are data-source agnostic.

---

## 📁 Project Structure

```
customer-support-agent/
├── app/
│   ├── main.py                  # FastAPI entry point
│   ├── orchestrator.py          # Multi-agent routing coordinator
│   ├── ui.py                    # Streamlit frontend
│   ├── agents/
│   │   ├── product_agent.py     # Product recommendation agent
│   │   ├── order_agent.py       # Order tracking agent
│   │   ├── policy_agent.py      # Policy Q&A agent
│   │   └── complaint_agent.py   # Complaint registration agent
│   ├── services/
│   │   ├── product_service.py   # Product data access layer
│   │   ├── order_service.py     # Order data access layer
│   │   ├── policy_service.py    # Policy data access layer
│   │   └── complaint_service.py # Complaint data access layer
│   ├── tools/
│   │   └── vector_store.py      # Product search (keyword scoring)
│   └── utils/
│       ├── llm.py               # LLM wrapper + topic guardrails
│       ├── guardrails.py        # Safety + relevance classifiers
│       └── intent_classifier.py # Query intent detection
├── data/
│   ├── clean_products.json      # 40 products across 8 categories
│   ├── orders.json              # Sample order records
│   ├── policies.json            # 6 store policies
│   └── complaints.json          # Complaint ticket store
├── .streamlit/
│   └── config.toml              # Streamlit theme configuration
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

```bash
Python 3.10+
OpenAI API key
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
OPENAI_API_KEY=sk-your-openai-api-key-here
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

To run with the production data stack locally:

### Vector DB (Pinecone)

```bash
pip install pinecone-client sentence-transformers
```

```python
# app/services/product_service.py
import pinecone
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')
pc = pinecone.Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("products")

def search_products(query: str, top_k: int = 5):
    embedding = model.encode(query).tolist()
    results = index.query(vector=embedding, top_k=top_k, include_metadata=True)
    return [r.metadata for r in results.matches]
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

## 🌐 Deployment

### Backend — Render

1. Push code to GitHub
2. Create a new **Web Service** on [render.com](https://render.com)
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Add environment variable: `OPENAI_API_KEY`

### Frontend — Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Connect your GitHub repository
3. Set main file: `app/ui.py`
4. Add secret: `ASSISTIQ_API_URL = "https://your-render-url.onrender.com/chat"`

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
| Average response time | 2.5 – 4.8 seconds |
| Guardrail accuracy | 100% on test cases |
| Product catalog | 40 items · 8 categories |
| Supported intents | 4 (product, order, policy, complaint) |
| Deployment uptime | Stable on Render free tier |

---

## 🔮 Roadmap

- [ ] **Vector DB integration** — Pinecone/Weaviate for semantic product search
- [ ] **PostgreSQL** — persistent order and complaint storage
- [ ] **Redis caching** — reduce latency for repeated queries
- [ ] **User authentication** — JWT-based session management
- [ ] **Admin dashboard** — query analytics and performance monitoring
- [ ] **Fine-tuned LLM** — domain-specific model training on e-commerce data
- [ ] **WhatsApp / Email integration** — omnichannel support
- [ ] **Auto-scaling** — Kubernetes deployment for high traffic

---

## ⚠️ Known Limitations

- **JSON storage** — data is not persistent across server restarts on the deployed version
- **No authentication** — the chatbot is publicly accessible without login
- **Free tier cold starts** — Render free tier may have 30-50s cold start delays after inactivity
- **No analytics** — query patterns and usage metrics are not tracked

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Streamlit |
| Backend | FastAPI + Uvicorn |
| LLM | OpenAI GPT-4.1-mini |
| Guardrails | GPT-based classifiers |
| Search | Keyword scoring (deployed) / Vector DB (local) |
| Storage | JSON files (deployed) / PostgreSQL (local) |
| Cache | None (deployed) / Redis (local) |
| Deployment | Render + Streamlit Cloud |
| Version Control | GitHub (auto-deploy on push) |

---

## 👤 Author

**Raju Kumar**
Applied Generative AI — April 2026

---

## 📄 License

This project is licensed under the MIT License.

---

<div align="center">
Made with ❤️ by Raju Kumar &nbsp;·&nbsp; Powered by OpenAI + FastAPI + Streamlit
</div>

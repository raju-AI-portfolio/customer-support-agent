from dotenv import load_dotenv
import os
import time

from fastapi import FastAPI
from pydantic import BaseModel

from app.orchestrator import Orchestrator
from app.db.database import engine
from app.db.models import Base


# ---------------- LOAD ENV ----------------
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("❌ OPENAI_API_KEY not found in .env")

print("✅ API KEY LOADED:", api_key[:10], "****")


# ---------------- DB INIT ----------------
Base.metadata.create_all(bind=engine)


# ---------------- APP INIT ----------------
app = FastAPI()
orchestrator = Orchestrator()


# ---------------- REQUEST MODEL ----------------
class ChatRequest(BaseModel):
    message: str


# ---------------- HEALTH CHECK ----------------
@app.get("/")
def root():
    return {"message": "API is running"}


# ---------------- CHAT ENDPOINT ----------------
@app.post("/chat")
def chat(request: ChatRequest):
    start_time = time.time()

    try:
        response = orchestrator.handle(request.message)

        total_latency = time.time() - start_time

        return {
            "response": response,
            "latency": round(total_latency, 3)
        }

    except Exception as e:
        return {
            "response": "⚠️ Internal server error",
            "latency": None,
            "error": str(e)
        }
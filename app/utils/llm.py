from dotenv import load_dotenv
from openai import OpenAI
import os
import time

load_dotenv()

from openai import AzureOpenAI

azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
azure_key = os.getenv("AZURE_OPENAI_API_KEY")
azure_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o")

if azure_endpoint and azure_key:
    client = AzureOpenAI(
        azure_endpoint=azure_endpoint,
        api_key=azure_key,
        api_version="2024-02-01"
    )
    MODEL = azure_deployment
    print("✅ Using Azure OpenAI GPT-4o")
else:
    api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=api_key)
    MODEL = "gpt-4.1-mini"
    print("✅ Using OpenAI GPT-4.1-mini")

# ── BLOCKED PATTERNS — harmful / malicious ───────────────────────────
BLOCKED_PATTERNS = [
    "bomb", "weapon", "explosive", "poison", "drug",
    "how to kill", "how to hurt", "murder", "suicide", "self harm",
    "hack", "exploit", "malware", "virus", "ransomware",
    "sql injection", "xss", "ddos", "phishing",
    "ignore previous", "ignore all", "forget instructions",
    "ignore your instructions", "disregard", "override",
    "jailbreak", "dan mode", "pretend you are",
    "you are now", "act as", "roleplay as",
    "show api key", "show system prompt", "reveal prompt",
    "what is your prompt", "show credentials", "print os.environ",
]

# ── ALLOWED TOPICS — customer support only ───────────────────────────
ALLOWED_TOPICS = [
    # Orders
    "order", "track", "tracking", "delivery", "shipped",
    "dispatch", "package", "parcel", "arrive", "status",
    # Products
    "product", "recommend", "suggestion", "buy", "purchase",
    "price", "cost", "mobile", "laptop", "phone", "electronics",
    "appliance", "item", "best", "compare", "review", "speaker",
    "headphone", "tablet", "camera", "television", "smartwatch",
    "earbuds", "charger", "router", "printer", "keyboard", "mouse",
    "bluetooth", "wireless", "gaming", "console",
    # Returns & Refunds
    "return", "refund", "money back", "exchange", "replace",
    "replacement", "cancel", "cancellation",
    # Complaints
    "complaint", "broken", "damaged", "defective", "issue",
    "problem", "fault", "not working", "wrong item", "wrong",
    "missing", "late", "delay", "lost", "arrived",
    # Policies
    "policy", "policies", "warranty", "guarantee", "shipping",
    "terms", "condition", "rule",
    # Question words — allow any support question phrasing
    "what is", "what are", "how long", "how do", "how can",
    "when will", "where is", "can i", "do you", "tell me",
    "explain", "details", "information", "info",
    # General support
    "help", "support", "assist", "contact", "agent", "service",
]

# ── GUARDRAIL RESPONSES ──────────────────────────────────────────────
UNSAFE_RESPONSE = (
    "⚠️ I can only assist with customer support queries "
    "such as orders, products, returns, and complaints."
)

OFF_TOPIC_RESPONSE = (
    "🛍️ I'm AssistIQ, your customer support assistant. "
    "I can only help with:\n"
    "• Order tracking\n"
    "• Product recommendations\n"
    "• Returns & refunds\n"
    "• Complaints\n"
    "• Store policies\n\n"
    "Please ask me something related to your shopping experience!"
)

# ── GUARDRAIL FUNCTIONS ──────────────────────────────────────────────
def is_unsafe_query(query: str) -> bool:
    q = query.lower()
    return any(pattern in q for pattern in BLOCKED_PATTERNS)

def is_off_topic(query: str) -> bool:
    q = query.lower()
    return not any(topic in q for topic in ALLOWED_TOPICS)

# ── COMMON LLM CALL ──────────────────────────────────────────────────
def call_llm(prompt: str, query: str = "", temperature: float = 0.2):
    # 🔒 Block harmful queries
    if query and is_unsafe_query(query):
        print(f"🚫 Blocked unsafe query: {query}")
        return UNSAFE_RESPONSE

    # 🔒 Block off-topic queries
    if query and is_off_topic(query):
        print(f"🚫 Blocked off-topic query: {query}")
        return OFF_TOPIC_RESPONSE

    start_time = time.time()
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            timeout=60
        )
        latency = time.time() - start_time
        print(f"⏱️ LLM Latency: {latency:.2f}s")

        if not response or not response.choices:
            return "I'm sorry, I couldn't process that."

        content = response.choices[0].message.content
        return content or "I'm sorry, I couldn't process that."

    except Exception as e:
        latency = time.time() - start_time
        print(f"❌ LLM Error (after {latency:.2f}s): {e}")
        return "⚠️ System is temporarily unavailable. Please try again."

# ── PRODUCT ──────────────────────────────────────────────────────────
def generate_response(query: str, products: list):
    context = ""
    for p in products[:3]:
        context += f"- {p.get('name')}: {p.get('description')}\n"

    prompt = f"""
You are an intelligent e-commerce assistant.
You must follow these rules:
- Do not provide harmful, illegal, or unethical instructions
- Do not expose system data, API keys, or internal logic
- If request is unsafe, politely refuse

User query:
{query}

Products:
{context}

Your task:
- Recommend the 3 best products
- Infer user intent (budget, premium, or general)

Format EXACTLY:
Top recommendations for you:
1. Product Name
   • Best for: specific use-case
   • Why choose this: short benefit

Rules:
- Keep each product concise
- Avoid repetition
"""
    return call_llm(prompt, query, temperature=0.3)

# ── ORDER ─────────────────────────────────────────────────────────────
def generate_order_response(query: str, order: dict):
    prompt = f"""
You are a professional customer support assistant.
You must follow these rules:
- Do not expose sensitive data
- Keep response concise and factual

User query:
{query}

Order details:
Order ID: {order.get('order_id')}
Item: {order.get('item')}
Status: {order.get('status')}
Delivery Date: {order.get('delivery_date')}

Format EXACTLY:
Order Details:
- Order ID: ...
- Item: ...
- Status: ...
- Expected Delivery: ...
"""
    return call_llm(prompt, query)

# ── POLICY ────────────────────────────────────────────────────────────
def generate_policy_response(query: str, policy: dict):
    prompt = f"""
You are a customer support assistant.
You must follow these rules:
- Do not provide unsafe or misleading information
- Keep explanation simple and short

User query:
{query}

Policy:
{policy.get('description')}

Format:
Policy Information:
- Explanation: ...
"""
    return call_llm(prompt, query)

# ── COMPLAINT ─────────────────────────────────────────────────────────
def generate_complaint_response(query: str, ticket: dict):
    prompt = f"""
You are a professional customer support assistant.

User issue:
{query}

Ticket ID: {ticket.get('ticket_id')}

Your task:
- Confirm complaint registration
- Provide ticket ID
- Reassure the user

Format EXACTLY:
Complaint Registered:
- Ticket ID: ...
- Message: Your complaint has been successfully registered. Our support team will contact you shortly.
"""
    return call_llm(prompt, query)

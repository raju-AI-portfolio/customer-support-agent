from dotenv import load_dotenv
from openai import OpenAI
import os
import time

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("❌ OPENAI_API_KEY not found")

client = OpenAI(api_key=api_key)


# ---------------- COMMON CALL (WITH LATENCY + SAFETY) ----------------
def call_llm(prompt: str, temperature: float = 0.2):
    start_time = time.time()

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            timeout=15  # 🔥 prevent hanging
        )

        latency = time.time() - start_time
        print(f"⏱️ LLM Latency: {latency:.2f}s")

        # 🔥 Safe extraction
        if not response or not response.choices:
            return "I'm sorry, I couldn't process that."

        content = response.choices[0].message.content
        return content or "I'm sorry, I couldn't process that."

    except Exception as e:
        latency = time.time() - start_time
        print(f"❌ LLM Error (after {latency:.2f}s): {e}")
        return "⚠️ System is temporarily unavailable. Please try again."


# ---------------- PRODUCT ----------------
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

    return call_llm(prompt, temperature=0.3)


# ---------------- ORDER ----------------
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

• Order ID: ...
• Item: ...
• Status: ...
• Expected Delivery: ...
"""

    return call_llm(prompt)


# ---------------- POLICY ----------------
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

• Explanation: ...
"""

    return call_llm(prompt)


# ---------------- COMPLAINT ----------------
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

• Ticket ID: ...
• Message: Your complaint has been successfully registered. Our support team will contact you shortly.
"""

    return call_llm(prompt)

from dotenv import load_dotenv
import os
import json
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def classify_intent(query: str):
    prompt = f"""
You are an intent classification system for a customer support assistant.

Classify the user query into ONE of these intents:
- product → product search or recommendation
- order → order status or tracking
- policy → return/refund/cancellation policy
- complaint → damaged product, issue, problem

Return ONLY valid JSON in this format:
{{"intent": "<intent>"}}

User query:
{query}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        content = response.choices[0].message.content
        result = json.loads(content)

        intent = result.get("intent", "product")

        # 🔥 Validate intent (important)
        if intent not in ["product", "order", "policy", "complaint"]:
            return "product"

        return intent

    except Exception:
        # 🔥 Fail-safe fallback
        return "product"
from app.utils.intent_classifier import classify_intent
from app.agents.order_agent import OrderAgent
from app.agents.product_agent import ProductAgent
from app.agents.policy_agent import PolicyAgent
from app.agents.complaint_agent import ComplaintAgent
from app.utils.guardrails import (
    classify_safety,
    classify_relevance,
    blocked_response,
    out_of_scope_response,
    sanitize_output,
)


class Orchestrator:
    def __init__(self):
        self.order_agent = OrderAgent()
        self.product_agent = ProductAgent()
        self.policy_agent = PolicyAgent()
        self.complaint_agent = ComplaintAgent()

    def handle(self, query: str):

        # 🔥 STEP 1: SAFETY CHECK
        safety = classify_safety(query)
        if safety == "unsafe":
            return blocked_response()

        # 🔥 STEP 2: RELEVANCE CHECK
        relevance = classify_relevance(query)
        if relevance == "out_of_scope":
            return out_of_scope_response()

        # 🔥 STEP 3: INTENT CLASSIFICATION
        intent = classify_intent(query)

        # 🔥 STEP 4: ROUTING
        if intent == "order":
            response = self.order_agent.handle(query)

        elif intent == "product":
            response = self.product_agent.handle(query)

        elif intent == "policy":
            response = self.policy_agent.handle(query)

        elif intent == "complaint":
            response = self.complaint_agent.handle(query)

        else:
            response = "I couldn't understand your request."

        # 🔥 STEP 5: OUTPUT GUARD
        return sanitize_output(response)
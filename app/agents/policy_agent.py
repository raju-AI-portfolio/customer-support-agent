from app.services.policy_service import PolicyService
from app.utils.llm import generate_policy_response


class PolicyAgent:
    def __init__(self):
        self.service = PolicyService()

    def handle(self, query: str):
        policy = self.service.search_policy(query)

        if not policy:
            return "I'm sorry, I couldn't find relevant policy information."

        return generate_policy_response(query, policy)
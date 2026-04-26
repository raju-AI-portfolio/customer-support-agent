from app.services.complaint_service import ComplaintService
from app.utils.llm import generate_complaint_response


class ComplaintAgent:
    def __init__(self):
        self.service = ComplaintService()

    def handle(self, query: str):
        # 🔥 Create ticket (action)
        ticket = self.service.create_ticket(query)

        # 🔥 Format with LLM
        return generate_complaint_response(query, ticket)
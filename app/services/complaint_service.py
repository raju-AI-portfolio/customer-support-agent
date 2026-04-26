import uuid
from app.db.database import SessionLocal
from app.db.models import Complaint


class ComplaintService:
    def create_ticket(self, query: str):
        db = SessionLocal()
        try:
            ticket_id = str(uuid.uuid4())[:8]

            complaint = Complaint(
                ticket_id=ticket_id,
                issue=query,
                status="open"
            )

            db.add(complaint)
            db.commit()

            return {
                "ticket_id": ticket_id,
                "issue": query,
                "status": "open"
            }
        finally:
            db.close()
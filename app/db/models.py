from sqlalchemy import Column, String
from app.db.database import Base


class Order(Base):
    __tablename__ = "orders"

    order_id = Column(String, primary_key=True, index=True)
    item = Column(String)
    status = Column(String)
    delivery_date = Column(String)


class Complaint(Base):
    __tablename__ = "complaints"

    ticket_id = Column(String, primary_key=True, index=True)
    issue = Column(String)
    status = Column(String)
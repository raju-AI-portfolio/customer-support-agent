from app.db.database import SessionLocal
from app.db.models import Order


def seed():
    db = SessionLocal()

    orders = [
        Order(order_id="ORD123", item="Mixer Grinder", status="Shipped", delivery_date="2026-04-28"),
        Order(order_id="ORD456", item="Air Fryer", status="Delivered", delivery_date="2026-04-20"),
        Order(order_id="ORD789", item="Vacuum Cleaner", status="Processing", delivery_date="2026-04-30"),
    ]

    for order in orders:
        existing = db.query(Order).filter(Order.order_id == order.order_id).first()
        if not existing:
            db.add(order)

    db.commit()
    db.close()


if __name__ == "__main__":
    seed()
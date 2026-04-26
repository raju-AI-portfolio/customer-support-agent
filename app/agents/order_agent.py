import re
from app.services.order_service import OrderService
from app.utils.llm import generate_order_response


class OrderAgent:
    def __init__(self):
        self.service = OrderService()

    def extract_order_id(self, query: str):
        match = re.search(r'ord\d+', query.lower())
        return match.group(0).upper() if match else None

    def handle(self, query: str):
        order_id = self.extract_order_id(query)

        # ❗ Step 1: Missing order ID
        if not order_id:
            return "Please provide your order ID (e.g., ORD123)."

        # ❗ Step 2: Fetch order from service
        order = self.service.get_order(order_id)

        # ❗ Step 3: Order not found
        if not order:
            return f"Order {order_id} not found."

        # ✅ Step 4: LLM formatted response
        return generate_order_response(query, order)
import json
import os

class OrderService:
    def __init__(self):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        file_path = os.path.join(BASE_DIR, "data", "orders.json")

        if os.path.exists(file_path):
            with open(file_path) as f:
                data = json.load(f)
                # Handle both {"orders": [...]} and plain [...] formats
                self.orders = data.get("orders", data) if isinstance(data, dict) else data
        else:
            # File missing → start empty instead of crashing
            self.orders = []

    def get_order(self, order_id: str):
        for order in self.orders:
            if order["order_id"] == order_id:
                return order
        return None

import json
import os

class OrderService:
    def __init__(self):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        file_path = os.path.join(BASE_DIR, "data", "orders.json")

        with open(file_path) as f:
            self.orders = json.load(f)

    def get_order(self, order_id: str):
        for order in self.orders:
            if order["order_id"] == order_id:
                return order
        return None
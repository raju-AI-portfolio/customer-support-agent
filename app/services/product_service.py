import json
import os

class ProductService:
    def __init__(self):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        file_path = os.path.join(BASE_DIR, "data", "clean_products.json")

        if os.path.exists(file_path):
            with open(file_path) as f:
                data = json.load(f)
                # Handle both {"products": [...]} and plain [...] formats
                self.products = data.get("products", data) if isinstance(data, dict) else data
        else:
            self.products = []

    def search_products(self, query: str):
        query_lower = query.lower()

        # Step 1 — match by category
        category_matches = [
            p for p in self.products
            if p.get("category", "").lower() in query_lower
        ]
        if category_matches:
            return category_matches[:3]

        # Step 2 — match by brand name
        brand_matches = [
            p for p in self.products
            if p.get("brand", "").lower() in query_lower
        ]
        if brand_matches:
            return brand_matches[:3]

        # Step 3 — match by product name words
        name_matches = [
            p for p in self.products
            if any(
                word in query_lower
                for word in p.get("name", "").lower().split()
                if len(word) > 3
            )
        ]
        if name_matches:
            return name_matches[:3]

        # Step 4 — fallback: return top 3 rated products
        sorted_products = sorted(
            self.products,
            key=lambda x: x.get("rating", 0),
            reverse=True
        )
        return sorted_products[:3]

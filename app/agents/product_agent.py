from app.tools.vector_store import search_products
from app.utils.llm import generate_response

class ProductAgent:
    def handle(self, query: str):
        results = search_products(query)

        if not results:
            return "Sorry, I couldn't find relevant products."

        # 🔥 LLM layer
        return generate_response(query, results)
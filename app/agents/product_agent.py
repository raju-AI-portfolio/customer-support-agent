import os
from app.services.azure_search_service import search_products as azure_search
from app.tools.vector_store import search_products as json_search

def search_products(query):
    if os.getenv("AZURE_SEARCH_KEY"):
        results = azure_search(query)
        if results:
            return results
    return json_search(query)
from app.utils.llm import generate_response

class ProductAgent:
    def handle(self, query: str):
        results = search_products(query)

        if not results:
            return "Sorry, I couldn't find relevant products."

        # 🔥 LLM layer
        return generate_response(query, results)
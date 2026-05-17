import os
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential

SEARCH_ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT", "https://rituximab-search.search.windows.net")
SEARCH_KEY = os.getenv("AZURE_SEARCH_KEY", "")
INDEX_NAME = "assistiq-products"

def search_products(query: str, top: int = 5):
    try:
        client = SearchClient(SEARCH_ENDPOINT, INDEX_NAME, AzureKeyCredential(SEARCH_KEY))
        results = client.search(search_text=query, top=top)
        products = []
        for r in results:
            products.append({
                "name": r.get("name", ""),
                "description": r.get("description", ""),
                "category": r.get("category", ""),
                "price": r.get("price", 0),
            })
        return products
    except Exception as e:
        print(f"Azure Search error: {e}")
        return []

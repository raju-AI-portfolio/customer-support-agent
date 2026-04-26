import json
import os

# ---------------- LOAD DATA ----------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
file_path = os.path.join(BASE_DIR, "data", "clean_products.json")

with open(file_path) as f:
    products = json.load(f)

# 🔴 DEBUG (kept for visibility)
print("🚨 VECTOR STORE LOADED")
print("🚨 FILE:", file_path)
print("🚨 COUNT:", len(products))
print("🚨 SAMPLE:", products[0].get("name"))


# ---------------- SIMPLE SEARCH ----------------
def search_products(query: str, top_k=5):
    query = query.lower()

    scored = []

    for product in products:
        text = (
            (product.get("name", "") + " " + product.get("description", ""))
            .lower()
        )

        # simple relevance scoring
        score = 0

        for word in query.split():
            if word in text:
                score += 1

        if score > 0:
            scored.append((score, product))

    # sort by score
    scored.sort(key=lambda x: x[0], reverse=True)

    # fallback if nothing found
    if not scored:
        return products[:top_k]

    return [p[1] for p in scored[:top_k]]
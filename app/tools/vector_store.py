import os
import json

# ---------------- PATH SETUP ----------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FILE_PATH = os.path.join(BASE_DIR, "data", "clean_products.json")


# ---------------- LOAD FUNCTION (SAFE) ----------------
def load_products():
    try:
        with open(FILE_PATH, "r") as f:
            products = json.load(f)

        print("✅ PRODUCTS LOADED")
        print("📂 FILE:", FILE_PATH)
        print("📦 COUNT:", len(products))

        return products

    except Exception as e:
        print("❌ ERROR LOADING PRODUCTS:", str(e))
        return []


# ---------------- SIMPLE SEARCH ----------------
def search_products(query: str, top_k=5):
    products = load_products()

    if not products:
        return []

    query = query.lower()
    scored = []

    for product in products:
        text = (
            (product.get("name", "") + " " + product.get("description", ""))
            .lower()
        )

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

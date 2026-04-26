from sentence_transformers import SentenceTransformer
import json
import os
import numpy as np
from numpy.linalg import norm

model = SentenceTransformer("all-MiniLM-L6-v2")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
file_path = os.path.join(BASE_DIR, "data", "clean_products.json")

with open(file_path) as f:
    products = json.load(f)

# 🔴 PROOF THIS FILE IS USED
print("🚨 VECTOR STORE LOADED")
print("🚨 FILE:", file_path)
print("🚨 COUNT:", len(products))
print("🚨 SAMPLE:", products[0].get("name"))

texts = [(p.get("name","") + " " + p.get("description","")).strip() for p in products]
embeddings = model.encode(texts)

def cosine(a, b):
    return np.dot(a, b) / (norm(a) * norm(b))

def search_products(query: str, top_k=5):
    q_emb = model.encode([query])[0]
    scored = []

    for i, emb in enumerate(embeddings):
        score = cosine(emb, q_emb)
        scored.append((score, products[i]))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [p[1] for p in scored[:top_k]]
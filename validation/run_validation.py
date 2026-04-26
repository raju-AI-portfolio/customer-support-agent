import json
from app.orchestrator import Orchestrator

# ---------------- INIT ----------------
orch = Orchestrator()

# ---------------- LOAD DATA ----------------
with open("validation/test_cases.json") as f:
    test_cases = json.load(f)

results = []
correct = 0

# ---------------- RUN TESTS ----------------
for case in test_cases:
    query = case["query"]
    expected = case["expected"]

    # Run system
    response = orch.handle(query)

    # ---------------- CLASSIFY OUTPUT ----------------
    response_lower = response.lower()

    if "⚠️ i cannot assist" in response_lower:
        predicted = "blocked"

    elif "designed to help" in response_lower:
        predicted = "out_of_scope"

    elif "complaint registered" in response_lower:
        predicted = "complaint"

    elif "policy information" in response_lower:
        predicted = "policy"

    elif "top recommendations" in response_lower:
        predicted = "product"

    elif "order" in response_lower:
        predicted = "order"

    else:
        predicted = "unknown"

    # ---------------- CHECK CORRECTNESS ----------------
    is_correct = predicted == expected

    if is_correct:
        correct += 1

    # 🔥 IMPORTANT: MUST be inside loop
    results.append({
        "query": query,
        "expected": expected,
        "predicted": predicted,
        "correct": is_correct
    })

# ---------------- PRINT RESULTS ----------------
for r in results:
    print("\n----------------------------")
    print(f"Query: {r['query']}")
    print(f"Expected: {r['expected']}")
    print(f"Predicted: {r['predicted']}")
    print(f"Correct: {r['correct']}")

# ---------------- FINAL ACCURACY ----------------
print("\n============================")

if len(results) == 0:
    print("❌ No results generated")
else:
    accuracy = correct / len(results)
    print(f"Accuracy: {accuracy * 100:.2f}%")

print("============================")
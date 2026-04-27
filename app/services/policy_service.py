import json
import os

class PolicyService:
    def __init__(self):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        file_path = os.path.join(BASE_DIR, "data", "policies.json")

        if os.path.exists(file_path):
            with open(file_path) as f:
                data = json.load(f)
                self.policies = data.get("policies", data) if isinstance(data, dict) else data
        else:
            self.policies = []

    def search_policy(self, query: str):
        query = query.lower()
        # First pass — exact topic match
        for policy in self.policies:
            if policy["topic"] in query:
                return policy
        # Second pass — partial keyword match
        for policy in self.policies:
            if any(word in query for word in policy["topic"].split()):
                return policy
        return None

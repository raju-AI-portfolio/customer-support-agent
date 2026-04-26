import json
import os


class PolicyService:
    def __init__(self):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        file_path = os.path.join(BASE_DIR, "data", "policies.json")

        with open(file_path) as f:
            self.policies = json.load(f)

    def search_policy(self, query: str):
        query = query.lower()

        for policy in self.policies:
            if policy["topic"] in query:
                return policy

        return None
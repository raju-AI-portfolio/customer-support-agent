import gzip
import json

input_file = "data/meta_Electronics.json.gz"
output_file = "data/clean_products.json"

max_records = 5000  # 🔥 limit to avoid crash

clean_data = []

with gzip.open(input_file, 'rt') as f:
    for i, line in enumerate(f):
        if i >= max_records:
            break

        try:
            data = json.loads(line)

            title = data.get("title")
            description = " ".join(data.get("description", [])) if data.get("description") else ""

            if not title or not description:
                continue

            clean_data.append({
                "name": title,
                "description": description
            })

        except:
            continue

# Save cleaned data
with open(output_file, "w") as f:
    json.dump(clean_data, f, indent=2)

print(f"Saved {len(clean_data)} products")
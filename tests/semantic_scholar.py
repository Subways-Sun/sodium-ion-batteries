import requests
import json

base_url = "https://api.semanticscholar.org/graph/v1/paper/search"

query = "sodium+ion+batteries"
limit = 20
fields = "url,title,abstract"

url = f"{base_url}?query={query}&limit={limit}&fields={fields}"

response = requests.get(url, timeout=100)
result = {}

if response.status_code == 200:
    result = response.json()

with open("test.json", "w", encoding='utf-8') as f:
    json.dump(result["data"], f, ensure_ascii=False, indent=4)

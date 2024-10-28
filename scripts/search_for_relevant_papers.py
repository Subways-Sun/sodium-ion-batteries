"""Script to retrive relevant paper"""

import json
import sib_package.literature_retrival.semantic_scholar as ss

WORK_DIR = r"%HOMEPATH%\OneDrive\Documents\GitHub\sodium-ion-batteries\literature-retrival"

QUERY = "sodium+ion+battery+anode"

result = ss.search(QUERY, limit = 100, fields = "title,abstract")
RESULT_PATH = WORK_DIR + r"\data\search.json"
with open(RESULT_PATH, "w", encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=4)

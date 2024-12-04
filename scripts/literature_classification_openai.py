"""Script to classify literature using OpenAI API"""

import json
import platform
import os
from pathlib import Path
from sib.literature.openai import classify as cl

# Set working directory based on the operating system
HOME_PATH = str(Path.home())
WORK_DIR = ""
if platform.system() == "Windows":
    WORK_DIR = HOME_PATH + r"\OneDrive\Documents\GitHub\sodium-ion-batteries"
if platform.system() == "Darwin":
    WORK_DIR = HOME_PATH + r"/Documents/GitHub/sodium-ion-batteries"

RESULT = "annotated_data.json"
RESULT_PATH = os.path.join(WORK_DIR, "data_annotated", RESULT)

text = []
label = []

# Load the annotated data
with open(RESULT_PATH, "r", encoding='utf-8') as file:
    data = json.load(file)
    text = data["text"]
    label = data["label"]

# Classify the literature
result = []
for item in text:
    res = cl('gpt-4o', item)
    result.append(res.content)

result_int = []
for item in result:
    if item == "relevant cathode" or item == "relevant anode" or item == "relevant cathode anode":
        result_int.append(1)
    elif item == "irrelevant":
        result_int.append(0)
    else:
        result_int.append(-1)

# Save the result to a json file
RESULT_OPENAI = "annotated_data_openai.json"
RESULT_PATH_OPENAI = os.path.join(WORK_DIR, "data_annotated", RESULT_OPENAI)
with open(RESULT_PATH_OPENAI, "w", encoding='utf-8') as file:
    json.dump({"text": text, "label_openai_raw": result, "label_openai": result_int, "label_annotated": label}, file, ensure_ascii=False, indent=4)

# with open(RESULT_PATH, "r", encoding='utf-8') as file:
#     data = json.load(file)
#     i = 0
#     for item in data[:100]:
#         user_message = item["abstract"]
#         res = cl('gpt-4o-mini', user_message)
#         print(f"{i} {res}")
#         i += 1

# with open(RESULT_PATH, "r", encoding='utf-8') as file:
#     i = 34
#     item = json.load(file)[i-1]
#     print(item["abstract"])
#     user_message = item["abstract"]
#     res = cl('gpt-4o', user_message)
#     print(f"{i} {res}")

"""Script to keep only relevant entries from the annotated data."""
# pylint: disable=locally-disabled, line-too-long
import json
import platform
import os
from pathlib import Path

# Set working directory based on the operating system
HOME_PATH = str(Path.home())
WORK_DIR = ""
if platform.system() == "Windows":
    WORK_DIR = HOME_PATH + r"\OneDrive\Documents\GitHub\sodium-ion-batteries"
if platform.system() == "Darwin":
    WORK_DIR = HOME_PATH + r"/Documents/GitHub/sodium-ion-batteries"

RESULT = "search_20241212-002935_sodium+ion+battery+anode-sodium+ion+battery+cathode-sodium+ion+battery+electrode_openai.json"
RESULT_PATH = os.path.join(WORK_DIR, "data_annotated", RESULT)

with open(RESULT_PATH, 'r', encoding='utf-8') as file:
    data = json.load(file)

relevant_list = []
for entry in data:
    if entry.get("label_openai") == 1:
        print(1)
        relevant_list.append(entry)

OUTPUT = "search_20241212-002935_sodium+ion+battery+anode-sodium+ion+battery+cathode-sodium+ion+battery+electrode_openai_relevant.json"
OUTPUT_PATH = os.path.join(WORK_DIR, "data_annotated", OUTPUT)

with open(OUTPUT_PATH, 'w', encoding='utf-8') as file:
    json.dump(relevant_list, file, ensure_ascii=False, indent=4)

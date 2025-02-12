"""Script to process manual label from annotated data"""
# pylint: disable=locally-disabled, line-too-long, invalid-name
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

# Load the annotated data
ANNOTATED = "search_20241106-223705_sodium+ion+battery+anode-sodium+ion+battery+cathode-sodium+ion+battery+electrode_annotated.json"

ANNOTATED_PATH = os.path.join(WORK_DIR, "data_annotated", ANNOTATED)

# Load the annotated data into a list
with open(ANNOTATED_PATH, "r", encoding='utf-8') as file:
    annotated_data = json.load(file)

# Process the manual label
for i in annotated_data:
    if "Relevant" in i["label"]:
        i["label_int"] = 1
    elif "Irrelevant" in i["label"]:
        i["label_int"] = 0
    else:
        i["label_int"] = -1
        print("Error in DOI:", i["externalIds"]["doi"])

# Dump the processed data
PROCESSED = "search_20241106-223705_sodium+ion+battery+anode-sodium+ion+battery+cathode-sodium+ion+battery+electrode_annotated_processed.json"
PROCESSED_PATH = os.path.join(WORK_DIR, "data_annotated", PROCESSED)

with open(PROCESSED_PATH, "w", encoding='utf-8') as file:
    json.dump(annotated_data, file, indent=4)

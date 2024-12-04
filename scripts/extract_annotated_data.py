"""Script to extract text and label from annotated data"""
import json
import platform
import os
from pathlib import Path
import random

# Set working directory based on the operating system
HOME_PATH = str(Path.home())
WORK_DIR = ""
if platform.system() == "Windows":
    WORK_DIR = HOME_PATH + r"\OneDrive\Documents\GitHub\sodium-ion-batteries"
if platform.system() == "Darwin":
    WORK_DIR = HOME_PATH + r"/Documents/GitHub/sodium-ion-batteries"

# Load the annotated data
ORIGINAL = "search_20241106-223705_sodium+ion+battery+anode-sodium+ion+battery+cathode-sodium+ion+battery+electrode.json"
ANNOTATED = "search_20241106-223705_sodium+ion+battery+anode-sodium+ion+battery+cathode-sodium+ion+battery+electrode_annotated.json"

ORIGINAL_PATH = os.path.join(WORK_DIR, "data", ORIGINAL)
ANNOTATED_PATH = os.path.join(WORK_DIR, "data_annotated", ANNOTATED)

TEXT = []
LABEL = []

# Load the original and annotated data into lists
with open(ANNOTATED_PATH, "r", encoding='utf-8') as file1:
    with open(ORIGINAL_PATH, "r", encoding='utf-8') as file2:
        annotated_data = json.load(file1)
        original_data = json.load(file2)
        LABELLED_COUNT = len(annotated_data)
        for item in annotated_data:
            LABEL.append(item["label"])
            paperId = item["paperId"]
            for paper in original_data:
                if paper["paperId"] == paperId:
                    TEXT.append(paper["abstract"])
                    break

# Convert the label to a list of integers
LABEL_INT = []
for item in LABEL:
    if "Relevant" in item:
        LABEL_INT.append(1)
    elif "Irrelevant" in item:
        LABEL_INT.append(0)
    else:
        LABEL_INT.append(-1)

# Add irrelevant data
IRRELEVANT = "search_20241203-193208_lithium+ion+battery.json"
IRRELEVANT_PATH = os.path.join(WORK_DIR, "data", IRRELEVANT)
IRRELEVANT_COUNT = 50

with open(IRRELEVANT_PATH, "r", encoding='utf-8') as file:
    irrelevant_data = json.load(file)
    for i in range(IRRELEVANT_COUNT):
        TEXT.append(irrelevant_data[i]["abstract"])
        LABEL_INT.append(0)

# Shuffle the data
combined = list(zip(TEXT, LABEL, LABEL_INT))
random.shuffle(combined)
TEXT[:], LABEL[:], LABEL_INT[:] = zip(*combined)

# Save the data to a json file
OUTPUT = "annotated_data.json"
OUTPUT_PATH = os.path.join(WORK_DIR, "data_annotated", OUTPUT)

with open(OUTPUT_PATH, "w", encoding='utf-8') as file:
    json.dump({"text": TEXT, "label": LABEL_INT}, file, ensure_ascii=False, indent=4)
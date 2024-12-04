import platform
import os
import json
from pathlib import Path
from sib.literature import lit_processing as lp

# Set working directory based on the operating system
HOME_PATH = str(Path.home())
WORK_DIR = ""
if platform.system() == "Windows":
    WORK_DIR = HOME_PATH + r"\OneDrive\Documents\GitHub\sodium-ion-batteries"
if platform.system() == "Darwin":
    WORK_DIR = HOME_PATH + r"/Documents/GitHub/sodium-ion-batteries"

# Load the result
RESULT = "annotated_data_openai.json"
RESULT_PATH = os.path.join(WORK_DIR, "data_annotated", RESULT)

text = []
label_openai = []
label_openai_raw = []
label_annotated = []
with open(RESULT_PATH, "r", encoding='utf-8') as file:
    data = json.load(file)
    text = data["text"]
    label_openai = data["label_openai"]
    label_openai_raw = data["label_openai_raw"]
    label_annotated = data["label_annotated"]

# Compare the labels
incorrect = 0
for i in range(len(label_openai)):
    if label_openai[i] != label_annotated[i]:
        print(f"{i} {label_openai[i]} {label_annotated[i]}")
        print(f"{text[i]}")
        print("\n")
        incorrect += 1

print(f"Number of incorrect labels: {incorrect}")
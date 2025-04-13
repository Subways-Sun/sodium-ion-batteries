"""Module to get relevant DOIs from annotated data."""
# pylint: disable=locally-disabled, line-too-long, invalid-name
import json
import platform
import os
from pathlib import Path
from sib.literature.lit_processing import *

# Set working directory based on the operating system
HOME_PATH = str(Path.home())
WORK_DIR = ""
if platform.system() == "Windows":
    WORK_DIR = HOME_PATH + r"\OneDrive\Documents\GitHub\sodium-ion-batteries"
if platform.system() == "Darwin":
    WORK_DIR = HOME_PATH + r"/Documents/GitHub/sodium-ion-batteries"

# Load the annotated data
ANNOTATED = "search_20250313-003348_openai_relevant.json"
ANNOTATED_PATH = os.path.join(WORK_DIR, "data_annotated", ANNOTATED)
# ORIGINAL = "search_20241106-223705_sodium+ion+battery+anode-sodium+ion+battery+cathode-sodium+ion+battery+electrode.json"
# ORIGINAL_PATH = os.path.join(WORK_DIR, "data", ORIGINAL)
DATA = []
with open(ANNOTATED_PATH, "r", encoding='utf-8') as f:
    DATA = json.load(f)
# ORIGINAL_DATA = []
# with open(ORIGINAL_PATH, "r", encoding='utf-8') as f:
#     ORIGINAL_DATA = json.load(f)

# Get the relevant DOIs
relevant_dois = []
for i in DATA:
    if i["label_openai"] == 1:
        relevant_dois.append(i["externalIds"]["DOI"])

# for i in range(len(DATA["text"])):
#     if DATA["label_openai"][i] == 1:
#         text = DATA["text"][i]
#         for j in range(len(ORIGINAL_DATA)):
#             if text == ORIGINAL_DATA[j]["abstract"]:
#                 relevant_dois.append(ORIGINAL_DATA[j]["externalIds"]["DOI"])

# Screen the relevant DOIs
PREFIX = ["10.1039", # RSC
          "10.1016", # Elsevier
          "10.1021", # ACS
          "10.1002", # Wiley
          "10.1007", # Springer
          "10.1080", # Taylor & Francis
          "10.1038"] # Nature
relevant_dois = [doi.lower() for doi in relevant_dois if doi[:7] in PREFIX]

# Sort the relevant DOIs in ascending order
relevant_dois.sort()

# Save the relevant DOIs
DOIS = "relevant_dois_20250313-003348.txt"
DOIS_PATH = os.path.join(WORK_DIR, "data", DOIS)
with open(DOIS_PATH, "w", encoding='utf-8') as f:
    for doi in relevant_dois:
        f.write(doi + "\n")

"""Script to retrive relevant paper"""

import json
import platform
import time
from pathlib import Path
import sib.literature.semantic as ss

# Set working directory based on the operating system
HOME_PATH = str(Path.home())
WORK_DIR = ""
if platform.system() == "Windows":
    WORK_DIR = HOME_PATH + r"\OneDrive\Documents\GitHub\sodium-ion-batteries"
if platform.system() == "Darwin":
    WORK_DIR = HOME_PATH + r"/Documents/GitHub/sodium-ion-batteries"

# Define search parameters
QRY = "sodium+ion+battery+anode"
LMT = 100
FLD = "externalIds,title,abstract,publicationTypes,publicationDate,venue"
OFSLST = range(0, 500, 100)

result = list([])
# Search for relevant papers
for OFS in OFSLST:
    temp = ss.search(QRY, offset = OFS, limit = LMT, fields = FLD)[0]
    for item in temp:
        result.append(item)
    time.sleep(3)

# Save the result to a json file
RESULT_PATH = ""
if platform.system() == "Windows":
    RESULT_PATH = WORK_DIR + rf"\data\search_{QRY}_{len(result)}.json"
if platform.system() == "Darwin":
    RESULT_PATH = WORK_DIR + rf"/data/search_{QRY}_{len(result)}.json"
with open(RESULT_PATH, "w", encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=4)

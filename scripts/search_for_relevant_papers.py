"""Script to retrive relevant paper"""

import json
import platform
from datetime import datetime
from pathlib import Path
from sib.literature import semantic as ss
from sib.literature import lit_processing as lp

# Set working directory based on the operating system
HOME_PATH = str(Path.home())
WORK_DIR = ""
if platform.system() == "Windows":
    WORK_DIR = HOME_PATH + r"\OneDrive\Documents\GitHub\sodium-ion-batteries"
if platform.system() == "Darwin":
    WORK_DIR = HOME_PATH + r"/Documents/GitHub/sodium-ion-batteries"

# Define search parameters
QRYLST = ["sodium+ion+battery+anode",
          "sodium+ion+battery+cathode",
          "sodium+ion+battery+electrode"]

FLD = "externalIds,title,abstract,publicationTypes,publicationDate,venue"
CNT = 100 # Number of papers to retrieve

LMT = 100
OFSLST = range(0, CNT, 100)
PBL = "JournalArticle"
BLK_PASS = 1
BLK_TOKEN = ""

result = list([])
# Search for relevant papers
# for QRY in QRYLST:
#     for OFS in OFSLST:
#         temp = ss.search(QRY, offset = OFS, limit = LMT, fields = FLD, publicationTypes = PBL)[0]
#         for item in temp:
#             result.append(item)

for QRY in QRYLST:
    temp = ss.search_bulk(QRY, fields = FLD, publicationTypes = PBL)[0]
    for item in temp:
        result.append(item)

# Save the result to a json file
RESULT_PATH = ""
current_time = datetime.now().strftime("%Y%m%d-%H%M%S")
if platform.system() == "Windows":
    SEARCH_NAME = "-".join(QRYLST)
    RESULT_PATH = WORK_DIR + rf"\data\search_{current_time}_{SEARCH_NAME}.json"
if platform.system() == "Darwin":
    RESULT_PATH = WORK_DIR + rf"/data/search_{current_time}_{SEARCH_NAME}.json"
with open(RESULT_PATH, "w", encoding='utf-8') as file:
    json.dump(result, file, ensure_ascii=False, indent=4)

# Remove duplicates
lp.remove_duplicates(RESULT_PATH)

# Only keep journal articles
lp.keep_journal(RESULT_PATH)

# Remove papers with no abstract
lp.remove_no_abstract(RESULT_PATH)

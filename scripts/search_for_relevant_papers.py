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
YR = "2016-"

result = list([])
# Search for relevant papers
# for QRY in QRYLST:
#     for OFS in OFSLST:
#         temp = ss.search(QRY, offset = OFS, limit = LMT, fields = FLD, publicationTypes = PBL)[0]
#         for item in temp:
#             result.append(item)

for QRY in QRYLST:
    BLK_TOKEN = ""
    for i in range(0, CNT, 1000):
        result_temp = ss.search_bulk(QRY, fields = FLD, publicationTypes = PBL, token = BLK_TOKEN, year = YR)
        temp = result_temp[0]
        BLK_TOKEN = result_temp[2]
        for item in temp:
            result.append(item)

# Save the result to a json file
RESULT_PATH = ""
SEARCH_NAME = "-".join(QRYLST)
current_time = datetime.now().strftime("%Y%m%d-%H%M%S")
if platform.system() == "Windows":
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

# Only keep papers from select publishers
publishers = ["10.1039", # RSC
              "10.1016", # Elsevier
              "10.1021", # ACS
              "10.1002", # Wiley
              "10.1007", # Springer
              "10.1080", # Taylor & Francis
              "10.1038"] # Nature
lp.keep_select_publishers(RESULT_PATH, publishers)

# Print the number of papers retrieved
with open(RESULT_PATH, "r", encoding='utf-8') as file:
    data = json.load(file)
    print(f"Number of papers retrieved: {len(data)}")

"""Script to classify literature using OpenAI API"""

import json
import platform
from pathlib import Path
from sib.literature.openai import classify as cl

# Set working directory based on the operating system
HOME_PATH = str(Path.home())
WORK_DIR = ""
if platform.system() == "Windows":
    WORK_DIR = HOME_PATH + r"\OneDrive\Documents\GitHub\sodium-ion-batteries"
if platform.system() == "Darwin":
    WORK_DIR = HOME_PATH + r"/Documents/GitHub/sodium-ion-batteries"

RESULT_PATH = ""
# Load the search result
if platform.system() == "Windows":
    # RESULT_PATH = WORK_DIR + r"\data\test.json"
    RESULT_PATH = WORK_DIR + r"\data\search_20241106-223705_sodium+ion+battery+anode-sodium+ion+battery+cathode-sodium+ion+battery+electrode.json"

if platform.system() == "Darwin":
    # RESULT_PATH = WORK_DIR + r"/data/test.json"
    RESULT_PATH = WORK_DIR + r"/data/search_20241106-223705_sodium+ion+battery+anode-sodium+ion+battery+cathode-sodium+ion+battery+electrode.json"

# with open(RESULT_PATH, "r", encoding='utf-8') as file:
#     i = 1
#     for item in json.load(file):
#         user_message = item["abstract"]
#         res = cl('gpt-4o-mini', user_message)
#         print(f"{i} {res}")
#         i += 1

with open(RESULT_PATH, "r", encoding='utf-8') as file:
    i = 34
    item = json.load(file)[i-1]
    print(item["abstract"])
    user_message = item["abstract"]
    res = cl('gpt-4o-mini', user_message)
    print(f"{i} {res}")

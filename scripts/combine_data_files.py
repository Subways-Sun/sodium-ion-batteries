"""Combine two search results and remove duplicates."""
# pylint: disable=locally-disabled, line-too-long, invalid-name
import platform
from pathlib import Path
from sib.literature import lit_processing as lp

# Set working directory based on the operating system
HOME_PATH = str(Path.home())
WORK_DIR = ""
if platform.system() == "Windows":
    WORK_DIR = HOME_PATH + r"\OneDrive\Documents\GitHub\sodium-ion-batteries\data"
if platform.system() == "Darwin":
    WORK_DIR = HOME_PATH + r"/Documents/GitHub/sodium-ion-batteries/data"

# Load the first search result
RESULT_PATH_1 = ""
RESULT_1 = "search_20241106-223705_sodium+ion+battery+anode-sodium+ion+battery+cathode-sodium+ion+battery+electrode.json"
if platform.system() == "Windows":
    RESULT_PATH_1 = WORK_DIR + "\\" + RESULT_1
if platform.system() == "Darwin":
    RESULT_PATH_1 = WORK_DIR + r"/" + RESULT_1

# Load the second search result
RESULT_PATH_2 = ""
RESULT_2 = "search_20241203-194124_sodium+ion+battery+anode-sodium+ion+battery+cathode-sodium+ion+battery+electrode.json"
if platform.system() == "Windows":
    RESULT_PATH_2 = WORK_DIR + "\\" + RESULT_2
if platform.system() == "Darwin":
    RESULT_PATH_2 = WORK_DIR + r"/" + RESULT_2

# Combine the two search results
COMBINED_PATH = ""
if platform.system() == "Windows":
    COMBINED_PATH = WORK_DIR + r"\search_combined.json"
if platform.system() == "Darwin":
    COMBINED_PATH = WORK_DIR + r"/search_combined.json"
lp.combine_json_files(COMBINED_PATH, RESULT_PATH_1, RESULT_PATH_2)

# Remove duplicates
lp.remove_duplicates(COMBINED_PATH)

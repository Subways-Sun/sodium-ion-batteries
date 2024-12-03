"""Combine two search results and remove duplicates."""
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
if platform.system() == "Windows":
    RESULT_PATH_1 = WORK_DIR + r"\search_20241106-223705_sodium+ion+battery+anode-sodium+ion+battery+cathode-sodium+ion+battery+electrode.json"
if platform.system() == "Darwin":
    RESULT_PATH_1 = WORK_DIR + r"/search_20241106-223705_sodium+ion+battery+anode-sodium+ion+battery+cathode-sodium+ion+battery+electrode.json"

# Load the second search result
RESULT_PATH_2 = ""
if platform.system() == "Windows":
    RESULT_PATH_2 = WORK_DIR + r"\search_20241106-224154_sodium+ion+battery+anode-sodium+ion+battery+cathode-sodium+ion+battery+electrode.json"
if platform.system() == "Darwin":
    RESULT_PATH_2 = WORK_DIR + r"/search_20241106-224154_sodium+ion+battery+anode-sodium+ion+battery+cathode-sodium+ion+battery+electrode.json"

# Combine the two search results
lp.combine_json_files(WORK_DIR + r"\search_combined.json", RESULT_PATH_1, RESULT_PATH_2)

# Remove duplicates
lp.remove_duplicates(WORK_DIR + r"\search_combined.json")

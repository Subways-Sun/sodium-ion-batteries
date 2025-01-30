"""Script to rephrase abstract using OpenAI API"""
# pylint: disable=locally-disabled, line-too-long
import json
import platform
import os
import time
from pathlib import Path
from sib.literature.openai import classify as cl
# from sib.literature.lit_processing import keep_relevant as kr

# Set working directory based on the operating system
HOME_PATH = str(Path.home())
WORK_DIR = ""
if platform.system() == "Windows":
    WORK_DIR = HOME_PATH + r"\OneDrive\Documents\GitHub\sodium-ion-batteries"
if platform.system() == "Darwin":
    WORK_DIR = HOME_PATH + r"/Documents/GitHub/sodium-ion-batteries"

RESULT = "search_20241212-002935_sodium+ion+battery+anode-sodium+ion+battery+cathode-sodium+ion+battery+electrode.json"
RESULT_PATH = os.path.join(WORK_DIR, "data_annotated", RESULT)

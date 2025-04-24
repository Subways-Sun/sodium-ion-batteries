"""Script to rephrase abstract using OpenAI API"""
# pylint: disable=locally-disabled, line-too-long, invalid-name
import json
import platform
import os
import time
from pathlib import Path
from sib.literature.openai import rephrase as rp
# from sib.literature.openai import classify as cl
# from sib.literature.lit_processing import keep_relevant as kr

# Set working directory based on the operating system
HOME_PATH = str(Path.home())
WORK_DIR = ""
if platform.system() == "Windows":
    WORK_DIR = HOME_PATH + r"\OneDrive\Documents\GitHub\sodium-ion-batteries"
if platform.system() == "Darwin":
    WORK_DIR = HOME_PATH + r"/Documents/GitHub/sodium-ion-batteries"

# RESULT = "search_20241106-223705_sodium+ion+battery+anode-sodium+ion+battery+cathode-sodium+ion+battery+electrode_annotated_processed.json"
RESULT = "search_20241106-223705_sodium+ion+battery+anode-sodium+ion+battery+cathode-sodium+ion+battery+electrode_annotated_50irrelevant_processed.json"
RESULT_PATH = os.path.join(WORK_DIR, "data_annotated", RESULT)

data = []
rephrased_data = []

# Load the data
with open(RESULT_PATH, "r", encoding="utf-8") as file:
    data = json.load(file)
    for times in range(3):
        j = 0
        for i in data:
            user_message = i["text"]
            res = rp('gpt-4o', user_message)
            rephrased_data.append({"text": res.content, "label_int": i["label_int"]})
            print(str(times) + "-" + str(j))
            j += 1

overall_data = data + rephrased_data

# Dump the rephrased data
REPHRASED = "search_20241106-223705_sodium+ion+battery+anode-sodium+ion+battery+cathode-sodium+ion+battery+electrode_annotated_50irrelevant_rephrased3.json"
REPHRASED_PATH = os.path.join(WORK_DIR, "data_annotated", REPHRASED)

with open(REPHRASED_PATH, "w", encoding="utf-8") as file:
    json.dump(overall_data, file, indent=4)

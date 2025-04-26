"""Script to classify literature using OpenAI API"""
# pylint: disable=locally-disabled, line-too-long, invalid-name, consider-using-enumerate, logging-fstring-interpolation
import json
import platform
import os
import time
import logging
from pathlib import Path
from sib.literature.openai import classify as cl
from sib.literature.lit_processing import *

logging.basicConfig(
    filename = f"logs/lit_classification_openai_{time.strftime('%Y-%m-%d_%H%M%S')}.log",
    encoding = "utf-8",
    filemode = "a",
    format = "{asctime}.{msecs:03.0f} - {levelname} - {message}",
    style = "{",
    datefmt = "%Y-%m-%d %H:%M:%S",
    level = logging.DEBUG
)

# Set working directory based on the operating system
HOME_PATH = str(Path.home())
WORK_DIR = ""
if platform.system() == "Windows":
    WORK_DIR = HOME_PATH + r"\OneDrive\Documents\GitHub\sodium-ion-batteries"
if platform.system() == "Darwin":
    WORK_DIR = HOME_PATH + r"/Documents/GitHub/sodium-ion-batteries"

# RESULT = "search_20241106-223705_noirrelevant.json"
RESULT = "search_20241106-223705_50irrelevant.json"
RESULT_OPENAI = "search_20241106-223705_50irrelevant_openai_repeat.json"

RESULT_PATH = os.path.join(WORK_DIR, "data_annotated", RESULT)

data = read_json(RESULT_PATH)
try:
    for x in range(10):
        for i in range(len(data)):
            logging.info(f"Processing DOI {data[i]['externalIds']['DOI']} of {len(data)}")
            user_message = data[i]["text"]
            res = cl('gpt-4o', user_message)
            logging.info(f"Response: {res}")
            data[i][f"label_openai_raw_{x}"] = res.content
            if res.content in ("relevant cathode", "relevant anode", "relevant cathode anode"):
                data[i][f"label_openai_{x}"] = 1
            elif res.content == "irrelevant":
                data[i][f"label_openai_{x}"] = 0
            else:
                data[i][f"label_openai_{x}"] = -1
    RESULT_PATH_OPENAI = os.path.join(WORK_DIR, "data_annotated", RESULT_OPENAI)
    write_json(RESULT_PATH_OPENAI, data)

except Exception as e:
    logging.error(f"Error processing DOI {data[i]['externalIds']['DOI']}: {e}")
    RESULT_PATH_OPENAI = os.path.join(WORK_DIR, "data_annotated", RESULT_OPENAI)
    write_json(RESULT_PATH_OPENAI, data)
    print("Error occurred, data saved. Exiting")

# # Keep relevant papers
# RESULT_OPENAI_RELEVANT = "search_20250313-003348_3000-_openai_relevant.json"
# RESULT_PATH_OPENAI_RELEVANT = os.path.join(WORK_DIR, "data_annotated", RESULT_OPENAI_RELEVANT)
# write_json(RESULT_PATH_OPENAI_RELEVANT, keep_relevant(read_json(RESULT_PATH_OPENAI), "label_openai"))
# logging.info(f"Number of papers relevant: {len(read_json(RESULT_PATH_OPENAI_RELEVANT))}")

# with open(RESULT_PATH_OPENAI, "r", encoding='utf-8') as file:
#     data1 = json.load(file)
#     print(f"Number of papers relevant: {len(data1)}")


# RESULT = "annotated_data.json"
# RESULT_PATH = os.path.join(WORK_DIR, "data_annotated", RESULT)

# text = []
# label = []

# Load the annotated data
# with open(RESULT_PATH, "r", encoding='utf-8') as file:
#     data = json.load(file)
#     text = data["text"]
#     label = data["label"]

# Classify the literature
# result = []
# for item in text:
#     res = cl('gpt-4o', item)
#     result.append(res.content)

# result_int = []
# for item in result:
#     if item == "relevant cathode" or item == "relevant anode" or item == "relevant cathode anode":
#         result_int.append(1)
#     elif item == "irrelevant":
#         result_int.append(0)
#     else:
#         result_int.append(-1)

# Save the result to a json file
# RESULT_OPENAI = "annotated_data_openai.json"
# RESULT_PATH_OPENAI = os.path.join(WORK_DIR, "data_annotated", RESULT_OPENAI)
# with open(RESULT_PATH_OPENAI, "w", encoding='utf-8') as file:
#     json.dump({"text": text, "label_openai_raw": result, "label_openai": result_int, "label_annotated": label}, file, ensure_ascii=False, indent=4)

# with open(RESULT_PATH, "r", encoding='utf-8') as file:
#     data = json.load(file)
#     i = 0
#     for item in data[:100]:
#         user_message = item["abstract"]
#         res = cl('gpt-4o-mini', user_message)
#         print(f"{i} {res}")
#         i += 1

# with open(RESULT_PATH, "r", encoding='utf-8') as file:
#     i = 34
#     item = json.load(file)[i-1]
#     print(item["abstract"])
#     user_message = item["abstract"]
#     res = cl('gpt-4o', user_message)
#     print(f"{i} {res}")

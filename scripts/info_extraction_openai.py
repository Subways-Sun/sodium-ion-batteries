"""Tests the OpenAI model for information extraction"""
# pylint: disable=locally-disabled, line-too-long, invalid-name, logging-fstring-interpolation
import json
import os
import logging
import time
# import tiktoken
from sib.literature.openai import extract
from sib.literature.lit_processing import read_json, write_json, extract_content

logging.basicConfig(
    filename = f"logs/info_extraction_openai_{time.strftime('%Y-%m-%d_%H%M%S')}.log",
    encoding = "utf-8",
    filemode = "a",
    format = "{asctime} - {levelname} - {message}",
    style = "{",
    datefmt = "%Y-%m-%d %H:%M:%S",
    level = logging.DEBUG
)

openai_model = "o3-mini"

full_text_dir = os.path.join(os.getcwd(), "extraction")
logging.debug(f"Full text directory: {full_text_dir}")

for file in os.listdir(full_text_dir):
    if file.endswith(".json"):
        file_path = os.path.join(full_text_dir, file)
        full_text = read_json(file_path)
        logging.debug(f"Reading file: {file_path}")

        results = extract_content(full_text, "Result")
        if results == "":
            logging.warning(f"Result section not found in {file}, skipping...")
            continue
        experimental = extract_content(full_text, "Experiment")
        if experimental == "":
            logging.warning(f"Experimental section not found in {file}")

        datas = extract(openai_model, results, "results")
        data = json.loads(datas)
        if experimental != "":
            for i in data["material"]:
                sm = extract(openai_model, experimental, "experimental", i["material_name"])
                i["starting_material"] = json.loads(sm)["starting_material"]

        write_json(os.path.join(os.getcwd(), "extracted", f"{file.removesuffix('.json')}_processed_{openai_model}.json"), data)

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
    format = "{asctime}.{msecs:03.0f} - {levelname} - {message}",
    style = "{",
    datefmt = "%Y-%m-%d %H:%M:%S",
    level = logging.DEBUG
)

openai_model = "o3-mini"
reasoning_effort = "medium"

full_text_dir = os.path.join(os.getcwd(), "articles_20250313_500_json_part")
logging.debug(f"Full text directory: {full_text_dir}")

for file in os.listdir(full_text_dir):
    if file.endswith(".json"):
        file_path = os.path.join(full_text_dir, file)
        full_text = read_json(file_path)
        logging.debug(f"Reading file: {file_path}")

        results = extract_content(full_text, "Result")
        if results == "":
            logging.warning(f"Result section not found in {file}, using full text...")
            results = extract_content(full_text, "")
        experimental = extract_content(full_text, "Experiment")
        if experimental == "":
            experimental = extract_content(full_text, "Method")
            if experimental == "":
                logging.warning(f"Experimental section not found in {file}")

        datas = extract(openai_model, results, "results", "", reasoning_effort)
        logging.info(f"OpenAI Response: {datas[1]}")
        data = json.loads(datas[0])
        if experimental != "":
            for i in data["material"]:
                sm = extract(openai_model, experimental, "experimental", i["material_name"], reasoning_effort)
                i["starting_material"] = json.loads(sm[0])["starting_material"]
                logging.info(f"OpenAI Response: {sm[1]}")
        if openai_model == "o3-mini": 
            write_json(os.path.join(os.getcwd(), "articles_20250313_500_extracted", f"{file.removesuffix('.json')}_processed_{openai_model}_{reasoning_effort}.json"), data)
        if openai_model == "gpt-4o":
            write_json(os.path.join(os.getcwd(), "articles_20250313_500_extracted", f"{file.removesuffix('.json')}_processed_{openai_model}.json"), data)

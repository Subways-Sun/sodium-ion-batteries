"""Tests the OpenAI model for information extraction"""
# pylint: disable=locally-disabled, line-too-long, invalid-name
import json
import os
import logging
import tiktoken
from sib.literature.openai import extract
from sib.literature.lit_processing import read_json, write_json, extract_content

file_dir = os.path.join(os.getcwd(), "articles_20241212_json")

for file in os.listdir(file_dir):
    if file.endswith(".json"):
        file_path = os.path.join(file_dir, file)
        full_text = read_json(file_path)

        text = extract_content(full_text, "Result")
        model = "gpt-4o"

        data = extract(model, text)
        data_out = json.loads(data)
        write_json(os.path.join(file_dir, file.removesuffix(".json"), "_processed_", model, ".json"), data_out)

test = "10.1021-acs.langmuir.4c02868.json"
file_test = os.path.join(os.getcwd(), "extraction_tests", test)

full_text = read_json(file_test)

text = ""
for i in full_text["Sections"]:
    if "Result" in i["name"]:
        for j in i["content"]:
            text += "\n".join(j["content"])
        text += "\n"
openai_model = "gpt-4o"
data = extract(openai_model, text)
data_out = json.loads(data)
# with open(r"tests\10.1021-acs.nanolett.9b00544_processed_" + openai_model + ".json", "w", encoding="utf-8") as f:
#     json.dump(data_out, f, ensure_ascii=False, indent=4)
with open(r"tests\10.1021-acs.langmuir.4c02868_processed_" + openai_model + ".json", "w", encoding="utf-8") as f:
    json.dump(data_out, f, ensure_ascii=False, indent=4)

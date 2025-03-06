"""Tests the OpenAI model for information extraction"""
# pylint: disable=locally-disabled, line-too-long, invalid-name
import json
import os
import logging
import tiktoken
from sib.literature.openai import extract
from sib.literature.lit_processing import read_json, write_json, extract_content

full_text_dir = os.path.join(os.getcwd(), "extraction")

for file in os.listdir(full_text_dir):
    if file.endswith(".json"):
        file_path = os.path.join(full_text_dir, file)
        full_text = read_json(file_path)

        results = extract_content(full_text, "Result")
        experimental = extract_content(full_text, "Experiment")
        openai_model = "gpt-4o"

        datas = extract(openai_model, results, "results")
        data = json.loads(datas)
        for i in data["material"]:
            sm = extract(openai_model, experimental, "experimental", i["material_name"])
            i["starting_material"] = json.loads(sm)["starting_material"]

        write_json(os.path.join(os.getcwd(), "extracted", f"{file.removesuffix('.json')}_processed_{openai_model}.json"), data)

# test = "10.1021-acs.langmuir.4c02868.json"
# # test = "10.1021-acs.nanolett.9b00544.json"
# file_test = os.path.join(os.getcwd(), "extraction_tests", test)

# full_text = read_json(file_test)

# # text = ""
# # for i in full_text["Sections"]:
# #     if "Result" in i["name"]:
# #         for j in i["content"]:
# #             text += "\n".join(j["content"])
# #         text += "\n"

# results = extract_content(full_text, "Result")
# experimental = extract_content(full_text, "Experiment")
# openai_model = "gpt-4o"

# datas = extract(openai_model, results, "results")
# data = json.loads(datas)
# for i in data["material"]:
#     sm = extract(openai_model, experimental, "experimental", i["material_name"])
#     i["starting_material"] = json.loads(sm)["starting_material"]
# # with open(r"extraction_tests\10.1021-acs.nanolett.9b00544_processed_" + openai_model + ".json", "w", encoding="utf-8") as f:
# #     json.dump(data, f, ensure_ascii=False, indent=4)
# with open(r"extraction_tests\10.1021-acs.langmuir.4c02868_processed_" + openai_model + ".json", "w", encoding="utf-8") as f:
#     json.dump(data, f, ensure_ascii=False, indent=4)

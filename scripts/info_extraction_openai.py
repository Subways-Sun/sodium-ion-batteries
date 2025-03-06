"""Tests the OpenAI model for information extraction"""
# pylint: disable=locally-disabled, line-too-long, invalid-name
import json
import os
import logging
import tiktoken
from sib.literature.openai import extract
from sib.literature.lit_processing import read_json, write_json, extract_content

results_json = {
    "type": "json_schema",
    "json_schema": {
        "name": "sodium_ion_battery_data",
        "schema": {
            "type": "object",
            "properties": {
                "material": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "material_type": {
                                "type": "string",
                                "enum": ["cathode", "anode", "electrolyte"]
                            },
                            "material_name": {"type": "string"},
                            "material_formula": {"type": "string"},
                            "capacity": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "capacity_value": {"type": "number"},
                                        "capacity_unit": {"type": "string"},
                                        "current_density_value": {"type": "number"},
                                        "current_density_unit": {"type": "string"}
                                    },
                                    "required": ["capacity_value", "capacity_unit"],
                                    "additionalProperties": False
                                }
                            },
                            "cycle_life": {
                                "type": "object",
                                "properties": {
                                    "value": {"type": "number"},
                                    "unit": {"type": "string"}
                                },
                                "required": ["value", "unit"],
                                "additionalProperties": False
                            }
                        },
                        "required": ["material_type",
                                     "material_name",
                                     "material_formula",
                                     "capacity",
                                     "cycle_life"],
                        "additionalProperties": False
                    }
                }
            },
            "required": ["material"],
            "additionalProperties": False
        },
        "strict": True
    }
}
experimental_json = {
    "type": "json_schema",
    "json_schema": {
        "name": "sodium_ion_battery_data",
        "schema": {
            "type": "object",
            "properties": {
                "starting_material": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "material_name": {"type": "string"},
                            "material_formula": {"type": "string"},
                            "amount": {
                                "type": "object",
                                "properties": {
                                    "value": {"type": "number"},
                                    "unit": {"type": "string"}
                                },
                                "required": ["value", "unit"],
                                "additionalProperties": False
                            }
                        },
                        "required": ["material_name", "material_formula", "amount"],
                        "additionalProperties": False
                    }
                }
            },
            "required": ["starting_material"],
            "additionalProperties": False
        },
        "strict": True
    }
}

full_text_dir = os.path.join(os.getcwd(), "articles_20241212_json")

# for file in os.listdir(full_text_dir):
#     if file.endswith(".json"):
#         file_path = os.path.join(full_text_dir, file)
#         full_text = read_json(file_path)

#         text = extract_content(full_text, "Result")
#         model = "gpt-4o"

#         data = extract(model, text, "results", results_json)
#         data = json.loads(data)
#         write_json(os.path.join(full_text_dir, file.removesuffix(".json"), "_processed_", model, ".json"), data)

test = "10.1021-acs.langmuir.4c02868.json"
# test = "10.1021-acs.nanolett.9b00544.json"
file_test = os.path.join(os.getcwd(), "extraction_tests", test)

full_text = read_json(file_test)

# text = ""
# for i in full_text["Sections"]:
#     if "Result" in i["name"]:
#         for j in i["content"]:
#             text += "\n".join(j["content"])
#         text += "\n"

results = extract_content(full_text, "Result")
experimental = extract_content(full_text, "Experiment")
print(experimental)
openai_model = "gpt-4o"

datas = extract(openai_model, results, "results")
data = json.loads(datas)
for i in data["material"]:
    sm = extract(openai_model, experimental, "experimental", i["material_name"])
    i["starting_material"] = json.loads(sm)["starting_material"]
# with open(r"extraction_tests\10.1021-acs.nanolett.9b00544_processed_" + openai_model + ".json", "w", encoding="utf-8") as f:
#     json.dump(data, f, ensure_ascii=False, indent=4)
with open(r"extraction_tests\10.1021-acs.langmuir.4c02868_processed_" + openai_model + ".json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

"""Module using OpenAI API to classify literature."""
# pylint: disable=locally-disabled, line-too-long, invalid-name
# from pydantic import BaseModel
from openai import OpenAI
# import tiktoken
client = OpenAI()

def classify(openai_model, user_message):
    """Function to chat with the AI"""
    prompt_v1 = "You are a scientific paper classifier. Your task is to classify the given abstract of a scientific paper into one of the following categories: 'relevant cathode', 'relevant anode', 'relevant cathode anode', or 'irrelevant'. The classification is based on whether the abstract mainly discusses sodium ion battery electrodes, and if so, whether it discusses cathode, anode, or both. Do not include quotation marks in your response."
    prompt_v2 = "You are a scientific paper classifier. Your task is to classify the given abstract of a scientific paper into one of the following categories: 'relevant cathode', 'relevant anode', 'relevant cathode anode', or 'irrelevant'. The classification is based on whether the abstract mainly discusses sodium ion battery electrodes, and if so, whether it discusses cathode, anode, or both. If you are not sure, or the abstract contains too little information, classify it as 'irrelevant'. Do not include quotation marks in your response."
    prompt_v3 = "You are a scientific paper classifier. Your task is to classify the given abstract of a scientific paper into one of the following categories: 'relevant cathode', 'relevant anode', 'relevant cathode anode', or 'irrelevant'. The classification is based on whether the abstract mainly discusses sodium ion battery electrodes, and if so, whether it discusses cathode, anode, or both. If the abstract mainly discusses other types of batteries such as lithium and potassium ion batteries, or is a review article, classify it as 'irrelevant'. If you are not sure, or the abstract contains too little information, classify it as 'irrelevant'. Do not include quotation marks in your response."
    prompt_v4 = "You are a scientific paper classifier. Your task is to classify the given abstract of a scientific paper into one of the following categories: 'relevant cathode', 'relevant anode', 'relevant cathode anode', or 'irrelevant'. The classification is based on whether the abstract mainly discusses sodium ion battery electrodes, and if so, whether it discusses cathode, anode, or both. If the abstract is unrelated to the field, or contains only theoretical approaches such as computer simulations (for example, density functional theory), or mainly discusses other types of batteries such as lithium and potassium ion batteries, or is a review article, classify it as 'irrelevant'. If you are not sure, or the abstract contains too little information, classify it as 'irrelevant'. Do not include quotation marks in your response."
    completion = client.chat.completions.create(
        model=openai_model,
        messages=[
            {
                "role": "system",
                "content": prompt_v4
            },
            {
                "role": "user",
                "content": user_message
            }
        ]
    )
    return completion.choices[0].message

def rephrase(openai_model, user_message):
    """Function to rephrase the user message"""
    completion = client.chat.completions.create(
        model=openai_model,
        messages=[
            {
                "role": "system",
                "content": "You are a scientific paper rephraser. You will be given an abstract of a scientific paper in the field of batteries. Your task is to rephrase the given abstract, retaining every detail in the original abstract. The overall topic cannot be changed, and any data mentioned cannot be altered. Output only the rephrasing of the abstract, do not include any additional information. Keep your response concise and to the point."
            },
            {
                "role": "user",
                "content": user_message
            }
        ]
    )
    return completion.choices[0].message

def extract(openai_model, user_message, mode: str, material_name: str = ""):
    """Function to rephrase the user message"""

    results_prompt = "You will be given unstructured text from the results and discussion section of a research paper and should extract information into the given JSON structure. The paper should focus on electrode or electrolyte materials of sodium ion batteries. Your task is to extract the material information from the given text. The material information includes the material type (cathode, anode, or electrolyte), material name, chemical formula of the material (if applicable), material properties including the type (charge, discharge, reversible, specific) and values of capacity reported under different current density (with unit) and cycle. Extract these information for each material mentioned in the paper. Take a moment to distinguish between different names of the same material and include all relevant information mentioned. If a series of capacities have been reported under different charge densities, make sure to include all of them. You should only look at materials used for sodium ion batteries, not for any other type of battery. For any information that the paper doesn't mention or that you are not sure of, you should assume it to be null. Check if the unit of the value matches the property you're assigning it to, if it does not, don't include it. If you find too little information on a specific material, don't include it."

    experimental_prompt = f"You will be given unstructured text from the experimental section of a research paper that focuses on '{material_name}'. You should extract information into the given JSON structure. Your task is to extract the starting materials used to synthesize '{material_name}'. Find the name, structure, and amount (with unit) of the starting materials. The paper may also focus on other materials, but you should only extract information related to '{material_name}'. For any information that the paper doesn't mention or if you are not sure, you should assume it to be null. If the synthesis of '{material_name}' is not mentioned, you should return an empty JSON."

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
                                "material_properties": {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "capacity_value": {"type": "number"},
                                            "capacity_unit": {"type": "string"},
                                            "capacity_type": {"type": "string",
                                                              "enum": ["charge", "discharge", "reversible", "specific", "not mentioned"]},
                                            "current_density_value": {"type": "number"},
                                            "current_density_unit": {"type": "string"},
                                            "cycle": {"type": "number"}
                                        },
                                        "required": ["capacity_value",
                                                     "capacity_unit",
                                                     "capacity_type",
                                                     "current_density_value",
                                                     "current_density_unit",
                                                     "cycle"],
                                        "additionalProperties": False
                                    }
                                }
                            },
                            "required": ["material_type",
                                         "material_name",
                                         "material_formula",
                                         "material_properties"],
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

    prompt = ""
    if mode == "results":
        prompt = results_prompt
    elif mode == "experimental":
        prompt = experimental_prompt

    if openai_model == "gpt-4o":
        completion = client.beta.chat.completions.parse(
            model = openai_model,
            messages = [
                {
                    "role": "system",
                    "content": prompt
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            response_format = results_json if mode == "results" else experimental_json
        )
        return completion.choices[0].message.content

    elif openai_model == "o3-mini":
        completion = client.beta.chat.completions.parse(
            model = openai_model,
            reasoning_effort = "medium",
            messages = [
                {
                    "role": "developer",
                    "content": prompt
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            response_format = results_json if mode == "results" else experimental_json
        )
        return completion.choices[0].message.content
    
    else:
        return

# def num_tokens_from_messages(messages, model="gpt-4o-2024-08-06"):
#     """Return the number of tokens used by a list of messages."""
#     try:
#         encoding = tiktoken.encoding_for_model(model)
#     except KeyError:
#         print("Warning: model not found. Using o200k_base encoding.")
#         encoding = tiktoken.get_encoding("o200k_base")
#     if model in {
#         "gpt-3.5-turbo-0125",
#         "gpt-4-0314",
#         "gpt-4-32k-0314",
#         "gpt-4-0613",
#         "gpt-4-32k-0613",
#         "gpt-4o-mini-2024-07-18",
#         "gpt-4o-2024-08-06"
#         }:
#         tokens_per_message = 3
#         tokens_per_name = 1
#     elif "gpt-3.5-turbo" in model:
#         print("Warning: gpt-3.5-turbo may update over time. Returning num tokens assuming gpt-3.5-turbo-0125.")
#         return num_tokens_from_messages(messages, model="gpt-3.5-turbo-0125")
#     elif "gpt-4o-mini" in model:
#         print("Warning: gpt-4o-mini may update over time. Returning num tokens assuming gpt-4o-mini-2024-07-18.")
#         return num_tokens_from_messages(messages, model="gpt-4o-mini-2024-07-18")
#     elif "gpt-4o" in model:
#         print("Warning: gpt-4o and gpt-4o-mini may update over time. Returning num tokens assuming gpt-4o-2024-08-06.")
#         return num_tokens_from_messages(messages, model="gpt-4o-2024-08-06")
#     elif "gpt-4" in model:
#         print("Warning: gpt-4 may update over time. Returning num tokens assuming gpt-4-0613.")
#         return num_tokens_from_messages(messages, model="gpt-4-0613")
#     else:
#         raise NotImplementedError(
#             f"""num_tokens_from_messages() is not implemented for model {model}."""
#         )
#     num_tokens = 0
#     for message in messages:
#         num_tokens += tokens_per_message
#         for key, value in message.items():
#             num_tokens += len(encoding.encode(value))
#             if key == "name":
#                 num_tokens += tokens_per_name
#     num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
#     return num_tokens

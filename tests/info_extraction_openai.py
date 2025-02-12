from sib.literature.openai import extract
import json

# def retrieve_content(content):
#     if content

full_text = ""
with open(r"tests\10.1021-acs.nanolett.9b00544.json", "r", encoding="utf-8") as f:
    full_text = json.load(f)
text = ""
for i in full_text["Sections"]:
    if "Result" in i["name"]:
        for j in i["content"]:
            text += "\n".join(j["content"])
        text += "\n"
openai_model = "gpt-4o"
data = extract(openai_model, text)
data_out = json.loads(data)
with open(r"tests\10.1021-acs.nanolett.9b00544_processed_" + openai_model + ".json", "w", encoding="utf-8") as f:
    json.dump(data_out, f, ensure_ascii=False, indent=4)

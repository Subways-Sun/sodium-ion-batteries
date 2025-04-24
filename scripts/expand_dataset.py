from sib.literature.lit_processing import read_json, write_json, combine_json_files
import os
import random

file1 = r"data_annotated\search_20241106-223705_sodium+ion+battery+anode-sodium+ion+battery+cathode-sodium+ion+battery+electrode_annotated.json"
file2 = r"data\search_20250424-210705.json"

data1 = read_json(file1)
data2 = read_json(file2)

random50 = random.sample(data2, 50)
for i in range(len(random50)):
    if "abstract" in random50[i]:
        random50[i]["text"] = random50[i]["abstract"]
        del random50[i]["abstract"]
    random50[i]["label"] = ["Irrelevant"]

file3 = r"data_annotated\search_20241106-223705_sodium+ion+battery+anode-sodium+ion+battery+cathode-sodium+ion+battery+electrode_annotated_50irrelevant.json"

write_json(file3, random50)

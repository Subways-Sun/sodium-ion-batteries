from sib.literature.lit_processing import read_json
data = read_json(r"data_annotated\search_20250313-003348_openai_relevant.json")

cathode = {
    "2016": 0,
    "2017": 0,
    "2018": 0,
    "2019": 0,
    "2020": 0,
    "2021": 0,
    "2022": 0,
    "2023": 0,
    "2024": 0,
    "2025": 0,
}
anode = {
    "2016": 0,
    "2017": 0,
    "2018": 0,
    "2019": 0,
    "2020": 0,
    "2021": 0,
    "2022": 0,
    "2023": 0,
    "2024": 0,
    "2025": 0
}
cathode_anode = {
    "2016": 0,
    "2017": 0,
    "2018": 0,
    "2019": 0,
    "2020": 0,
    "2021": 0,
    "2022": 0,
    "2023": 0,
    "2024": 0,
    "2025": 0
}

for i in data:
    try:
        if "cathode" in i["label_openai_raw"]:
            cathode[i["publicationDate"][:4]] += 1
        if "anode" in i["label_openai_raw"]:
            anode[i["publicationDate"][:4]] += 1
        if "cathode anode" in i["label_openai_raw"]:
            cathode_anode[i["publicationDate"][:4]] += 1
    except Exception as e:
        print(f"Error: {i['externalIds']['DOI']}")
        continue

print(f"Cathode: (2016,{cathode['2016']}) (2017,{cathode['2017']}) (2018,{cathode['2018']}) (2019,{cathode['2019']}) (2020,{cathode['2020']}) (2021,{cathode['2021']}) (2022,{cathode['2022']}) (2023,{cathode['2023']}) (2024,{cathode['2024']}) (2025,{cathode['2025']})")
print(f"Anode: (2016,{anode['2016']}) (2017,{anode['2017']}) (2018,{anode['2018']}) (2019,{anode['2019']}) (2020,{anode['2020']}) (2021,{anode['2021']}) (2022,{anode['2022']}) (2023,{anode['2023']}) (2024,{anode['2024']}) (2025,{anode['2025']})")
print(f"Cathode Anode: (2016,{cathode_anode['2016']}) (2017,{cathode_anode['2017']}) (2018,{cathode_anode['2018']}) (2019,{cathode_anode['2019']}) (2020,{cathode_anode['2020']}) (2021,{cathode_anode['2021']}) (2022,{cathode_anode['2022']}) (2023,{cathode_anode['2023']}) (2024,{cathode_anode['2024']}) (2025,{cathode_anode['2025']})")
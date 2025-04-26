from sib.literature.lit_processing import read_json
data = read_json(r"data\search_20250313-003348.json")
wiley = 0
acs = 0
rsc = 0
elsevier = 0
springer = 0
nature = 0
for i in data:
    if "10.1002" in i["externalIds"]["DOI"]:
        wiley += 1
    elif "10.1021" in i["externalIds"]["DOI"]:
        acs += 1
    elif "10.1039" in i["externalIds"]["DOI"]:
        rsc += 1
    elif "10.1016" in i["externalIds"]["DOI"]:
        elsevier += 1
    elif "10.1007" in i["externalIds"]["DOI"]:
        springer += 1
    elif "10.1038" in i["externalIds"]["DOI"]:
        nature += 1

print(f"Wiley: {wiley}")
print(f"ACS: {acs}")
print(f"RSC: {rsc}")
print(f"Elsevier: {elsevier}")
print(f"Springer: {springer}")
print(f"Nature: {nature}")
print(f"Total: {wiley + acs + rsc + elsevier + springer + nature}")
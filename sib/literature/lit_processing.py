"""Module for processing literature data."""
# pylint: disable=locally-disabled, line-too-long, invalid-name
import json

def read_json(json_file_path) -> dict:
    """Function to read a JSON file"""
    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def write_json(json_file_path, data: dict) -> None:
    """Function to write to a JSON file"""
    with open(json_file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def combine_json_files(output_file_path, *json_file_paths) -> None:
    """Function to combine multiple JSON files into one"""
    combined_data = []

    for file_path in json_file_paths:
        data = read_json(file_path)
        combined_data.extend(data)

    write_json(output_file_path, combined_data)

def remove_duplicates(input_dict: dict) -> list:
    """Function to remove duplicates from a dictionary list"""
    unique_entries = []
    seen_ids = set()

    for entry in input_dict:
        entry_id = entry.get('paperId')
        if entry_id not in seen_ids:
            unique_entries.append(entry)
            seen_ids.add(entry_id)

    return unique_entries

def keep_journal(input_dict: dict) -> list:
    """Function to only retain journal articles in a dictionary list"""
    journal = []
    for entry in input_dict:
        if entry.get('publicationTypes') == ['JournalArticle']:
            journal.append(entry)

    return journal

def remove_no_abstract(input_dict: dict) -> list:
    """Function to remove papers with no abstract from a dictionary list"""
    with_abstract = []
    for entry in input_dict:
        if entry.get('abstract'):
            with_abstract.append(entry)

    return with_abstract

def keep_select_publishers(input_dict: dict, publishers: list) -> list:
    """Function to only retain papers from select publishers in a dictionary list"""
    selected_list = []
    for entry in input_dict:
        if entry.get('externalIds').get('DOI'):
            if entry.get('externalIds').get('DOI').split('/')[0] in publishers:
                selected_list.append(entry)

    return selected_list

def keep_relevant(input_dict: dict, label: str) -> list:
    """Function to only retain relevant papers in a labelled dictionary list"""
    relevant_list = []
    for entry in input_dict:
        if entry.get(label) == 1:
            relevant_list.append(entry)

    return relevant_list

def extract_content(json_data: dict, key: str) -> str:
    """Extracts content from the JSON data"""
    content = ""
    for j in json_data:
        if j in ("Sections", "content"):
            for l in json_data[j]:
                if key in l["name"]:
                    content += recursive_extract(l["content"], l["name"])
                    content += "\n"
                elif isinstance(l["content"][0], dict):
                    content += extract_content(l, key)
    return content

def recursive_extract(json_data: dict, header: str) -> str:
    """Extracts content from the JSON data"""
    content = "\n" + header + "\n"
    for j in json_data:
        if isinstance(j, dict):
            content += recursive_extract(j["content"], j["name"])
        elif isinstance(j, str):
            content += j
            content += "\n"

    return content

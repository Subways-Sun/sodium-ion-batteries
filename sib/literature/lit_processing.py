"""Module for processing literature data."""
# pylint: disable=locally-disabled, line-too-long
import json

def combine_json_files(output_file_path, *json_file_paths):
    """Function to combine multiple JSON files into one"""
    combined_data = []

    for file_path in json_file_paths:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            combined_data.extend(data)

    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        json.dump(combined_data, output_file, ensure_ascii=False, indent=4)

def remove_duplicates(json_file_path):
    """Function to remove duplicates from a JSON file"""
    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    unique_entries = []
    seen_ids = set()

    for entry in data:
        entry_id = entry.get('paperId')
        if entry_id not in seen_ids:
            unique_entries.append(entry)
            seen_ids.add(entry_id)

    with open(json_file_path, 'w', encoding='utf-8') as file:
        json.dump(unique_entries, file, indent=4)

def keep_journal(json_file_path):
    """Function to only retain journal articles in a JSON file"""
    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    journal = []
    for entry in data:
        if entry.get('publicationTypes') == ['JournalArticle']:
            journal.append(entry)

    with open(json_file_path, 'w', encoding='utf-8') as file:
        json.dump(journal, file, ensure_ascii=False, indent=4)

def remove_no_abstract(json_file_path):
    """Function to remove papers with no abstract from a JSON file"""
    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    with_abstract = []
    for entry in data:
        if entry.get('abstract'):
            with_abstract.append(entry)

    with open(json_file_path, 'w', encoding='utf-8') as file:
        json.dump(with_abstract, file, ensure_ascii=False, indent=4)

def keep_select_publishers(json_file_path, publishers: list):
    """Function to only retain papers from select publishers in a JSON file"""
    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    selected_list = []
    for entry in data:
        if entry.get('externalIds').get('DOI').split('/')[0] in publishers:
            selected_list.append(entry)

    with open(json_file_path, 'w', encoding='utf-8') as file:
        json.dump(selected_list, file, ensure_ascii=False, indent=4)

def keep_relevant(json_file_path, label: str):
    """Function to only retain relevant papers in a labelled JSON file"""
    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    relevant_list = []
    for entry in data:
        if entry.get(label) == 1:
            relevant_list.append(entry)

    with open(json_file_path, 'w', encoding='utf-8') as file:
        json.dump(relevant_list, file, ensure_ascii=False, indent=4)

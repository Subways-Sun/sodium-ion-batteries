"""Module for processing literature data."""

import json

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

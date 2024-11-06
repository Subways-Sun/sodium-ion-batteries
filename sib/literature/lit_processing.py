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

def remove_reviews(json_file_path):
    """Function to remove review articles from a JSON file"""
    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    no_reviews = []
    for entry in data:
        if 'Review' not in entry.get('publicationTypes'):
            no_reviews.append(entry)

    with open(json_file_path, 'w', encoding='utf-8') as file:
        json.dump(no_reviews, file, ensure_ascii=False, indent=4)

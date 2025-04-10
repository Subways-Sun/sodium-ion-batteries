"""Combine two search results and remove duplicates."""
# pylint: disable=locally-disabled, line-too-long, invalid-name
import os
from sib.literature.lit_processing import combine_json_files

FILE_1 = os.path.join(os.getcwd(), "data_annotated", "search_20250313-003348_1-1000_openai_relevant.json")
FILE_2 = os.path.join(os.getcwd(), "data_annotated", "search_20250313-003348_1000-3000_openai_relevant.json")
FILE_3 = os.path.join(os.getcwd(), "data_annotated", "search_20250313-003348_3000-_openai_relevant.json")
combine_json_files(os.path.join(os.getcwd(), "data_annotated", "search_20250313-003348_openai_relevant.json"), FILE_1, FILE_2, FILE_3)

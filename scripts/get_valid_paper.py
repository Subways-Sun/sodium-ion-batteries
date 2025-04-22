from sib.literature.lit_processing import read_json, extract_content
import logging
import time
import os

logging.basicConfig(
    filename = f"logs/valid_paper_{time.strftime('%Y-%m-%d_%H%M%S')}.log",
    encoding = "utf-8",
    filemode = "a",
    format = "{asctime} - {levelname} - {message}",
    style = "{",
    datefmt = "%Y-%m-%d %H:%M:%S",
    level = logging.INFO
)

empty_count = 0
with_results = 0
with_abstract = 0

# Directory containing the JSON files
directory_path = "articles_20250313_500_json"  # Update this path
logging.info(f"Processing files in directory: {directory_path}, number of files: {len(os.listdir(directory_path))}")

# Go through each file in the directory
for filename in os.listdir(directory_path):
    if filename.endswith(".json"):
        file_path = os.path.join(directory_path, filename)
        try:
            # Read the JSON file
            data = read_json(file_path)
            logging.info(f"Successfully processed {filename}")
            
            # Check if the data is empty
            if not data:
                empty_count += 1
                logging.warning(f"Empty data in {filename}")
                continue

            results = extract_content(data, "Result")
            experimental = extract_content(data, "Experiment")

            if results:
                with_results += 1
                logging.info(f"Results section found in {filename}")
            
            if experimental:
                with_abstract += 1
                logging.info(f"Experimental section found in {filename}")

            # Process the data as needed
            # For example: extract information, validate, etc.
            
        except Exception as e:
            logging.error(f"Error processing {filename}: {str(e)}")

# Summary of counts
logging.info(f"Total files processed: {len(os.listdir(directory_path))}")
logging.info(f"Empty files: {empty_count}")
logging.info(f"Files with results section: {with_results}")
logging.info(f"Files with experimental section: {with_abstract}")

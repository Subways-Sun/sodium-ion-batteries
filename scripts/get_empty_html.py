import logging
import time
import os

logging.basicConfig(
    filename = f"logs/empty_html_{time.strftime('%Y-%m-%d_%H%M%S')}.log",
    encoding = "utf-8",
    filemode = "a",
    format = "{asctime} - {levelname} - {message}",
    style = "{",
    datefmt = "%Y-%m-%d %H:%M:%S",
    level = logging.INFO
)

directory_path = "articles_20250313_500"  # Update this path
logging.info(f"Processing files in directory: {directory_path}, number of files: {len(os.listdir(directory_path))}")
empty_files = []

for filename in os.listdir(directory_path):
    if filename.endswith(".txt"):
        file_path = os.path.join(directory_path, filename)
        try:
            # Check if file is empty
            if os.stat(file_path).st_size == 0:
                # Strip extension and modify filename
                base_filename = os.path.splitext(filename)[0]
                modified_filename = base_filename.replace("-", "/", 1)
                
                # Add to list of empty files
                empty_files.append(modified_filename)
                logging.info(f"Found empty file: {filename}")
        except Exception as e:
            logging.error(f"Error processing {filename}: {str(e)}")

    # Write empty files to output file
    if 'empty_files' in locals() and empty_files:
        output_path = "articles_20250313_500_output/empty_files.txt"
        with open(output_path, "w", encoding="utf-8") as f:
            for empty_file in empty_files:
                f.write(empty_file + "\n")
        logging.info(f"Wrote {len(empty_files)} empty files to {output_path}")
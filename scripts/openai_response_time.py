import re
import logging
import time
from datetime import datetime

# Set up logging configuration
logging.basicConfig(
    filename=f"logs/openai_response_time_{time.strftime('%Y-%m-%d_%H%M%S')}.log",
    encoding="utf-8",
    filemode="a",
    format="{asctime}.{msecs:03.0f} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.DEBUG
)

log_file_path = r"logs\lit_classification_openai_2025-04-25_174514.log"

def parse_log_file(file_path):
    """Parse the log file and extract timing information."""
    # Update patterns to handle milliseconds
    start_pattern = r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})(?:\.(\d{3}))? - DEBUG - receive_response_headers\.started request=<Request \[b'POST'\]>"
    complete_pattern = r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})(?:\.(\d{3}))? - DEBUG - receive_response_headers\.complete"

    results = []
    start_time = None
    start_line = None

    with open(file_path, 'r', encoding="utf-8") as file:
        for line in file:
            # Check for start line
            start_match = re.match(start_pattern, line)
            if start_match:
                datetime_str = start_match.group(1)
                ms_str = start_match.group(2) or "0"  # Default to 0 if milliseconds not present

                start_time = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
                microseconds = int(ms_str) * 1000  # Convert milliseconds to microseconds
                start_time = start_time.replace(microsecond=microseconds)
                start_line = line.strip()
                continue

            # Check for complete line if we have a start time
            if start_time:
                complete_match = re.match(complete_pattern, line)
                if complete_match:
                    datetime_str = complete_match.group(1)
                    ms_str = complete_match.group(2) or "0"  # Default to 0 if milliseconds not present

                    complete_time = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
                    microseconds = int(ms_str) * 1000  # Convert milliseconds to microseconds
                    complete_time = complete_time.replace(microsecond=microseconds)

                    # Calculate time difference in milliseconds
                    time_diff_ms = (complete_time - start_time).total_seconds() * 1000

                    results.append({
                        'start_time': start_time,
                        'complete_time': complete_time,
                        'time_diff_ms': time_diff_ms,
                        'start_line': start_line,
                        'complete_line': line.strip()
                    })

                    # Reset start_time for next pair
                    start_time = None
                    start_line = None

    return results

# Main execution code - you can run this directly in VSCode
try:
    results = parse_log_file(log_file_path)

    # Log results
    logging.info(f"Found {len(results)} request header operations.")
    logging.info("-" * 80)

    total_time = 0
    for result in results:
        logging.info(f"Start: {result['start_line']}")
        logging.info(f"Complete: {result['complete_line']}")
        logging.info(f"Duration: {result['time_diff_ms']:.3f} ms")
        logging.info("-" * 60)
        total_time += result['time_diff_ms']

    if results:
        avg_time = total_time / len(results)
        logging.info("-" * 80)
        logging.info(f"Average time: {avg_time:.3f} ms")
        logging.info(f"Total time: {total_time:.3f} ms")
        logging.info(f"Number of operations: {len(results)}")

except FileNotFoundError:
    logging.error(f"Error: File '{log_file_path}' not found.")
except Exception as e:
    logging.error(f"Error: {e}")

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

def parse_log_file(file_path):
    """Parse the log file and extract timing information."""
    start_pattern = r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) - DEBUG - send_request_headers\.started request=<Request \[b'POST'\]>"
    complete_pattern = r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) - DEBUG - send_request_headers\.complete"
    
    results = []
    start_time = None
    
    with open(file_path, 'r', encoding="utf-8") as file:
        for line in file:
            # Check for start line
            start_match = re.match(start_pattern, line)
            if start_match:
                start_time = datetime.strptime(start_match.group(1), "%Y-%m-%d %H:%M:%S")
                continue
                
            # Check for complete line if we have a start time
            if start_time:
                complete_match = re.match(complete_pattern, line)
                if complete_match:
                    complete_time = datetime.strptime(complete_match.group(1), "%Y-%m-%d %H:%M:%S")
                    # Calculate time difference in milliseconds
                    time_diff_ms = (complete_time - start_time).total_seconds() * 1000
                    
                    results.append({
                        'start_time': start_time,
                        'complete_time': complete_time,
                        'time_diff_ms': time_diff_ms
                    })
                    
                    # Reset start_time for next pair
                    start_time = None
    
    return results

# Configuration variables - modify these as needed
log_file_path = r"logs\lit_classification_openai_2025-04-25_161454.log"  # Change this to your log file path

# Main execution code - you can run this directly in VSCode
try:
    results = parse_log_file(log_file_path)
    
    # Log results
    logging.info(f"Found {len(results)} request header operations.")
    logging.info("-" * 80)
    logging.info(f"{'Start Time':<25} {'Complete Time':<25} {'Duration (ms)':<15}")
    logging.info("-" * 80)
    
    total_time = 0
    for result in results:
        logging.info(f"{result['start_time']:%Y-%m-%d %H:%M:%S.%f} {result['complete_time']:%Y-%m-%d %H:%M:%S.%f} {result['time_diff_ms']:.2f}")
        total_time += result['time_diff_ms']
    
    if results:
        avg_time = total_time / len(results)
        logging.info("-" * 80)
        logging.info(f"Average time: {avg_time:.2f} ms")
        logging.info(f"Total time: {total_time:.2f} ms")
except FileNotFoundError:
    logging.error(f"Error: File '{log_file_path}' not found.")
except Exception as e:
    logging.error(f"Error: {e}")
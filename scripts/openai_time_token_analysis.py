import re
import os
import time
import logging
from datetime import datetime
from statistics import mean

# Ensure logs directory exists
os.makedirs("logs", exist_ok=True)

# Configure logging as specified
logging.basicConfig(
    filename=f"logs/openai_processing_time_and_tokens_{time.strftime('%Y-%m-%d_%H%M%S')}.log",
    encoding="utf-8",
    filemode="a",
    format="{asctime}.{msecs:03.0f} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.DEBUG
)

def extract_values_from_log(log_file_path):
    """
    Extract token-related metrics and processing time from log files.
    Metrics: openai-processing-ms, total_tokens, reasoning_tokens, 
             completion_tokens, prompt_tokens
    """
    try:
        with open(log_file_path, 'r', encoding='utf-8') as file:
            log_content = file.read()
        
        # Initialize empty lists for each metric
        processing_ms_values = []
        total_tokens_values = []
        reasoning_tokens_values = []
        completion_tokens_values = []
        prompt_tokens_values = []
        
        # Extract values using regex
        processing_ms_matches = re.findall(r"\(b'openai-processing-ms', b'(\d+)'\)", log_content)
        processing_ms_values = [int(value) for value in processing_ms_matches]
        
        total_tokens_matches = re.findall(r"total_tokens=(\d+)", log_content)
        total_tokens_values = [int(value) for value in total_tokens_matches]
        
        reasoning_tokens_matches = re.findall(r"reasoning_tokens=(\d+)", log_content)
        reasoning_tokens_values = [int(value) for value in reasoning_tokens_matches]
        
        completion_tokens_matches = re.findall(r"completion_tokens=(\d+)", log_content)
        completion_tokens_values = [int(value) for value in completion_tokens_matches]
        
        prompt_tokens_matches = re.findall(r"prompt_tokens=(\d+)", log_content)
        prompt_tokens_values = [int(value) for value in prompt_tokens_matches]
        
        # Create results dictionary and calculate averages
        results = {}
        metrics = [
            ("processing_ms", processing_ms_values),
            ("total_tokens", total_tokens_values),
            ("reasoning_tokens", reasoning_tokens_values),
            ("completion_tokens", completion_tokens_values),
            ("prompt_tokens", prompt_tokens_values)
        ]
        
        for metric_name, values in metrics:
            if values:
                results[f"{metric_name}_values"] = values
                results[f"avg_{metric_name}"] = mean(values)
                logging.info(f"Found {len(values)} {metric_name} entries")
            else:
                logging.warning(f"No {metric_name} values found in the log file")
                results[f"{metric_name}_values"] = []
                results[f"avg_{metric_name}"] = 0
        
        # Find the maximum number of entries across all metrics
        max_entries = max(len(values) for _, values in metrics)
        
        # Log each entry with available metrics
        for i in range(max_entries):
            entry_info = f"Entry {i+1} - "
            
            for metric_name, values in metrics:
                if i < len(values):
                    entry_info += f"{metric_name}: {values[i]}, "
            
            # Remove trailing comma and space
            entry_info = entry_info.rstrip(", ")
            logging.info(entry_info)
        
        # Log the averages for each metric
        for metric_name, values in metrics:
            if values:
                logging.info(f"Average {metric_name}: {results[f'avg_{metric_name}']:.2f}")
        
        return results
    
    except Exception as e:
        logging.error(f"Error extracting values from log file: {e}")
        return None

def process_log_file(log_file_path):
    """
    Process a single log file and extract metrics.
    """
    logging.info(f"Processing log file: {log_file_path}")
    
    results = extract_values_from_log(log_file_path)
    
    if results:
        logging.info(f"Successfully extracted values from {log_file_path}")
        
        # Print summary to console
        print(f"\nResults for {os.path.basename(log_file_path)}:")
        
        metrics = [
            "processing_ms",
            "total_tokens",
            "reasoning_tokens",
            "completion_tokens",
            "prompt_tokens"
        ]
        
        for metric in metrics:
            values = results.get(f"{metric}_values", [])
            if values:
                print(f"  Processed {len(values)} {metric} entries")
                print(f"  Average {metric}: {results[f'avg_{metric}']:.2f}")
    else:
        logging.warning(f"Failed to extract values from {log_file_path}")
        print(f"Failed to extract values from {log_file_path}")
    
    return results

if __name__ == "__main__":
    # Paths to your log files - add more files as needed
    log_files = [
        "path/to/first/logfile.log",   # Replace with actual path
    ]
    
    # Process each log file
    all_results = {}
    for log_file in log_files:
        if os.path.exists(log_file):
            all_results[log_file] = process_log_file(log_file)
        else:
            logging.error(f"Log file not found: {log_file}")
            print(f"Error: Log file not found: {log_file}")
    
    # Initialize containers for overall metrics
    all_metrics = {
        "processing_ms": [],
        "total_tokens": [],
        "reasoning_tokens": [],
        "completion_tokens": [],
        "prompt_tokens": []
    }
    
    # Collect all values across files
    for file_results in all_results.values():
        if file_results:
            for metric in all_metrics:
                all_metrics[metric].extend(file_results.get(f"{metric}_values", []))
    
    # Log and print overall averages
    print("\n--- Overall Averages Across All Files ---")
    for metric, values in all_metrics.items():
        if values:
            overall_avg = mean(values)
            logging.info(f"Overall average {metric} across all files: {overall_avg:.2f}")
            
            # Format output based on metric type
            if metric == "processing_ms":
                print(f"Overall average {metric}: {overall_avg:.2f} ms")
            else:
                print(f"Overall average {metric}: {overall_avg:.2f} tokens")
    
    logging.info("Script execution completed")
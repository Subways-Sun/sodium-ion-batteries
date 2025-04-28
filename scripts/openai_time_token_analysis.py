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
    filename=f"logs/openai_time_token_analysis_{time.strftime('%Y-%m-%d_%H%M%S')}.log",
    encoding="utf-8",
    filemode="a",
    format="{asctime}.{msecs:03.0f} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.DEBUG
)

def extract_values_from_log(log_file_path):
    """
    Extract 'openai-processing-ms', 'total_tokens', and 'reasoning_tokens' values from a log file
    and calculate averages.
    """
    try:
        with open(log_file_path, 'r', encoding='utf-8') as file:
            log_content = file.read()
        
        # Initialize empty lists for each metric
        processing_ms_values = []
        total_tokens_values = []
        reasoning_tokens_values = []
        
        # Extract all 'openai-processing-ms' values using regex
        processing_ms_matches = re.findall(r"\(b'openai-processing-ms', b'(\d+)'\)", log_content)
        processing_ms_values = [int(value) for value in processing_ms_matches]
        
        # Extract all 'total_tokens' values using regex
        total_tokens_matches = re.findall(r"total_tokens=(\d+)", log_content)
        total_tokens_values = [int(value) for value in total_tokens_matches]
        
        # Extract all 'reasoning_tokens' values using regex
        reasoning_tokens_matches = re.findall(r"reasoning_tokens=(\d+)", log_content)
        reasoning_tokens_values = [int(value) for value in reasoning_tokens_matches]
        
        # Calculate averages (only if values exist)
        results = {}
        
        if processing_ms_values:
            results["processing_ms_values"] = processing_ms_values
            results["avg_processing_ms"] = mean(processing_ms_values)
            logging.info(f"Found {len(processing_ms_values)} openai-processing-ms entries")
        else:
            logging.warning("No openai-processing-ms values found in the log file")
            results["processing_ms_values"] = []
            results["avg_processing_ms"] = 0
        
        if total_tokens_values:
            results["total_tokens_values"] = total_tokens_values
            results["avg_total_tokens"] = mean(total_tokens_values)
            logging.info(f"Found {len(total_tokens_values)} total_tokens entries")
        else:
            logging.warning("No total_tokens values found in the log file")
            results["total_tokens_values"] = []
            results["avg_total_tokens"] = 0
        
        if reasoning_tokens_values:
            results["reasoning_tokens_values"] = reasoning_tokens_values
            results["avg_reasoning_tokens"] = mean(reasoning_tokens_values)
            logging.info(f"Found {len(reasoning_tokens_values)} reasoning_tokens entries")
        else:
            logging.warning("No reasoning_tokens values found in the log file")
            results["reasoning_tokens_values"] = []
            results["avg_reasoning_tokens"] = 0
        
        # Log the extracted values
        max_entries = max(
            len(processing_ms_values),
            len(total_tokens_values),
            len(reasoning_tokens_values)
        )
        
        for i in range(max_entries):
            entry_info = f"Entry {i+1} - "
            
            if i < len(processing_ms_values):
                entry_info += f"openai-processing-ms: {processing_ms_values[i]}, "
            
            if i < len(total_tokens_values):
                entry_info += f"total_tokens: {total_tokens_values[i]}, "
            
            if i < len(reasoning_tokens_values):
                entry_info += f"reasoning_tokens: {reasoning_tokens_values[i]}, "
            
            # Remove trailing comma and space
            entry_info = entry_info.rstrip(", ")
            
            logging.info(entry_info)
        
        # Log the averages
        if processing_ms_values:
            logging.info(f"Average openai-processing-ms: {results['avg_processing_ms']:.2f}")
        
        if total_tokens_values:
            logging.info(f"Average total_tokens: {results['avg_total_tokens']:.2f}")
        
        if reasoning_tokens_values:
            logging.info(f"Average reasoning_tokens: {results['avg_reasoning_tokens']:.2f}")
        
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
        
        if results["processing_ms_values"]:
            print(f"  Processed {len(results['processing_ms_values'])} openai-processing-ms entries")
            print(f"  Average openai-processing-ms: {results['avg_processing_ms']:.2f} ms")
        
        if results["total_tokens_values"]:
            print(f"  Processed {len(results['total_tokens_values'])} total_tokens entries")
            print(f"  Average total_tokens: {results['avg_total_tokens']:.2f} tokens")
        
        if results["reasoning_tokens_values"]:
            print(f"  Processed {len(results['reasoning_tokens_values'])} reasoning_tokens entries")
            print(f"  Average reasoning_tokens: {results['avg_reasoning_tokens']:.2f} tokens")
    else:
        logging.warning(f"Failed to extract values from {log_file_path}")
        print(f"Failed to extract values from {log_file_path}")
    
    return results

if __name__ == "__main__":
    # Paths to your log files - add more files as needed
    log_files = [
        "logs/info_extraction_openai_2025-04-27_232924_gpt-4o.log",   # Replace with actual path
    ]
    
    # Process each log file
    all_results = {}
    for log_file in log_files:
        if os.path.exists(log_file):
            all_results[log_file] = process_log_file(log_file)
        else:
            logging.error(f"Log file not found: {log_file}")
            print(f"Error: Log file not found: {log_file}")
    
    # Calculate overall averages across all files
    all_processing_ms = []
    all_total_tokens = []
    all_reasoning_tokens = []
    
    for file_results in all_results.values():
        if file_results:
            all_processing_ms.extend(file_results.get("processing_ms_values", []))
            all_total_tokens.extend(file_results.get("total_tokens_values", []))
            all_reasoning_tokens.extend(file_results.get("reasoning_tokens_values", []))
    
    # Log and print overall averages
    if all_processing_ms:
        overall_avg_processing_ms = mean(all_processing_ms)
        overall_median_processing_ms = sorted(all_processing_ms)[len(all_processing_ms) // 2]
        logging.info(f"Overall average openai-processing-ms across all files: {overall_avg_processing_ms:.2f}")
        logging.info(f"Overall median openai-processing-ms across all files: {overall_median_processing_ms:.2f}")
        print(f"\nOverall average openai-processing-ms: {overall_avg_processing_ms:.2f} ms")
        print(f"Overall median openai-processing-ms: {overall_median_processing_ms:.2f} ms")
    
    if all_total_tokens:
        overall_avg_total_tokens = mean(all_total_tokens)
        overall_median_total_tokens = sorted(all_total_tokens)[len(all_total_tokens) // 2]
        logging.info(f"Overall average total_tokens across all files: {overall_avg_total_tokens:.2f}")
        logging.info(f"Overall median total_tokens across all files: {overall_median_total_tokens:.2f}")
        print(f"Overall average total_tokens: {overall_avg_total_tokens:.2f} tokens")
        print(f"Overall median total_tokens: {overall_median_total_tokens:.2f} tokens")
    
    if all_reasoning_tokens:
        overall_avg_reasoning_tokens = mean(all_reasoning_tokens)
        overall_median_reasoning_tokens = sorted(all_reasoning_tokens)[len(all_reasoning_tokens) // 2]
        logging.info(f"Overall average reasoning_tokens across all files: {overall_avg_reasoning_tokens:.2f}")
        logging.info(f"Overall median reasoning_tokens across all files: {overall_median_reasoning_tokens:.2f}")
        print(f"Overall average reasoning_tokens: {overall_avg_reasoning_tokens:.2f} tokens")
        print(f"Overall median reasoning_tokens: {overall_median_reasoning_tokens:.2f} tokens")
    
    logging.info("Script execution completed")
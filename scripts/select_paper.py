import random

def sample_lines(input_file, output_file, num_lines=500):
    """
    Randomly extract a specified number of lines from a text file
    
    Args:
        input_file (str): Path to the input text file
        output_file (str): Path to save the sampled lines
        num_lines (int): Number of lines to sample (default: 500)
    """
    # Read all lines from the input file
    with open(input_file, 'r') as file:
        all_lines = file.readlines()
    
    # Check if we have enough lines
    total_lines = len(all_lines)
    if total_lines <= num_lines:
        print(f"Warning: File only contains {total_lines} lines, which is less than requested {num_lines}.")
        sampled_lines = all_lines
    else:
        # Randomly sample the lines
        sampled_lines = random.sample(all_lines, num_lines)
    
    sampled_lines.sort()  # Sort the sampled lines for consistency
    # Write the sampled lines to the output file
    with open(output_file, 'w') as file:
        file.writelines(sampled_lines)
    
    print(f"Successfully extracted {len(sampled_lines)} lines to {output_file}")

# if __name__ == "__main__":
#     import argparse
    
#     parser = argparse.ArgumentParser(description="Randomly sample lines from a text file")
#     parser.add_argument("input_file", help="Path to the input text file")
#     parser.add_argument("output_file", help="Path to save the sampled lines")
#     parser.add_argument("-n", "--num_lines", type=int, default=500,
#                         help="Number of lines to sample (default: 500)")
    
#     args = parser.parse_args()
    
#     sample_lines(args.input_file, args.output_file, args.num_lines)

sample_lines("data/relevant_dois_20250313-003348_bak.txt", "data/selected_papers.txt", 500)
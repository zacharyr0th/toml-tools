import os
import re
import sys
from datetime import datetime

def extract_repo_name(url):
    """Extract repository name from GitHub URL."""
    match = re.search(r'https://github\.com/([^/]+/[^/]+)', url)
    return match.group(1) if match else None

def remove_duplicates(input_file, output_file):
    """
    Remove duplicate repository URLs from input file and write unique URLs to output file.
    
    Args:
        input_file (str): Path to input file containing repository URLs
        output_file (str): Path to output file where unique URLs will be written
    """
    # Add timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    try:
        # Read all lines from the input file
        with open(input_file, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found")
        sys.exit(1)

    # Track unique repositories
    unique_repos = {}
    
    # Process each line
    for line in lines:
        url = line.strip()
        if url:
            repo_name = extract_repo_name(url)
            if repo_name:
                unique_repos[repo_name] = url

    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Calculate statistics
    total_urls = len(lines)
    unique_count = len(unique_repos)
    duplicate_count = total_urls - unique_count
    duplicate_percentage = (duplicate_count / total_urls * 100) if total_urls > 0 else 0

    # Write to the output file
    with open(output_file, 'w') as f:
        # Write analysis section
        f.write(f"Analysis Report\n")
        f.write(f"==============\n")
        f.write(f"Generated on: {timestamp}\n\n")
        f.write(f"Summary Statistics:\n")
        f.write(f"- Total URLs analyzed: {total_urls}\n")
        f.write(f"- Unique repositories: {unique_count}\n")
        f.write(f"- Duplicates removed: {duplicate_count}\n")
        f.write(f"- Duplicate percentage: {duplicate_percentage:.1f}%\n\n")
        f.write(f"Repository List:\n")
        f.write(f"===============\n\n")
        
        # Write unique repos
        for url in sorted(unique_repos.values()):
            f.write(f"{url}\n")

    print(f"Found {len(lines)} total URLs")
    print(f"Found {len(unique_repos)} unique repositories")
    print(f"Removed {len(lines) - len(unique_repos)} duplicates")
    print(f"Results written to: {output_file}")

if __name__ == "__main__":
    # Check if ecosystem argument is provided
    if len(sys.argv) != 2:
        print("Usage: python3 remove_duplicates.py <ecosystem>")
        print("Example: python3 remove_duplicates.py aptos")
        sys.exit(1)
    
    # Get the ecosystem name from command line argument
    ecosystem = sys.argv[1]
    
    # Get current date for filename
    date_str = datetime.now().strftime("%y-%m-%d")
    
    # Get the project root directory (one level up from script_dir)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(script_dir))
    
    # Construct file paths
    input_file = os.path.join(script_dir, "potential-duplicates.txt")
    output_file = os.path.join(project_root, 'output', f'{ecosystem}-unique-{date_str}.txt')
    
    remove_duplicates(input_file, output_file)
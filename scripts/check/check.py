import re
import os
import sys
from datetime import datetime

def extract_urls_from_toml(filename):
    """Extract repository URLs from ecosystem.toml file."""
    urls = set()
    try:
        with open(filename, 'r') as file:
            for line in file:
                if 'url = ' in line:
                    # Extract URL between quotes
                    match = re.search(r'url = "([^"]+)"', line)
                    if match:
                        urls.add(match.group(1))
    except FileNotFoundError:
        print(f"Warning: {filename} not found")
        return set()
    
    print(f"Found {len(urls)} unique repositories in {filename}")
    return urls

def load_repos_from_txt(filename):
    """Load repository URLs from new-repos.txt file."""
    urls = set()
    total_lines = 0
    try:
        with open(filename, 'r') as file:
            for line in file:
                total_lines += 1
                url = line.strip()
                if url.startswith('https://github.com/'):
                    urls.add(url)
    except FileNotFoundError:
        print(f"Warning: {filename} not found")
        return set()
    
    print(f"Found {len(urls)} unique repositories out of {total_lines} total lines in {filename}")
    return urls

def write_results_to_file(included, not_included, output_filename, filename_base):
    """Write comparison results to output file."""
    with open(output_filename, 'w') as f:
        # Calculate statistics
        total_repos = len(included) + len(not_included)
        included_percentage = (len(included) / total_repos * 100) if total_repos > 0 else 0
        not_included_percentage = (len(not_included) / total_repos * 100) if total_repos > 0 else 0

        # Write analysis section
        f.write(f"Analysis Report\n")
        f.write(f"==============\n")
        f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write(f"Summary Statistics:\n")
        f.write(f"- Total repositories analyzed: {total_repos}\n")
        f.write(f"- Already in {filename_base}.toml: {len(included)} ({included_percentage:.1f}%)\n")
        f.write(f"- Not in {filename_base}.toml: {len(not_included)} ({not_included_percentage:.1f}%)\n\n")
        
        f.write(f"Detailed Results:\n")
        f.write(f"===============\n\n")
        
        f.write(f"Repos already in {filename_base}.toml:\n")
        f.write(f"--------------------------------\n")
        for repo in sorted(included):
            f.write(f"{repo}\n")
        
        f.write(f"\nRepos not in {filename_base}.toml:\n")
        f.write(f"----------------------------\n")
        for repo in sorted(not_included):
            f.write(f"{repo}\n")

def main():
    # Check if filename argument is provided
    if len(sys.argv) != 2:
        print("Usage: python3 check_repos.py <filename>")
        sys.exit(1)
    
    # Get the filename from command line argument (without extension)
    filename_base = sys.argv[1]
    
    # Get current date for filename
    date_str = datetime.now().strftime("%y-%m-%d")
    
    # Get the project root directory (one level up from script_dir)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(script_dir))
    
    # Construct file paths
    toml_file = os.path.join(project_root, 'input', f'{filename_base}.toml')
    
    # Load repositories from both files
    toml_repos = extract_urls_from_toml(toml_file)
    new_repos = load_repos_from_txt(os.path.join(script_dir, 'new-repos.txt'))
    
    # Find intersections and differences
    included = new_repos & toml_repos
    not_included = new_repos - toml_repos
    
    # Write results with date in filename
    output_filename = os.path.join(project_root, 'output', f'{filename_base}-check-{date_str}.txt')
    write_results_to_file(included, not_included, output_filename, filename_base)
    
    print(f"Results have been written to: {output_filename}")
    print(f"Total repos already in {filename_base}.toml: {len(included)}")
    print(f"Total repos not in {filename_base}.toml: {len(not_included)}")

if __name__ == "__main__":
    main()
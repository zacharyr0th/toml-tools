import os
import re

def extract_repo_name(url):
    match = re.search(r'https://github\.com/([^/]+/[^/]+)', url)
    return match.group(1) if match else None

def remove_duplicates(input_file, output_file):
    # Read all lines from the input file
    with open(input_file, 'r') as f:
        lines = f.readlines()

    # Extract repo names and remove duplicates
    unique_repos = {}
    for line in lines:
        repo_name = extract_repo_name(line.strip())
        if repo_name:
            unique_repos[repo_name] = line.strip()

    # Write unique repos to the output file
    with open(output_file, 'w') as f:
        for url in unique_repos.values():
            f.write(f"{url}\n")

    print(f"Original count: {len(lines)}")
    print(f"Unique count: {len(unique_repos)}")

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "original.txt")
    output_file = os.path.join(script_dir, "unique_repos.txt")

    remove_duplicates(input_file, output_file)
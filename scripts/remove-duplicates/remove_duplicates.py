import os
import re

def extract_repo_name(url):
    match = re.search(r'https://github\.com/([^/]+/[^/]+)', url)
    return match.group(1) if match else None

def remove_duplicates(input_file, output_file):
    # Read all lines from the input file
    with open(input_file, 'r') as f:
        lines = f.readlines()

    # Extract repo names and track duplicates and invalid URLs
    unique_repos = {}
    duplicate_repos = {}
    invalid_urls = []
    
    for line in lines:
        line = line.strip()
        repo_name = extract_repo_name(line)
        if repo_name:
            if repo_name in unique_repos:
                duplicate_repos.setdefault(repo_name, []).append(line)
            else:
                unique_repos[repo_name] = line
        else:
            invalid_urls.append(line)

    # Write to the output file
    with open(output_file, 'w') as f:
        # Write unique repos
        for url in unique_repos.values():
            f.write(f"{url}\n")
        
        # Write duplicate repos section
        if duplicate_repos:
            f.write("\n# Duplicate repos:\n")
            for repo_name, urls in duplicate_repos.items():
                f.write(f"\n## {repo_name}:\n")
                for url in urls:
                    f.write(f"{url}\n")
        
        # Write invalid URLs section
        if invalid_urls:
            f.write("\n# Invalid or non-GitHub URLs:\n")
            for url in invalid_urls:
                f.write(f"{url}\n")

    print(f"Original count: {len(lines)}")
    print(f"Unique count: {len(unique_repos)}")
    print(f"Duplicate repos: {len(duplicate_repos)}")
    print(f"Invalid URLs: {len(invalid_urls)}")

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "original.txt")
    output_file = os.path.join(script_dir, "unique_repos.txt")

    remove_duplicates(input_file, output_file)
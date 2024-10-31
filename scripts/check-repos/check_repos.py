import re
import os

def extract_urls_from_toml(filename):
    """Extract repository URLs from aptos.toml file."""
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

def write_results_to_file(included, not_included, output_filename):
    """Write comparison results to output file."""
    with open(output_filename, 'w') as f:
        f.write("Repos already in aptos.toml:\n")
        for repo in sorted(included):
            f.write(f"{repo}\n")
        
        f.write(f"\nRepos not in aptos.toml ({len(not_included)} repos):\n")
        for repo in sorted(not_included):
            f.write(f"{repo}\n")
        
        f.write(f"\nTotal repos already in aptos.toml: {len(included)}\n")
        f.write(f"Total repos not in aptos.toml: {len(not_included)}\n")

def main():
    # Get the script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Load repositories from both files
    toml_repos = extract_urls_from_toml(os.path.join(script_dir, 'aptos.toml'))
    new_repos = load_repos_from_txt(os.path.join(script_dir, 'new-repos.txt'))
    
    # Find intersections and differences
    included = new_repos & toml_repos
    not_included = new_repos - toml_repos
    
    # Write results
    output_filename = os.path.join(script_dir, 'repo_check_results.txt')
    write_results_to_file(included, not_included, output_filename)
    
    print(f"Results have been written to: {output_filename}")
    print(f"Total repos already in aptos.toml: {len(included)}")
    print(f"Total repos not in aptos.toml: {len(not_included)}")

if __name__ == "__main__":
    main()
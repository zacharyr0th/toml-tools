import re
import os

def load_repos_from_toml(filename):
    with open(filename, 'r') as file:
        content = file.read()
    return set(re.findall(r'url = "([^"]+)"', content))

def load_repos_from_txt(filename):
    with open(filename, 'r') as file:
        return set(line.strip() for line in file)

def check_inclusion(main_set, check_set):
    included = check_set & main_set
    not_included = check_set - main_set
    return included, not_included

def write_results_to_file(included, not_included, output_filename):
    with open(output_filename, 'w') as f:
        f.write("Repos already in aptos.toml:\n")
        for repo in sorted(included):
            f.write(repo + "\n")
        f.write("\nRepos not in aptos.toml:\n")
        for repo in sorted(not_included):
            f.write(repo + "\n")
        f.write(f"\nTotal repos in aptos.toml: {len(included)}\n")
        f.write(f"Total repos not in aptos.toml: {len(not_included)}\n")

def main():
    # Load the main list of repos from aptos.toml
    main_set = load_repos_from_toml('aptos.toml')

    # Load the list of repos to check from new-repos.txt
    check_set = load_repos_from_txt('new-repos.txt')

    # Check inclusion
    included, not_included = check_inclusion(main_set, check_set)

    # Write results to a file in the same directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_filename = os.path.join(script_dir, 'repo_check_results.txt')
    write_results_to_file(included, not_included, output_filename)
    
    print(f"Results have been written to: {output_filename}")

if __name__ == "__main__":
    main()
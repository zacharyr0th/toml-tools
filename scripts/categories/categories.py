import os
import sys
import re
from collections import defaultdict
from typing import Dict, List

# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from report.constants import COMPILED_CATEGORIES, REPO_PATTERN
from report.utils import extract_repo_info

def categorize_repos(repos: List[Dict[str, str]], categories: Dict[str, List[re.Pattern]]) -> Dict[str, List[str]]:
    """Categorize repositories based on predefined patterns."""
    categorized_repos = defaultdict(list)
    for repo in repos:
        repo_url = repo['url']
        for category, patterns in categories.items():
            if any(pattern.search(repo_url) for pattern in patterns):
                categorized_repos[category].append(repo_url)
                break
        else:
            categorized_repos["Uncategorized"].append(repo_url)
    return categorized_repos

def generate_category_lists(input_folder: str, output_folder: str) -> None:
    """Generate lists of repositories for each category from TOML files."""
    os.makedirs(output_folder, exist_ok=True)

    all_repos = []
    for filename in os.listdir(input_folder):
        if filename.endswith('.toml'):
            with open(os.path.join(input_folder, filename), 'r', encoding='utf-8') as file:
                content = file.read()
                _, repos, _, _, _, _ = extract_repo_info(content)
                all_repos.extend(repos)

    categorized_repos = categorize_repos(all_repos, COMPILED_CATEGORIES)

    for category, repos in categorized_repos.items():
        output_file = os.path.join(output_folder, f"{category.lower()}_repos.txt")
        with open(output_file, 'w', encoding='utf-8') as f:
            for repo in sorted(repos):
                f.write(f"{repo}\n")
        print(f"Generated list for {category}: {output_file}")

def main():
    if len(sys.argv) != 3:
        print("Usage: python category_repo_lister.py <input_folder> <output_folder>")
        sys.exit(1)

    input_folder = sys.argv[1]
    output_folder = sys.argv[2]

    if not os.path.exists(input_folder):
        print(f"Error: Input folder '{input_folder}' does not exist.")
        sys.exit(1)

    generate_category_lists(input_folder, output_folder)

if __name__ == "__main__":
    main()
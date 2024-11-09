"""Module for generating reports from TOML files containing repository information."""

from datetime import datetime
from typing import List
import os
import logging
from report.constants import COMPILED_CATEGORIES
from .utils import categorize_repos, extract_repo_info

def generate_master_report(toml_files: List[str], output_file: str) -> None:
    """Generate a master report from multiple TOML files."""
    ecosystem_data = []

    for input_file in toml_files:
        with open(input_file, 'r', encoding='utf-8') as file:
            content = file.read()

        total_repos, repos, github_accounts, _, _, _ = extract_repo_info(content)
        
        ecosystem_name = os.path.splitext(os.path.basename(input_file))[0]
        logging.debug("Ecosystem: %s, Total repos: %d", ecosystem_name, total_repos)
        
        sub_ecosystem_repos = categorize_repos(repos, COMPILED_CATEGORIES)

        # Convert account sets to lengths if they're sets
        github_count = len(github_accounts) if isinstance(github_accounts, set) else github_accounts

        category_stats = {
            cat: {
                'count': len(cat_repos),
                'percentage': f"{(len(cat_repos) / total_repos * 100):.2f}%" if total_repos > 0 else "0.00%"
            }
            for cat, cat_repos in sub_ecosystem_repos.items()
        }

        ecosystem_data.append({
            'name': ecosystem_name,
            'total_repos': total_repos,
            'github_accounts': github_count,
            'categories': category_stats
        })

    # Sort ecosystem_data by total_repos in descending order
    ecosystem_data.sort(key=lambda x: x['total_repos'], reverse=True)

    # Generate the report
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# Ecosystem Analysis Report\n\n")
        f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        # Summary table (will now be sorted by total repos)
        f.write("## Summary\n\n")
        f.write("| Ecosystem | Total Repos | GitHub Accounts |\n")
        f.write("|-----------|-------------|------------------|\n")
        
        for data in ecosystem_data:
            f.write(f"| {data['name']} | {data['total_repos']} | {data['github_accounts']} |\n")
        
        f.write("\n## Category Distribution\n\n")
        
        # Category distribution table
        categories = set()
        for data in ecosystem_data:
            categories.update(data['categories'].keys())
        
        header = "| Ecosystem | " + " | ".join(sorted(categories)) + " |"
        separator = "|-----------|" + "|".join(["-" * len(cat) for cat in sorted(categories)]) + "|"
        
        f.write(f"{header}\n")
        f.write(f"{separator}\n")
        
        for data in ecosystem_data:
            row = [data['name']]
            for category in sorted(categories):
                stats = data['categories'].get(category, {'count': 0, 'percentage': "0.00%"})
                row.append(f"{stats['count']}<br>{stats['percentage']}")
            f.write(f"| {' | '.join(row)} |\n")

def main() -> None:
    """Generate a single report for all TOML files in the input folder."""
    current_date = datetime.now().strftime("%m-%d-%y")
    
    # Get the project root directory (three levels up from this script)
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    input_dir = os.path.join(project_root, 'input')
    output_dir = os.path.join(project_root, 'output')
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    if not os.path.exists(input_dir):
        logging.error("Input folder '%s' does not exist.", input_dir)
        logging.info("Current working directory: %s", os.getcwd())
        logging.info("Please make sure you're running the script from the correct directory.")
        return

    try:
        toml_files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.endswith('.toml')]
    except OSError as e:
        logging.error("Error accessing the input folder: %s", e)
        return

    if not toml_files:
        logging.error("No .toml files found in the input folder.")
        return

    output_filename = f"report-{current_date}.md"
    output_path = os.path.join(output_dir, output_filename)
    
    generate_master_report(toml_files, output_path)
    logging.info("Generated report for all TOML files -> %s", output_filename)
    logging.info("Report has been generated for all TOML files and saved in the 'output' folder.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    main()

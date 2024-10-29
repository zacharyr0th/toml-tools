"""Module for generating reports from TOML files containing repository information."""

from datetime import datetime
from typing import List, Dict
import os
import sys
import logging
from report.constants import COMPILED_CATEGORIES
from .utils import categorize_repos, extract_repo_info

def generate_master_report(toml_files: List[str], output_file: str) -> None:
    """Generate a master report from multiple TOML files."""
    ecosystem_data = []

    for input_file in toml_files:
        with open(input_file, 'r', encoding='utf-8') as file:
            content = file.read()

        total_repos, repos, github_accounts, missing_repos, org_accounts, individual_accounts = extract_repo_info(content)
        
        ecosystem_name = os.path.splitext(os.path.basename(input_file))[0]
        logging.debug("Ecosystem: %s, Total repos: %d", ecosystem_name, total_repos)
        
        sub_ecosystem_repos = categorize_repos(repos, COMPILED_CATEGORIES)

        category_stats = {
            cat: {
                'count': len(repos),
                'percentage': f"{(len(repos) / total_repos * 100):.2f}%" if total_repos > 0 else "0.00%"
            }
            for cat, repos in sub_ecosystem_repos.items()
        }

        ecosystem_data.append({
            'name': ecosystem_name.capitalize(),
            'total_repos': total_repos,
            'github_accounts': len(github_accounts),
            'individual_accounts': len(individual_accounts),
            'org_accounts': len(org_accounts),
            'categories': category_stats
        })  

    ecosystem_data.sort(key=lambda x: x['total_repos'], reverse=True)

    write_report(ecosystem_data, output_file)

def write_report(ecosystem_data: List[Dict], output_file: str) -> None:
    """Write the generated report to a file."""
    with open(output_file, 'w', encoding='utf-8') as master_file:
        total_repos = sum(eco['total_repos'] for eco in ecosystem_data)
        total_github_accounts = sum(eco['github_accounts'] for eco in ecosystem_data)
        master_file.write("# Ecosystem Analysis Report\n\n")
        master_file.write(f"- Total Repositories: {total_repos:,}\n")
        master_file.write(f"- Total Github Accounts: {total_github_accounts:,}\n\n")

        master_file.write("| Ecosystem | Total Repos | GitHub Accounts | Individuals | Organizations | DeFi | Gaming | Social | Infrastructure | NFTs | Uncategorized |\n")
        master_file.write("|-----------|-------------|-----------------|---------------------|-------------------|------|--------|--------|----------------|------|---------------|\n")
        
        for ecosystem in ecosystem_data:
            master_file.write(f"| {ecosystem['name']} | ")
            master_file.write(f"{ecosystem['total_repos']:,} | ")
            master_file.write(f"{ecosystem['github_accounts']:,} | ")
            master_file.write(f"{ecosystem['individual_accounts']:,} | ")
            master_file.write(f"{ecosystem['org_accounts']:,} | ")
            for category in ['DeFi', 'Gaming', 'Social', 'Infrastructure', 'NFTs', 'Uncategorized']:
                master_file.write(f"{ecosystem['categories'].get(category, {'percentage': '0.00%'})['percentage']} | ")
            master_file.write("\n")

        master_file.write("\n## All Ecosystems\n\n")
        
        # Create a single table for all ecosystem summaries
        headers = ["Metric"] + [eco['name'] for eco in ecosystem_data]
        master_file.write("| " + " | ".join(headers) + " |\n")
        master_file.write("|" + "---|" * len(headers) + "\n")

        metrics = [
            ("Total Repositories", 'total_repos'),
            ("GitHub Accounts", 'github_accounts'),
            ("Individuals", 'individual_accounts'),
            ("Organizations", 'org_accounts'),
            ("DeFi", 'DeFi'),
            ("Gaming", 'Gaming'),
            ("Social", 'Social'),
            ("Infrastructure", 'Infrastructure'),
            ("NFTs", 'NFTs'),
            ("Uncategorized", 'Uncategorized')
        ]

        for metric_name, metric_key in metrics:
            row = [metric_name]
            for eco in ecosystem_data:
                if metric_key in ['total_repos', 'github_accounts', 'individual_accounts', 'org_accounts']:
                    value = f"{eco[metric_key]:,}"
                else:
                    value = eco['categories'].get(metric_key, {'percentage': '0.00%'})['percentage']
                row.append(value)
            master_file.write("| " + " | ".join(row) + " |\n")

    logging.debug("Final total repos across all ecosystems: %d", total_repos)
    logging.debug("Final total GitHub accounts across all ecosystems: %d", total_github_accounts)

def generate_report(input_file: str, output_file: str) -> None:
    """Generate a report for a single TOML file."""
    generate_master_report([input_file], output_file)

def main() -> None:
    """Generate a single report for all TOML files in the input folder."""
    current_date = datetime.now().strftime("%m-%d-%y")
    os.makedirs('output', exist_ok=True)

    input_folder = 'input'
    
    # Check if the input folder exists
    if not os.path.exists(input_folder):
        logging.error("Input folder '%s' does not exist.", input_folder)
        logging.info("Current working directory: %s", os.getcwd())
        logging.info("Please make sure you're running the script from the correct directory.")
        sys.exit(1)

    try:
        toml_files = [os.path.join(input_folder, f) for f in os.listdir(input_folder) if f.endswith('.toml')]
    except OSError as e:
        logging.error("Error accessing the input folder: %s", e)
        sys.exit(1)

    if not toml_files:
        logging.error("No .toml files found in the input folder.")
        sys.exit(1)

    output_filename = f"report-{current_date}.md"
    output_path = os.path.join('output', output_filename)
    
    generate_master_report(toml_files, output_path)
    logging.info("Generated report for all TOML files -> %s", output_filename)

    logging.info("Report has been generated for all TOML files and saved in the 'output' folder.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    main()

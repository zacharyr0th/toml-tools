"""Module for generating reports from TOML files containing repository information."""

import os
import logging
from datetime import datetime
from typing import List, Dict, Tuple
from collections import defaultdict
from constants import COMPILED_CATEGORIES, CATEGORIES
from utils import categorize_repos, extract_repo_info
from verbose_generator import generate_verbose_section

def process_ecosystem(content: str) -> Tuple[int, List[str], set, Dict, Dict, int, Dict]:
    """Process a single ecosystem's TOML content and return analysis data."""
    # Add debug logging
    logging.info("Starting ecosystem processing")
    
    # Get basic repo info
    total_repos, repos, categories, _, _, _ = extract_repo_info(content)
    logging.info(f"Found {total_repos} repositories to process")
    
    # Debug: Print first few repos
    if repos:
        logging.info(f"Sample repos: {repos[:3]}")
    
    # Categorize repositories and get pattern matches
    categorized_repos, pattern_matches = categorize_repos(repos, CATEGORIES)
    
    # Debug: Print categorization results
    for category, repos_list in categorized_repos.items():
        logging.info(f"Category {category}: {len(repos_list)} repositories")
    
    # Calculate statistics for each category
    category_stats = {}
    total_categorized = 0
    
    # Calculate statistics for each category
    for category in CATEGORIES.keys():
        if category == "Uncategorized":
            continue
            
        category_repos = categorized_repos.get(category, [])
        count = len(category_repos)
        percentage = (count / total_repos * 100) if total_repos > 0 else 0
        
        category_stats[category] = {
            'count': count,
            'percentage': f"{percentage:.2f}%",
            'pattern_matches': pattern_matches.get(category, {}),
            'categorized_repos': category_repos
        }
        total_categorized += count
    
    # Add uncategorized stats
    uncategorized_repos = categorized_repos.get("Uncategorized", [])
    category_stats["Uncategorized"] = {
        'count': len(uncategorized_repos),
        'percentage': f"{(len(uncategorized_repos) / total_repos * 100):.2f}%",
        'pattern_matches': pattern_matches.get("Uncategorized", {}),
        'categorized_repos': uncategorized_repos
    }
    
    logging.info(f"Total categorized: {total_categorized}")
    logging.info(f"Total uncategorized: {len(uncategorized_repos)}")
    
    return total_repos, repos, categories, pattern_matches, category_stats, total_categorized, {}

def generate_master_report(toml_files: List[str], output_file: str, verbose: bool = False) -> None:
    """Generate the master report."""
    ecosystem_data = []
    total_all_repos = 0
    
    # Process all ecosystems first
    for input_file in toml_files:
        ecosystem_name = os.path.basename(input_file).replace('.toml', '')
        
        with open(input_file, 'r', encoding='utf-8') as infile:
            content = infile.read()
            
        total_repos, repos, _, pattern_matches, category_stats, total_categorized, _ = process_ecosystem(content)
        
        # Add category counts to report
        with open(output_file, 'w', encoding='utf-8') as outfile:
            outfile.write("# Ecosystem Analysis Report\n\n")
            
            # Write overall statistics
            outfile.write("## Overall Statistics\n")
            outfile.write("| Metric | Count |\n")
            outfile.write("|--------|-------|\n")
            outfile.write(f"| Total repositories | {total_repos:,} |\n")
            
            # Write category statistics
            outfile.write("\n## Category Statistics\n")
            outfile.write("| Category | Repository Count | Percentage |\n")
            outfile.write("|----------|------------------|------------|\n")
            
            # Sort categories by count (excluding Uncategorized)
            sorted_categories = sorted(
                [(k, v['count'], v['percentage']) for k, v in category_stats.items() if k != "Uncategorized"],
                key=lambda x: x[1],
                reverse=True
            )
            
            # Write sorted categories
            for category, count, percentage in sorted_categories:
                outfile.write(f"| {category} | {count:,} | {percentage} |\n")
            
            # Write uncategorized at the end
            if "Uncategorized" in category_stats:
                uncat = category_stats["Uncategorized"]
                outfile.write(f"| Uncategorized | {uncat['count']:,} | {uncat['percentage']} |\n")
            
            # If verbose, add detailed pattern analysis
            if verbose:
                outfile.write("\n## Detailed Pattern Analysis\n\n")
                for category in CATEGORIES.keys():
                    if category == "Uncategorized":
                        continue
                    generate_verbose_section(category, ecosystem_data, outfile)

def main() -> None:
    """Generate a report comparing specific TOML files.
    
    Usage: python -m report.report_generator [ecosystem1] [ecosystem2] ... [ecosystem6]
    Example: python -m report.report_generator ethereum solana polkadot
    """
    import sys
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

    # Get ecosystems from command line arguments
    ecosystems = sys.argv[1:7] if len(sys.argv) > 1 else []
    
    try:
        if ecosystems:
            # Get only specified ecosystem TOML files
            toml_files = []
            for eco in ecosystems:
                file_path = os.path.join(input_dir, f"{eco}.toml")
                if os.path.exists(file_path):
                    toml_files.append(file_path)
                else:
                    logging.warning(f"Ecosystem file not found: {eco}.toml")
        else:
            # If no arguments provided, get all TOML files
            toml_files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.endswith('.toml')]
    except OSError as e:
        logging.error("Error accessing the input folder: %s", e)
        return

    if not toml_files:
        logging.error("No .toml files found to process.")
        return

    # Create a more descriptive filename when specific ecosystems are compared
    if ecosystems:
        eco_names = "-".join(ecosystems)
        output_filename = f"comparison-{eco_names}{'-verbose' if verbose else ''}-{current_date}.md"
    else:
        output_filename = f"report{'-verbose' if verbose else ''}-{current_date}.md"
    
    output_path = os.path.join(output_dir, output_filename)
    
    generate_master_report(toml_files, output_path, verbose=verbose)
    logging.info("Generated report -> %s", output_filename)
    logging.info("Report has been saved in the 'output' folder.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    main()

"""Module for generating reports from TOML files containing repository information."""

from datetime import datetime
from typing import List, Dict, Tuple
import os
import logging
from report.constants import COMPILED_CATEGORIES, CATEGORIES
from .utils import categorize_repos, extract_repo_info
from collections import defaultdict
import re
from .verbose_generator import generate_verbose_section

def process_ecosystem(content: str) -> Tuple[int, List[str], set, Dict, Dict, int, Dict]:
    """Process a single ecosystem's TOML content and return analysis data."""
    total_repos, repos, categories, _, _, _ = extract_repo_info(content)
    
    # Categorize repositories
    categorized_repos, pattern_matches, pattern_counts = categorize_repos(repos, CATEGORIES)
    
    category_stats = {}
    total_categorized = 0

    # Calculate statistics for each category
    for category in COMPILED_CATEGORIES:
        category_repos = categorized_repos.get(category, [])
        count = len(category_repos)
        percentage = (count / total_repos * 100) if total_repos > 0 else 0
        category_stats[category] = {
            'count': count,
            'percentage': f"{percentage:.2f}%",
            'pattern_matches': pattern_matches.get(category, {}),
            'pattern_counts': pattern_counts.get(category, {})
        }
        total_categorized += count

    return total_repos, repos, categories, pattern_matches, category_stats, total_categorized, pattern_matches

def generate_master_report(toml_files: List[str], output_file: str, verbose: bool = False) -> None:
    """Generate a master report from multiple TOML files."""
    ecosystem_data = []
    total_repos = 0

    with open(output_file, 'w', encoding='utf-8') as f:
        # Report Header with consolidated information
        f.write("# Ecosystem Analysis Report\n\n")
        
        # Executive Summary
        f.write("| Metric | Value |\n")
        f.write("|--------|-------|\n")
        f.write(f"| Report Generated | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} |\n")
        f.write(f"| Ecosystems Analyzed | {len(toml_files)} |\n")
        f.write(f"| Files Processed | {len(toml_files)} |\n")
        f.write(f"| Analysis Type | {'Verbose' if verbose else 'Standard'} |\n\n")

        # Source Files section with categories
        f.write("## Source Files\n\n")
        
        # Create header with all categories plus Uncategorized
        categories = list(COMPILED_CATEGORIES.keys())
        header = ["Ecosystem", "Repository Count"]
        header.extend(categories)
        header.append("Uncategorized")
        
        f.write("| " + " | ".join(header) + " |\n")
        f.write("|" + "|".join(["---" for _ in header]) + "|\n")

        # Process each ecosystem
        for input_file in toml_files:
            ecosystem_name = os.path.splitext(os.path.basename(input_file))[0]
            with open(input_file, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Process ecosystem data
            total_repos_eco, repos, _, _, category_stats, _, _ = process_ecosystem(content)
            total_repos += total_repos_eco
            
            # Create row with ecosystem data and category percentages
            row = [ecosystem_name, f"{total_repos_eco:,}"]
            
            # Calculate total categorized percentage
            total_categorized_percent = sum(
                float(stats.get('percentage', '0.00%').rstrip('%'))
                for stats in category_stats.values()
            )
            
            # Add category percentages
            for category in categories:
                percentage = category_stats.get(category, {}).get('percentage', '0.00%')
                row.append(percentage)
            
            # Add Uncategorized percentage
            uncategorized_percent = max(0, 100 - total_categorized_percent)
            row.append(f"{uncategorized_percent:.2f}%")
            
            # Add to table
            f.write(f"| {' | '.join(row)} |\n")
            
            ecosystem_data.append({
                'name': ecosystem_name,
                'total_repos': total_repos_eco,
                'categories': category_stats
            })
        
        f.write(f"\n**Total Repositories: {total_repos:,}**\n\n")

        if verbose:
            f.write("\n## Detailed Pattern Analysis\n\n")
            for category in COMPILED_CATEGORIES:
                generate_verbose_section(f, category, ecosystem_data, CATEGORIES[category])

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

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
    total_repos, repos, categories, _, _, _ = extract_repo_info(content)
    
    # Categorize repositories
    categorized_repos, pattern_matches, pattern_counts = categorize_repos(repos, CATEGORIES)
    
    category_stats = {}
    total_categorized = 0
    
    # Group categories by primary category (assuming format "PRIMARY/SUB")
    primary_categories = defaultdict(list)
    for category in COMPILED_CATEGORIES:
        if '/' in category:
            primary, _ = category.split('/', 1)
            primary_categories[primary].append(category)
        else:
            primary_categories[category].append(category)

    # Calculate statistics for each category
    for category in COMPILED_CATEGORIES:
        category_repos = categorized_repos.get(category, [])
        count = len(category_repos)
        percentage = (count / total_repos * 100) if total_repos > 0 else 0
        
        # Calculate primary category totals
        primary = category.split('/')[0] if '/' in category else category
        
        category_stats[category] = {
            'count': count,
            'percentage': f"{percentage:.2f}%",
            'pattern_matches': pattern_matches.get(category, {}),
            'pattern_counts': pattern_counts.get(category, {}),
            'primary_category': primary
        }
        total_categorized += count

    # Add cumulative stats for primary categories
    for primary, subcategories in primary_categories.items():
        cumulative_count = sum(category_stats[sub]['count'] for sub in subcategories)
        cumulative_percentage = (cumulative_count / total_repos * 100) if total_repos > 0 else 0
        category_stats[f"{primary}_cumulative"] = {
            'count': cumulative_count,
            'percentage': f"{cumulative_percentage:.2f}%"
        }

    return total_repos, repos, categories, pattern_matches, category_stats, total_categorized, pattern_counts

def generate_master_report(toml_files: List[str], output_file: str, verbose: bool = False) -> None:
    ecosystem_data = []
    
    # Process all ecosystems first
    for input_file in toml_files:
        ecosystem_name = os.path.basename(input_file).replace('.toml', '')
        with open(input_file, 'r', encoding='utf-8') as infile:
            content = infile.read()
            
        total_repos, repos, _, pattern_matches, category_stats, total_categorized, _ = process_ecosystem(content)
        
        ecosystem_data.append({
            'name': ecosystem_name,
            'total_repos': total_repos,
            'categories': category_stats,
            'pattern_matches': pattern_matches
        })
    
    with open(output_file, 'w', encoding='utf-8') as outfile:
        # Summary table
        outfile.write("# Ecosystem Analysis Report\n\n")
        
        # Create vertical summary table
        ecosystems = [data['name'] for data in ecosystem_data]
        outfile.write("| Category | " + " | ".join(ecosystems) + " |\n")
        outfile.write("|----------" + "|---------" * len(ecosystems) + "|\n")
        
        # Add Repository Count row
        repo_counts = [f"{data['total_repos']:,}" for data in ecosystem_data]
        outfile.write(f"| Repository Count | {' | '.join(repo_counts)} |\n")
        
        # Add rows for each category with percentages
        for category in COMPILED_CATEGORIES:
            row = [category]
            
            # Calculate total repos in this category across all ecosystems
            category_counts = []
            for eco_data in ecosystem_data:
                stats = eco_data['categories'].get(category, {})
                count = stats.get('count', 0)
                category_counts.append(count)
            total_category_repos = sum(category_counts)
            
            # Calculate percentages for each ecosystem
            for count, eco_data in zip(category_counts, ecosystem_data):
                stats = eco_data['categories'].get(category, {})
                within_chain_pct = stats.get('percentage', '0.00%')
                share_of_category = f"{(count / total_category_repos * 100):.2f}%" if total_category_repos > 0 else "0.00%"
                row.append(f"{within_chain_pct} ({share_of_category})")
                
            outfile.write(f"| {' | '.join(row)} |\n")
        
        if verbose:
            outfile.write("\n## Detailed Pattern Analysis\n\n")
            for primary in set(cat.split('/')[0] for cat in COMPILED_CATEGORIES):
                generate_verbose_section(outfile, primary, ecosystem_data)

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

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
    total_all_repos = 0
    unique_accounts = set()
    individual_accounts = set()
    org_accounts = set()
    
    # Process all ecosystems first
    for input_file in toml_files:
        ecosystem_name = os.path.basename(input_file).replace('.toml', '')
        with open(input_file, 'r', encoding='utf-8') as infile:
            content = infile.read()
            
        total_repos, repos, _, pattern_matches, category_stats, total_categorized, _ = process_ecosystem(content)
        total_all_repos += total_repos
        
        # Extract GitHub usernames/organizations from repo URLs
        for repo in repos:
            account = repo.split('/')[-2]  # Gets the account name from github.com/account/repo
            unique_accounts.add(account)
            # Simple heuristic: accounts with uppercase letters are likely organizations
            if any(c.isupper() for c in account):
                org_accounts.add(account)
            else:
                individual_accounts.add(account)
        
        ecosystem_data.append({
            'name': ecosystem_name,
            'total_repos': total_repos,
            'categories': category_stats,
            'pattern_matches': pattern_matches
        })
    
    with open(output_file, 'w', encoding='utf-8') as outfile:
        outfile.write("# Ecosystem Analysis Report\n\n")
        
        # Add overall statistics
        outfile.write("## Overall Statistics\n")
        outfile.write("| Metric | Count |\n")
        outfile.write("|--------|-------|\n")
        outfile.write(f"| Total repositories | {total_all_repos:,} |\n")
        outfile.write(f"| Unique GitHub accounts | {len(unique_accounts):,} |\n")
        outfile.write(f"| Estimated individual accounts | {len(individual_accounts):,} |\n")
        outfile.write(f"| Estimated organization/team accounts | {len(org_accounts):,} |\n\n")
        
        # Create ecosystem comparison table
        outfile.write("## Ecosystem Comparison Categories\n\n")
        outfile.write("| Category | Description |\n")
        outfile.write("|----------|-------------|\n")
        outfile.write("| DeFi & Financial | Decentralized finance protocols, financial instruments, and related tools |\n")
        outfile.write("| NFTs & Digital Assets | NFT marketplaces, tools, and digital collectibles |\n")
        outfile.write("| Infrastructure & Tools | Developer tools, SDKs, and blockchain infrastructure |\n")
        outfile.write("| Identity & Authentication | Identity management, authentication, and verification systems |\n")
        outfile.write("| Data & Analytics | Data indexing, analytics tools, and visualization platforms |\n")
        outfile.write("| Gaming & Entertainment | Blockchain games, metaverse projects, and entertainment platforms |\n")
        outfile.write("| Social | Social networks, communication platforms, and community tools |\n")
        outfile.write("| Security & Privacy | Security tools, auditing platforms, and privacy solutions |\n")
        outfile.write("| Uncategorized | Repositories that don't match any defined category patterns |\n\n")
        
        # Add Uncategorized Repositories section after main comparisons
        total_uncategorized = sum(len(data.get('categorized_repos', {}).get('Uncategorized', [])) 
                                 for data in ecosystem_data)
        
        outfile.write("\n## Uncategorized Repositories\n\n")
        outfile.write(f"Total uncategorized repositories across all ecosystems: **{total_uncategorized}**\n\n")
        
        outfile.write("<details>\n")
        outfile.write("<summary>Click to expand uncategorized repository analysis</summary>\n\n")
        
        # Add analysis text
        outfile.write("The following ecosystems contain repositories that don't match our defined category patterns. ")
        outfile.write("These might represent emerging trends, unique use cases, or repositories that need manual categorization.\n\n")
        
        # Create table of uncategorized repos by ecosystem
        outfile.write("| Ecosystem | Uncategorized Repositories | Percentage of Total |\n")
        outfile.write("|-----------|---------------------------|--------------------|\n")
        
        for eco_data in ecosystem_data:
            eco_name = eco_data['name']
            total_repos = eco_data['total_repos']
            uncategorized = len(eco_data.get('categorized_repos', {}).get('Uncategorized', []))
            percentage = (uncategorized / total_repos * 100) if total_repos > 0 else 0
            
            outfile.write(f"| {eco_name} | {uncategorized} | {percentage:.1f}% |\n")
        
        outfile.write("\n</details>\n\n")
        
        # Continue with verbose section if enabled
        if verbose:
            outfile.write("\n## Detailed Pattern Analysis\n\n")
            # Process all regular categories
            for primary in set(cat.split('/')[0] for cat in COMPILED_CATEGORIES):
                generate_verbose_section(outfile, primary, ecosystem_data)
            # Add Uncategorized section at the end
            generate_verbose_section(outfile, "Uncategorized", ecosystem_data)

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

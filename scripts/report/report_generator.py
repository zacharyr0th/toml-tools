"""Module for generating reports from TOML files containing repository information."""

import os
import re
import logging
from datetime import datetime
from typing import List, Dict, Tuple, Optional
from collections import defaultdict
import argparse

from .categories import CategoryRegistry
from .utils import (
    extract_repo_info,
    categorize_repos,
    calculate_category_stats,
    REPO_PATTERN,
    convert_categories_to_dict
)

# Initialize category registry
registry = CategoryRegistry()
CATEGORIES = convert_categories_to_dict(registry)

def filter_repos_by_keyword(repos: List[str], keyword: str) -> List[str]:
    """Filter repositories by keyword."""
    if not keyword:
        return repos
    keyword = keyword.lower()
    return [repo for repo in repos if keyword in repo.lower()]

def process_ecosystem(
    content: str,
    keyword: Optional[str] = None,
    category_filter: Optional[str] = None
) -> Tuple[int, List[str], Dict, Dict, Dict, int, Dict]:
    """Process a single ecosystem's TOML content with filtering."""
    repos, github_accounts, missing_repos, org_accounts, individual_accounts = extract_repo_info(content)
    
    # Apply keyword filter if specified
    if keyword:
        repos = filter_repos_by_keyword(repos, keyword)
        if not repos:
            return 0, [], {}, {}, {}, 0, {}
    
    total_repos = len(repos)
    
    # Categorize repositories
    categorized_repos = categorize_repos(repos)
    
    # Apply category filter if specified
    if category_filter:
        filtered_repos = categorized_repos.get(category_filter, [])
        categorized_repos = {category_filter: filtered_repos} if filtered_repos else {}
    
    total_categorized = sum(len(repos) for category, repos in categorized_repos.items() if category != "Uncategorized")
    
    # Calculate category statistics
    category_stats = calculate_category_stats(categorized_repos, total_repos)
    
    # Prepare ecosystem data
    eco_data = {
        'total_repos': total_repos,
        'repos': repos,
        'github_accounts': github_accounts,
        'missing_repos': missing_repos,
        'org_accounts': org_accounts,
        'individual_accounts': individual_accounts,
        'categorized_repos': categorized_repos,
        'category_stats': category_stats,
        'total_categorized': total_categorized
    }
    
    return total_repos, repos, categorized_repos, category_stats, total_categorized, eco_data

def generate_master_report(
    toml_files: List[str],
    output_file: str,
    verbose: bool = False,
    keyword: Optional[str] = None,
    category_filter: Optional[str] = None
) -> None:
    """Generate the master report with search and filter options."""
    ecosystem_data = []
    
    # Process all ecosystems first
    for input_file in toml_files:
        ecosystem_name = os.path.basename(input_file).replace('.toml', '')
        
        with open(input_file, 'r', encoding='utf-8') as infile:
            content = infile.read()
            
        total_repos, repos, categorized_repos, category_stats, total_categorized, eco_data = process_ecosystem(
            content,
            keyword=keyword,
            category_filter=category_filter
        )
        
        if total_repos > 0:  # Only include ecosystems with matching repos
            eco_data['name'] = ecosystem_name
            ecosystem_data.append(eco_data)
    
    # Write report after processing all ecosystems
    with open(output_file, 'w', encoding='utf-8') as outfile:
        # Add JavaScript for sorting
        outfile.write("""
<script>
function sortTable(tableId, n) {
    var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
    table = document.getElementById(tableId);
    switching = true;
    dir = "asc";
    
    while (switching) {
        switching = false;
        rows = table.rows;
        
        for (i = 1; i < (rows.length - 1); i++) {
            shouldSwitch = false;
            x = rows[i].getElementsByTagName("TD")[n];
            y = rows[i + 1].getElementsByTagName("TD")[n];
            
            if (dir == "asc") {
                if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
                    shouldSwitch = true;
                    break;
                }
            } else if (dir == "desc") {
                if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
                    shouldSwitch = true;
                    break;
                }
            }
        }
        
        if (shouldSwitch) {
            rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
            switching = true;
            switchcount++;
        } else {
            if (switchcount == 0 && dir == "asc") {
                dir = "desc";
                switching = true;
            }
        }
    }
}
</script>
<style>
th { cursor: pointer; }
th:hover { background-color: #f5f5f5; }
</style>
""")

        outfile.write("# Repository Analysis Report\n\n")
        
        # Write search parameters if any
        if keyword or category_filter:
            outfile.write("## Search Parameters\n")
            outfile.write("| Parameter | Value |\n")
            outfile.write("|-----------|-------|\n")
            if keyword:
                outfile.write(f"| Keyword | `{keyword}` |\n")
            if category_filter:
                outfile.write(f"| Category Filter | {category_filter} |\n")
            outfile.write("\n")
        
        # Write overall statistics
        total_all_repos = sum(eco['total_repos'] for eco in ecosystem_data)
        outfile.write("## Overall Statistics\n")
        outfile.write("| Metric | Count |\n")
        outfile.write("|--------|-------|\n")
        outfile.write(f"| Total repositories | {total_all_repos:,} |\n")
        outfile.write(f"| Ecosystems analyzed | {len(ecosystem_data)} |\n")
        
        # Write category statistics
        if ecosystem_data:
            outfile.write("\n## Category Statistics\n")
            outfile.write('<table id="categoryStats">\n')
            outfile.write('<tr>')
            outfile.write('<th onclick="sortTable(\'categoryStats\', 0)">Category ▼</th>')
            outfile.write('<th onclick="sortTable(\'categoryStats\', 1)">Repository Count ▼</th>')
            outfile.write('<th onclick="sortTable(\'categoryStats\', 2)">Percentage ▼</th>')
            outfile.write('</tr>\n')
            
            # Aggregate category stats across all ecosystems
            total_by_category = defaultdict(int)
            for eco in ecosystem_data:
                for category, stats in eco['category_stats'].items():
                    total_by_category[category] += stats['count']
            
            # Sort categories by count (excluding Uncategorized)
            sorted_categories = sorted(
                [(k, v) for k, v in total_by_category.items() if k != "Uncategorized"],
                key=lambda x: x[1],
                reverse=True
            )
            
            # Write sorted categories
            for category, count in sorted_categories:
                percentage = (count / total_all_repos * 100) if total_all_repos > 0 else 0
                outfile.write(f"<tr><td>{category}</td><td>{count:,}</td><td>{percentage:.2f}%</td></tr>\n")
            
            # Write uncategorized at the end
            if "Uncategorized" in total_by_category:
                count = total_by_category["Uncategorized"]
                percentage = (count / total_all_repos * 100) if total_all_repos > 0 else 0
                outfile.write(f"<tr><td>Uncategorized</td><td>{count:,}</td><td>{percentage:.2f}%</td></tr>\n")
            
            outfile.write("</table>\n\n")
        
        # Write ecosystem breakdown
        outfile.write("\n## Ecosystem Breakdown\n")
        for eco in ecosystem_data:
            # Write categorized repositories with collapsible sections
            for category, repos in sorted(eco['categorized_repos'].items()):
                if repos:  # Only show categories with repositories
                    table_id = f"table_{category.lower().replace(' ', '_')}"
                    outfile.write(f"<details>\n<summary>{category} ({len(repos)} repos)</summary>\n\n")
                    
                    # Create table header with sortable columns
                    outfile.write(f'<table id="{table_id}">\n')
                    outfile.write('<tr>')
                    outfile.write(f'<th onclick="sortTable(\'{table_id}\', 0)"># ▼</th>')
                    outfile.write(f'<th onclick="sortTable(\'{table_id}\', 1)">Repository ▼</th>')
                    outfile.write(f'<th onclick="sortTable(\'{table_id}\', 2)">Owner ▼</th>')
                    outfile.write(f'<th onclick="sortTable(\'{table_id}\', 3)">Type ▼</th>')
                    outfile.write('</tr>\n')
                    
                    # Sort repositories by owner/name for better readability
                    sorted_repos = sorted(repos, key=lambda x: x.lower())
                    
                    # Write repository entries
                    for idx, repo in enumerate(sorted_repos, 1):
                        parts = repo.split('/')
                        owner = parts[-2]
                        repo_name = parts[-1]
                        account_type = "Organization" if owner in eco['org_accounts'] else "Individual"
                        
                        outfile.write(
                            f"<tr><td>{idx}</td><td><a href='{repo}'>{repo_name}</a></td>"
                            f"<td><a href='https://github.com/{owner}'>{owner}</a></td>"
                            f"<td>{account_type}</td></tr>\n"
                        )
                    
                    outfile.write("</table>\n\n")
                    outfile.write("</details>\n\n")

def main() -> None:
    """Generate a report comparing specific TOML files."""
    parser = argparse.ArgumentParser(description='Generate repository analysis report.')
    parser.add_argument('ecosystems', nargs='*', help='Names of ecosystem TOML files to analyze.')
    parser.add_argument('--verbose', action='store_true', help='Generate detailed pattern analysis')
    parser.add_argument('--keyword', help='Filter repositories by keyword')
    parser.add_argument('--category-filter', help='Filter repositories by category')
    args = parser.parse_args()
    
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
    ecosystems = args.ecosystems if args.ecosystems else []
    
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
        output_filename = f"comparison-{eco_names}{'-verbose' if args.verbose else ''}-{current_date}.md"
    else:
        output_filename = f"report{'-verbose' if args.verbose else ''}-{current_date}.md"
    
    output_path = os.path.join(output_dir, output_filename)
    
    generate_master_report(toml_files, output_path, verbose=args.verbose, keyword=args.keyword, category_filter=args.category_filter)
    logging.info("Generated report -> %s", output_filename)
    logging.info("Report has been saved in the 'output' folder.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    main()

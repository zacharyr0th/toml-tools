"""Module for generating reports from TOML files containing repository information."""

from datetime import datetime
import re
from typing import List
from collections import defaultdict
import os
import sys
import logging

def categorize_repos(repos, categories):
    """Categorize repositories based on predefined patterns."""
    categorized = defaultdict(list)
    for repo in repos:
        for category, patterns in categories.items():
            if any(pattern.search(repo['url']) for pattern in patterns):
                categorized[category].append(repo['url'])
                break  # Stop after first match to avoid double-counting
        else:
            categorized["Uncategorized"].append(repo['url'])
    return categorized

def extract_repo_info(content):
    """Extract repository information from the given content."""
    repos = []
    github_accounts = set()
    missing_repos = 0
    org_accounts = set()
    individual_accounts = set()

    repo_pattern = re.compile(
        r'\[\[repo\]\]\s*url\s*=\s*"(https://github\.com/([^/]+)/([^/"\s]+))"'
        r'(?:\s*missing\s*=\s*(true|false))?',
        re.IGNORECASE
    )

    for match in repo_pattern.finditer(content):
        url, account, _, missing = match.groups()
        if missing and missing.lower() == 'true':
            missing_repos += 1
        else:
            repos.append({'url': url, 'account': account})
            github_accounts.add(account)
            if re.search(r'[A-Z]', account) or len(account) > 15:
                org_accounts.add(account)
            else:
                individual_accounts.add(account)

    return repos, github_accounts, missing_repos, org_accounts, individual_accounts

def organize_toml_content(content):
    """Organize TOML content by sorting sections and their contents."""
    # Parse TOML content manually
    sections = {}
    current_section = None
    for line in content.split('\n'):
        line = line.strip()
        if line.startswith('[') and line.endswith(']'):
            current_section = line[1:-1]
            sections[current_section] = []
        elif current_section and '=' in line:
            sections[current_section].append(line)

    # Sort sections and their contents
    organized_data = {k: sorted(v, key=lambda x: x.lower()) for k, v in sorted(sections.items())}

    # Convert back to TOML format
    organized_content = []
    for section, lines in organized_data.items():
        organized_content.append(f'[{section}]')
        organized_content.extend(lines)
        organized_content.append('')

    return '\n'.join(organized_content)

def generate_master_report(toml_files: List[str], output_file: str) -> None:
    """Generate a master report from multiple TOML files."""
    categories = {
        "DeFi": [
            r"\b(?:de)?fi(?:nance)?\b", r"\bswap(?:ping)?\b", r"\bexchange\b", r"\blend(?:ing)?\b",
            r"\bborrow(?:ing)?\b", r"\byield\b", r"\bamm\b", r"\bliquidity\b", r"\bstaking\b", r"\bvault\b",
            r"\bsynthetic(?:s)?\b", r"\bderivative(?:s)?\b", r"\bmoney\s*market\b", r"\basset\s*management\b",
            r"\bdex\b", r"\bdecentralized\s*exchange\b", r"\baave\b", r"\bcompound\b", r"\buniswap\b",
            r"\bsushiswap\b", r"\bcurve\b", r"\bbalancer\b"
        ],
        "Gaming": [
            r"\bgam(?:e|ing)\b", r"\bplay.*earn\b", r"\bvirtual\s*world\b", r"\bavatar\b", r"\besports?\b",
            r"\baxie\b", r"\bdecentraland\b", r"\bsandbox\b"
        ],
        "Social": [
            r"\bsocial\b", r"\bcommunity\b", r"\bmessag(?:e|ing)\b", r"\bchat\b", r"\bforum\b",
            r"\bnetwork(?:ing)?\b", r"\bcontent\b", r"\bmedia\b", r"\bblog\b", r"\bmicroblog(?:ging)?\b",
            r"\bprofile\b", r"\bsteemit\b", r"\bdtube\b", r"\bpeepeth\b"
        ],
        "Infrastructure": [
            r"\binfra(?:structure)?\b", r"\bprotocol\b", r"\bchain\b", r"\bnetwork\b", r"\boracle\b",
            r"\bbridge\b", r"\bscaling\b", r"\blayer[_\s]?2\b", r"\bl2\b", r"\binteroperability\b",
            r"\bcross[-\s]chain\b", r"\bconsensus\b", r"\bnode\b", r"\bvalidator\b", r"\bpolkadot\b",
            r"\bkosmos\b", r"\bchainlink\b", r"\boptimism\b", r"\barbitrum\b", r"\banalytics?\b", r"\bdata\b",
            r"\bmetrics?\b", r"\bdashboard\b", r"\bvisualization\b", r"\breporting\b", r"\binsights?\b",
            r"\bintelligence\b", r"\bmonitoring\b", r"\btracking\b", r"\bdune\s*analytics\b", r"\bnansen\b",
            r"\bglassnode\b", r"\bidentity\b", r"\bdid\b", r"\bdecentralized\s*id\b", r"\bssi\b",
            r"\bself[-\s]sovereign\b", r"\bkyc\b", r"\bknow\s*your\s*customer\b", r"\bauthentication\b",
            r"\bcivic\b", r"\buport\b", r"\bselfkey\b", r"\btoken(?:iz(?:e|ation))?\b", r"\basset[-\s]backed\b",
            r"\bsecurity\s*token\b", r"\butility\s*token\b", r"\berc[-\s]?20\b", r"\berc[-\s]?721\b", r"\berc[-\s]?1155\b", 
            r"\bdev\s*tools?\b", r"\bsdk\b", r"\bapi\b", r"\blibrary\b", r"\bframework\b", r"\btesting\b", 
            r"\bdeployment\b", r"\bide\b", r"\bcompiler\b", r"\bweb3[._]?js\b", r"\bethers[._]?js\b", r"\btruffle\b", 
            r"\bhardhat\b", r"\bganache\b", r"\bwallet\b", r"\bcustody\b", r"\bkey\s*management\b", r"\bmulti[-\s]sig\b",
            r"\bhardware\s*wallet\b", r"\bmetamask\b", r"\btrezor\b", r"\bledger\b", r"\bprivacy\b",
            r"\bencrypt(?:ion)?\b", r"\banonymous\b", r"\bconfidential\b", r"\bzero[-\s]knowledge\b", r"\bzk\b",
            r"\bmixer\b", r"\btumbler\b", r"\bsecure\s*messaging\b", r"\bmonero\b", r"\bzcash\b",
            r"\btornado\s*cash\b", r"\bsmart\s*contract\b", r"\bsolidity\b", r"\bvyper\b", r"\bmove\b",
            r"\brust\b", r"\bink!\b", r"\bopenzeppelin\b"
        ],
        "NFTs": [
            r"\bnft\b", r"\bnon[-\s]fungible\b", r"\bcollectible\b", r"\bmetaverse\b",
            r"\bmarketplace\b", r"\bauction\b", r"\be[-\s]commerce\b", r"\bbuy\b", r"\bsell\b", r"\btrade\b",
            r"\bopensea\b", r"\brarible\b", r"\bfoundation\b", r"\bcryptokitties\b"
        ]
    }
    categories = {k: [re.compile(v, re.IGNORECASE) for v in vs] for k, vs in categories.items()}

    ecosystem_data = []

    for input_file in toml_files:
        with open(input_file, 'r', encoding='utf-8') as file:
            content = file.read()

        repos, github_accounts, missing_repos, org_accounts, individual_accounts = extract_repo_info(content)
        
        ecosystem_name = os.path.splitext(os.path.basename(input_file))[0]
        
        sub_ecosystem_repos = categorize_repos(repos, categories)
        total_repos = len(repos) + missing_repos

        # Calculate counts and percentages for each category
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
            'valid_repos': len(repos),
            'missing_repos': missing_repos,
            'github_accounts': len(github_accounts),
            'individual_accounts': len(individual_accounts),
            'org_accounts': len(org_accounts),
            'categories': category_stats
        })  

    # Sort ecosystem_data by total_repos in descending order
    ecosystem_data.sort(key=lambda x: x['total_repos'], reverse=True)

    with open(output_file, 'w', encoding='utf-8') as master_file:
        # Write overall summary
        total_repos = sum(eco['total_repos'] for eco in ecosystem_data)
        total_github_accounts = sum(eco['github_accounts'] for eco in ecosystem_data)
        master_file.write("# Ecosystem Analysis Report\n\n")
        master_file.write(f"- Total Repositories Across Top Ecosystems: {total_repos:,}\n")
        master_file.write(f"- Gross Count of Users Across Top Ecosystems: {total_github_accounts:,}\n\n")

        # Write summary table header
        master_file.write("| Ecosystem | Total Repos | Valid Repos | Missing Repos | GitHub Accounts | Individual Accounts | Org/Team Accounts | DeFi | Gaming | Social | Infrastructure | NFTs | Uncategorized |\n")
        master_file.write("|-----------|-------------|-------------|---------------|-----------------|---------------------|-------------------|------|--------|--------|----------------|------|---------------|\n")
        
        # Add summary table rows
        for ecosystem in ecosystem_data:
            master_file.write(f"| {ecosystem['name']} | ")
            master_file.write(f"{ecosystem['total_repos']:,} | ")
            master_file.write(f"{ecosystem['valid_repos']:,} | ")
            master_file.write(f"{ecosystem['missing_repos']:,} | ")
            master_file.write(f"{ecosystem['github_accounts']:,} | ")
            master_file.write(f"{ecosystem['individual_accounts']:,} | ")
            master_file.write(f"{ecosystem['org_accounts']:,} | ")
            for category in ['DeFi', 'Gaming', 'Social', 'Infrastructure', 'NFTs', 'Uncategorized']:
                master_file.write(f"{ecosystem['categories'].get(category, {'percentage': '0.00%'})['percentage']} | ")
            master_file.write("\n")

        # Add detailed category breakdown for each ecosystem
        master_file.write("\n## Detailed Category Breakdown\n\n")
        for ecosystem in ecosystem_data:
            master_file.write(f"### {ecosystem['name']}\n\n")
            master_file.write(f"- Total Repositories in {ecosystem['name']}: {ecosystem['total_repos']:,}\n")
            master_file.write(f"- Affiliated GitHub Accounts: {ecosystem['github_accounts']:,}\n\n")
            master_file.write("| Category | Count | Percentage |\n")
            master_file.write("|----------|-------|------------|\n")
            for category in ['DeFi', 'Gaming', 'Social', 'Infrastructure', 'NFTs', 'Uncategorized']:
                stats = ecosystem['categories'].get(category, {'count': 0, 'percentage': '0.00%'})
                master_file.write(f"| {category} | {stats['count']:,} | {stats['percentage']} |\n")
            master_file.write("\n")

def generate_report(input_file: str, output_file: str) -> None:
    """
    Generate a report for a single TOML file.

    Args:
        input_file (str): Path to the input TOML file.
        output_file (str): Path to the output Markdown file.
    """
    generate_master_report([input_file], output_file)

def main() -> None:
    """Generate a single report for all TOML files in the input folder."""
    current_date = datetime.now().strftime("%m-%d-%y")
    os.makedirs('output', exist_ok=True)

    input_folder = 'input'
    toml_files = [os.path.join(input_folder, f) for f in os.listdir(input_folder) if f.endswith('.toml')]

    if not toml_files:
        logging.error("No .toml files found in the input folder.")
        sys.exit(1)

    output_filename = f"report-{current_date}.md"
    output_path = os.path.join('output', output_filename)
    
    generate_master_report(toml_files, output_path)
    logging.info("Generated report for all TOML files -> %s", output_filename)

    logging.info("Report has been generated for all TOML files and saved in the 'output' folder.")

if __name__ == "__main__":
    main()

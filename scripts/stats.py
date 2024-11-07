"""Module for generating statistics from TOML repository files."""

import re
import os
import sys
import argparse
from datetime import datetime
import logging
from collections import defaultdict
from typing import Dict, Set, List, Tuple

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def extract_repo_info(content: str) -> Tuple[
    List[Dict[str, str]],
    Set[str],
    int,
    Set[str],
    Set[str]
]:
    """
    Extract repository information from the given content.

    Args:
        content (str): The content to parse.

    Returns:
        Tuple containing repos, github_accounts, missing_repos, org_accounts, and individual_accounts.
    """
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
        url, account, repo_name, missing = match.groups()
        if missing and missing.lower() == 'true':
            missing_repos += 1
        else:
            repos.append({'url': url, 'account': account, 'name': repo_name})
            github_accounts.add(account)
            if any([
                account.endswith(('inc', 'llc', 'corp', 'ltd', 'foundation', 'org')),
                '-' in account,
                account.isupper(),
                len(account) > 15
            ]):
                org_accounts.add(account)
            else:
                individual_accounts.add(account)

    return repos, github_accounts, missing_repos, org_accounts, individual_accounts

def categorize_repos(repos: List[Dict[str, str]], categories: Dict[str, List[re.Pattern]]) -> Dict[str, List[str]]:
    """
    Categorize repositories based on predefined patterns.

    Args:
        repos: List of repository dictionaries.
        categories: Dictionary of category names and their associated regex patterns.

    Returns:
        Dictionary of categorized repository URLs.
    """
    sub_ecosystem_repos = defaultdict(list)
    for repo in repos:
        repo_url = repo['url']
        for eco, patterns in categories.items():
            if any(pattern.search(repo_url) for pattern in patterns):
                sub_ecosystem_repos[eco].append(repo_url)
                break
        else:
            sub_ecosystem_repos["Unrelated"].append(repo_url)
    return sub_ecosystem_repos

def extract_contributors(content: str) -> Tuple[Set[str], Set[str]]:
    """
    Extract team GitHub accounts and individual contributors from the content.

    Args:
        content (str): The content to parse.

    Returns:
        Tuple containing sets of team GitHub accounts and individual contributors.
    """
    team_github_accounts = set(re.findall(r'team_github\s*=\s*"(.*?)"', content))
    individual_contributors_match = re.search(r'individual_contributors\s*=\s*\[(.*?)\]', content, re.DOTALL)
    individual_contributors = set(
        contributor.strip().strip('"') for contributor in individual_contributors_match.group(1).split(',')
        if contributor.strip()
    ) if individual_contributors_match else set()
    return team_github_accounts, individual_contributors

def generate_report(
    repos: List[Dict[str, str]],
    github_accounts: Set[str],
    missing_repos: int,
    categories: Dict[str, List[re.Pattern]],
    org_accounts: Set[str],
    individual_accounts: Set[str]
) -> List[str]:
    """
    Generate a detailed report of the ecosystem analysis.

    Args:
        repos: List of repository dictionaries.
        github_accounts: Set of unique GitHub accounts.
        missing_repos: Number of missing repositories.
        categories: Dictionary of category names and their regex patterns.
        org_accounts: Set of organization/team accounts.
        individual_accounts: Set of individual accounts.

    Returns:
        List of strings containing the report content.
    """
    report = [
        "Ecosystem Analysis Report",
        f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "1. Overview",
        f"   Total repositories: {len(repos) + missing_repos}",
        f"   Valid repositories: {len(repos)}",
        f"   Missing repositories: {missing_repos}",
        f"   Unique GitHub accounts: {len(github_accounts)}",
        f"   Estimated individual accounts: {len(individual_accounts)}",
        f"   Estimated organization/team accounts: {len(org_accounts)}",
        "",
        "2. Ecosystem Analysis",
    ]

    sub_ecosystem_repos = categorize_repos(repos, categories)
    total_repos = len(repos)

    for eco, eco_repos in sub_ecosystem_repos.items():
        if eco != "Unrelated":
            count = len(eco_repos)
            percentage = (count / total_repos) * 100
            report.append(f"   - {eco}: {count} repositories ({percentage:.2f}% of total)")

    unrelated_count = len(sub_ecosystem_repos["Unrelated"])
    unrelated_percentage = (unrelated_count / total_repos) * 100
    report.append(f"   - Unrelated: {unrelated_count} repositories ({unrelated_percentage:.2f}% of total)")
    report.append("")

    report.append("3. Account Analysis")
    account_repos = defaultdict(list)
    for repo in repos:
        account_repos[repo['account']].append(repo['url'])

    sorted_accounts = sorted(account_repos.items(), key=lambda x: len(x[1]), reverse=True)

    for account, repo_list in sorted_accounts:
        if len(repo_list) >= 5:  
            account_type = "organization/team" if account in org_accounts else "individual"
            report.extend([
                f"   {account} ({account_type}):",
                f"   - Number of repositories: {len(repo_list)}",
                *[f"   - {repo_url}" for repo_url in repo_list],
                ""
            ])

    report.append("4. Category Analysis")
    for eco, eco_repos in sub_ecosystem_repos.items():
        if eco != "Unrelated":
            count = len(eco_repos)
            percentage = (count / total_repos) * 100
            report.extend([
                f"   {eco}: {count} ({percentage:.2f}%)",
                *[f"   - {url}" for url in sorted(eco_repos)],
                ""
            ])

    report.extend([
        f"   Unrelated: {unrelated_count} ({unrelated_percentage:.2f}%)",
        *[f"   - {url}" for url in sorted(sub_ecosystem_repos["Unrelated"])],
        ""
    ])

    return report

def generate_stats(input_file: str, output_file: str) -> None:
    """
    Generate statistics from input file and write to output file.

    Args:
        input_file (str): Path to the input TOML file.
        output_file (str): Path to the output statistics file.
    """
    with open(input_file, 'r', encoding='utf-8') as file:
        content = file.read()

    repos, github_accounts, missing_repos, org_accounts, individual_accounts = extract_repo_info(content)

    categories = {
        "DeFi": [
            r"\b(?:de)?fi(?:nance)?\b", r"\bswap(?:ping)?\b", r"\bexchange\b", r"\blend(?:ing)?\b",
            r"\bborrow(?:ing)?\b", r"\byield\b", r"\bamm\b", r"\bliquidity\b", r"\bstaking\b", r"\bvault\b",
            r"\bsynthetic(?:s)?\b", r"\bderivative(?:s)?\b", r"\bmoney\s*market\b", r"\basset\s*management\b",
            r"\bdex\b", r"\bdecentralized\s*exchange\b", r"\baave\b", r"\bcompound\b", r"\buniswap\b",
            r"\bsushiswap\b", r"\bcurve\b", r"\bbalancer\b"
        ],
        "Gaming": [
            r"\bgam(?:e|ing)\b", r"\bnft\b", r"\bcollectible\b", r"\bmetaverse\b", r"\bplay.*earn\b",
            r"\bvirtual\s*world\b", r"\bavatar\b", r"\besports?\b", r"\baxie\b", r"\bdecentraland\b",
            r"\bsandbox\b", r"\bcryptokitties\b"
        ],
        "Social": [
            r"\bsocial\b", r"\bcommunity\b", r"\bmessag(?:e|ing)\b", r"\bchat\b", r"\bforum\b",
            r"\bnetwork(?:ing)?\b", r"\bcontent\b", r"\bmedia\b", r"\bblog\b", r"\bmicroblog(?:ging)?\b",
            r"\bprofile\b", r"\bsteemit\b", r"\bdtube\b", r"\bpeepeth\b"
        ],
        "Infrastructure and Tools": [
            r"\binfra(?:structure)?\b", r"\bprotocol\b", r"\bchain\b", r"\bnetwork\b", r"\boracle\b",
            r"\bbridge\b", r"\bscaling\b", r"\blayer[_\s]?2\b", r"\bl2\b", r"\binteroperability\b",
            r"\bcross[-\s]chain\b", r"\bconsensus\b", r"\bnode\b", r"\bvalidator\b", r"\bpolkadot\b",
            r"\bkosmos\b", r"\bchainlink\b", r"\boptimism\b", r"\barbitrum\b", r"\banalytics?\b", r"\bdata\b",
            r"\bmetrics?\b", r"\bdashboard\b", r"\bvisualization\b", r"\breporting\b", r"\binsights?\b",
            r"\bintelligence\b", r"\bmonitoring\b", r"\btracking\b", r"\bdune\s*analytics\b", r"\bnansen\b",
            r"\bglassnode\b", r"\bidentity\b", r"\bdid\b", r"\bdecentralized\s*id\b", r"\bssi\b",
            r"\bself[-\s]sovereign\b", r"\bkyc\b", r"\bknow\s*your\s*customer\b", r"\bauthentication\b",
            r"\bcivic\b", r"\buport\b", r"\bselfkey\b", r"\btoken(?:iz(?:e|ation))?\b", r"\basset[-\s]backed\b",
            r"\bsecurity\s*token\b", r"\butility\s*token\b", r"\bnft\b", r"\bnon[-\s]fungible\b",
            r"\berc[-\s]?20\b", r"\berc[-\s]?721\b", r"\berc[-\s]?1155\b", r"\bdev\s*tools?\b", r"\bsdk\b",
            r"\bapi\b", r"\blibrary\b", r"\bframework\b", r"\btesting\b", r"\bdeployment\b", r"\bide\b",
            r"\bcompiler\b", r"\bweb3[._]?js\b", r"\bethers[._]?js\b", r"\btruffle\b", r"\bhardhat\b",
            r"\bganache\b", r"\bwallet\b", r"\bcustody\b", r"\bkey\s*management\b", r"\bmulti[-\s]sig\b",
            r"\bhardware\s*wallet\b", r"\bmetamask\b", r"\btrezor\b", r"\bledger\b", r"\bprivacy\b",
            r"\bencrypt(?:ion)?\b", r"\banonymous\b", r"\bconfidential\b", r"\bzero[-\s]knowledge\b", r"\bzk\b",
            r"\bmixer\b", r"\btumbler\b", r"\bsecure\s*messaging\b", r"\bmonero\b", r"\bzcash\b",
            r"\btornado\s*cash\b", r"\bsmart\s*contract\b", r"\bsolidity\b", r"\bvyper\b", r"\bmove\b",
            r"\brust\b", r"\bink!\b", r"\bopenzeppelin\b"
        ],
        "Marketplaces": [
            r"\bmarketplace\b", r"\bauction\b", r"\be[-\s]commerce\b", r"\bbuy\b", r"\bsell\b", r"\btrade\b",
            r"\bopensea\b", r"\brarible\b", r"\bfoundation\b"
        ]
    }

    categories = {k: [re.compile(v, re.IGNORECASE) for v in vs] for k, vs in categories.items()}

    report = generate_report(repos, github_accounts, missing_repos, categories, org_accounts, individual_accounts)

    with open(output_file, 'w', encoding='utf-8') as file:
        file.write('\n'.join(report))

    logging.info("Report generated: %s", output_file)

def main() -> None:
    """Parse command-line arguments and generate statistics from TOML files."""
    parser = argparse.ArgumentParser(description="Generate statistics from TOML repository files.")
    parser.add_argument("toml_file", help="Name of the TOML file to process (e.g. sui.toml, aptos.toml)")
    args = parser.parse_args()

    current_date = datetime.now().strftime("%m-%d-%y")
    
    # Use existing directories in toml-tools
    toml_tools_root = os.path.dirname(os.path.dirname(__file__))
    input_dir = os.path.join(toml_tools_root, 'input')
    output_dir = os.path.join(toml_tools_root, 'output')

    # Look for specified TOML file in input directory
    input_path = os.path.join(input_dir, args.toml_file)
    if not os.path.exists(input_path):
        logging.error("File %s not found in input directory.", args.toml_file)
        sys.exit(1)

    # Get just the filename without extension for the output
    base_name = os.path.splitext(os.path.basename(input_path))[0]
    output_filename = f"{base_name}-stats-{current_date}.txt"
    output_path = os.path.join(output_dir, output_filename)
    generate_stats(input_path, output_path)
    logging.info("Generated stats for %s -> %s", input_path, output_filename)

    logging.info("Statistics have been generated and saved in the 'toml-tools/output' folder.")

if __name__ == "__main__":
    main()

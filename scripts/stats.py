"""Module for generating statistics from TOML repository files."""
import re
import os
import sys
import argparse
from datetime import datetime
import logging
from collections import defaultdict
from typing import Dict, Set, List, Tuple
from report.constants import COMPILED_CATEGORIES

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def extract_repo_info(content: str) -> Tuple[List[Dict[str, str]], Set[str], int, Set[str], Set[str]]:
    repos = []
    github_accounts = set()
    missing_repos = 0
    org_accounts = set()
    individual_accounts = set()
    repo_pattern = re.compile(
        r'\[\[repo\]\]\s*url\s*=\s*"(https://github\.com/([^/]+)/([^/"\s]+))"'
        r'(?:\s*missing\s*=\s*(true|false))?', re.IGNORECASE
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
    """Categorize repositories based on predefined patterns."""
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
    team_github_accounts = set(re.findall(r'team_github\s*=\s*"(.*?)"', content))
    individual_contributors_match = re.search(r'individual_contributors\s*=\s*\[(.*?)\]', content, re.DOTALL)
    individual_contributors = set(
        contributor.strip().strip('"')
        for contributor in individual_contributors_match.group(1).split(',')
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
    report = [
        "# Ecosystem Analysis Report",
        f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "## 1. Overview",
        "| Metric | Count |",
        "|--------|-------|",
        f"| Total repositories | {len(repos) + missing_repos} |",
        f"| Valid repositories | {len(repos)} |",
        f"| Missing repositories | {missing_repos} |",
        f"| Unique GitHub accounts | {len(github_accounts)} |",
        f"| Estimated individual accounts | {len(individual_accounts)} |",
        f"| Estimated organization/team accounts | {len(org_accounts)} |",
        "",
        "## 2. Ecosystem Analysis"
    ]

    sub_ecosystem_repos = categorize_repos(repos, categories)
    total_repos = len(repos)
    report.extend([
        "| Category | Count | Percentage |",
        "|----------|-------|------------|"
    ])

    for eco, eco_repos in sub_ecosystem_repos.items():
        if eco != "Unrelated":
            count = len(eco_repos)
            percentage = (count / total_repos) * 100
            report.append(f"| {eco} | {count} | {percentage:.2f}% |")

    unrelated_count = len(sub_ecosystem_repos["Unrelated"])
    unrelated_percentage = (unrelated_count / total_repos) * 100
    report.append(f"| Unrelated | {unrelated_count} | {unrelated_percentage:.2f}% |")
    report.append("")

    report.append("## 3. Account Analysis")
    account_repos = defaultdict(list)
    for repo in repos:
        account_repos[repo['account']].append(repo['url'])

    sorted_accounts = sorted(account_repos.items(), key=lambda x: len(x[1]), reverse=True)
    report.extend([
        "| Account | Type | Repository Count | Repositories |",
        "|---------|------|------------------|--------------|"
    ])

    for account, repo_list in sorted_accounts:
        if len(repo_list) >= 5:
            account_type = "organization/team" if account in org_accounts else "individual"
            repo_links = "<br>".join(repo_list)
            report.append(f"| {account} | {account_type} | {len(repo_list)} | {repo_links} |")

    report.append("")
    report.append("## 4. Category Analysis")

    for eco, eco_repos in sub_ecosystem_repos.items():
        if eco_repos:
            count = len(eco_repos)
            percentage = (count / total_repos) * 100
            report.extend([
                f"### {eco} ({count} - {percentage:.2f}%)",
                "| Repository |",
                "|------------|",
                *[f"| {url} |" for url in sorted(eco_repos)],
                ""
            ])

    report.extend([
        "## 5. GitHub Accounts",
        "### Organization/Team Accounts",
        "| Account | Profile Link |",
        "|---------|--------------|",
        *[f"| {account} | https://github.com/{account} |" for account in sorted(org_accounts)],
        "",
        "### Individual Accounts",
        "| Account | Profile Link |",
        "|---------|--------------|",
        *[f"| {account} | https://github.com/{account} |" for account in sorted(individual_accounts)],
        "",
        "## 6. All GitHub Accounts",
        "| Account | Profile Link |",
        "|---------|--------------|",
        *[f"| {account} | https://github.com/{account} |" for account in sorted(github_accounts)],
        ""
    ])

    return report

def generate_stats(input_file: str, output_file: str) -> None:
    """Generate statistics from input TOML file and write to output markdown file."""
    with open(input_file, 'r', encoding='utf-8') as file:
        content = file.read()

    repos, github_accounts, missing_repos, org_accounts, individual_accounts = extract_repo_info(content)
    report = generate_report(repos, github_accounts, missing_repos, COMPILED_CATEGORIES, org_accounts, individual_accounts)

    with open(output_file, 'w', encoding='utf-8') as file:
        file.write('\n'.join(report))

    logging.info("Report generated: %s", output_file)

def main() -> None:
    parser = argparse.ArgumentParser(description="Generate statistics from TOML repository files.")
    parser.add_argument("ecosystem", help="Name of the ecosystem to process (e.g. sui, aptos)")
    args = parser.parse_args()

    current_date = datetime.now().strftime("%m-%d-%y")
    toml_tools_root = os.path.dirname(os.path.dirname(__file__))
    input_dir = os.path.join(toml_tools_root, 'input')
    output_dir = os.path.join(toml_tools_root, 'output')

    input_path = os.path.join(input_dir, f"{args.ecosystem}.toml")
    if not os.path.exists(input_path):
        logging.error("File %s.toml not found in input directory.", args.ecosystem)
        sys.exit(1)

    output_filename = f"{args.ecosystem}-stats-{current_date}.md"
    output_path = os.path.join(output_dir, output_filename)

    generate_stats(input_path, output_path)
    logging.info("Generated stats for %s -> %s", input_path, output_filename)
    logging.info("Statistics have been generated and saved in the 'toml-tools/output' folder.")

if __name__ == "__main__":
    main()
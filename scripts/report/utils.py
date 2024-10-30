from collections import defaultdict
import re
import logging
from typing import Dict, List, Tuple, Set
from report.constants import REPO_PATTERN

def categorize_repos(repos: List[Dict[str, str]], categories: Dict[str, List[re.Pattern]]) -> Dict[str, List[str]]:
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

def extract_repo_info(content: str) -> Tuple[int, List[Dict[str, str]], Set[str], int, Set[str], Set[str]]:
    """Extract repository information from the given content."""
    repos = []
    github_accounts = set()
    missing_repos = 0
    org_accounts = set()
    individual_accounts = set()

    total_repos = len(REPO_PATTERN.findall(content))
    
    for match in REPO_PATTERN.finditer(content):
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

    logging.debug("Total repos: %d, Valid: %d, Missing: %d", total_repos, len(repos), missing_repos)
    logging.debug("GitHub accounts: %d, Org: %d, Individual: %d", len(github_accounts), len(org_accounts), len(individual_accounts))
    
    return total_repos, repos, github_accounts, missing_repos, org_accounts, individual_accounts

def organize_toml_content(content: str) -> str:
    """Organize TOML content by sorting sections and their contents."""
    sections = {}
    current_section = None
    for line in content.split('\n'):
        line = line.strip()
        if line.startswith('[') and line.endswith(']'):
            current_section = line[1:-1]
            sections[current_section] = []
        elif current_section and '=' in line:
            sections[current_section].append(line)

    organized_data = {k: sorted(v, key=lambda x: x.lower()) for k, v in sorted(sections.items())}

    organized_content = []
    for section, lines in organized_data.items():
        organized_content.append(f'[{section}]')
        organized_content.extend(lines)
        organized_content.append('')

    return '\n'.join(organized_content)


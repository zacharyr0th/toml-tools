from collections import defaultdict
import re
import logging
from typing import Dict, List, Tuple, Set
from report.constants import REPO_PATTERN, CATEGORIES

def categorize_repos(repos: List[str], categories: Dict) -> Tuple[Dict, Dict, Dict]:
    """Categorize repositories based on patterns."""
    # Initialize all dictionaries with proper structure first
    categorized_repos = {cat: [] for cat in categories.keys()}
    pattern_matches = {cat: {pattern: [] for strength, patterns in categories[cat]['patterns'] 
                           for pattern in patterns} for cat in categories.keys()}
    pattern_counts = {cat: {pattern: 0 for strength, patterns in categories[cat]['patterns']
                          for pattern in patterns} for cat in categories.keys()}
    
    for repo in repos:
        repo_url = repo['url']
        
        for category, cat_data in categories.items():
            # Skip if repo matches any exclusion patterns
            excluded = False
            for exclude_pattern in cat_data.get('exclude_patterns', []):
                if re.search(exclude_pattern, repo_url, re.IGNORECASE):
                    excluded = True
                    break
            
            if excluded:
                continue
                
            # Check each pattern strength level
            for strength, patterns in cat_data['patterns']:
                for pattern in patterns:
                    if re.search(pattern, repo_url, re.IGNORECASE):
                        categorized_repos[category].append(repo_url)
                        pattern_matches[category][pattern].append(repo_url)
                        pattern_counts[category][pattern] += 1
                        break  # Move to next category once we find a match
    
    return categorized_repos, pattern_matches, pattern_counts

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


"""Utility functions for report generation."""
import re
import logging
from typing import Dict, List, Tuple, Set
from collections import defaultdict

from .categories import CategoryRegistry

# Initialize category registry
registry = CategoryRegistry()

# Regular expression for GitHub repository URLs
REPO_PATTERN = re.compile(r'url\s*=\s*"(https://github\.com/[^"]+)"')

def extract_repo_info(content: str) -> Tuple[List[str], Set[str], List[str], Set[str], Set[str]]:
    """Extract repository information from TOML content."""
    repos = []
    github_accounts = set()
    missing_repos = []
    org_accounts = set()
    individual_accounts = set()
    
    for line in content.split('\n'):
        if 'url = ' in line:
            match = REPO_PATTERN.search(line)
            if match:
                repo_url = match.group(1)
                repos.append(repo_url)
                
                # Extract GitHub account
                parts = repo_url.split('/')
                if len(parts) >= 2:
                    account = parts[-2]
                    github_accounts.add(account)
                    
                    # Classify account type
                    if any(char.isupper() for char in account):
                        org_accounts.add(account)
                    else:
                        individual_accounts.add(account)
        
        elif 'missing = true' in line:
            # Get the last URL we processed
            if repos:
                missing_repos.append(repos[-1])
    
    return repos, github_accounts, missing_repos, org_accounts, individual_accounts

def categorize_repos(repos: List[str]) -> Dict[str, List[str]]:
    """Categorize repositories using the category registry."""
    categorized = defaultdict(list)
    
    for repo in repos:
        categories = registry.categorize_text(repo)
        if not categories:
            categories = ["Uncategorized"]
        
        for category in categories:
            categorized[category].append(repo)
    
    return dict(categorized)

def calculate_category_stats(categorized_repos: Dict[str, List[str]], total_repos: int) -> Dict[str, Dict[str, str]]:
    """Calculate statistics for each category."""
    stats = {}
    
    for category, repos in categorized_repos.items():
        count = len(repos)
        percentage = (count / total_repos * 100) if total_repos > 0 else 0
        stats[category] = {
            'count': count,
            'percentage': f"{percentage:.2f}%"
        }
    
    return stats

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


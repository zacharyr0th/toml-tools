"""Utility functions for report generation."""
import re
import logging
from typing import Dict, List, Tuple, Set
from collections import defaultdict

from ..categories import CategoryRegistry

# Initialize category registry
registry = CategoryRegistry()

# Regular expression for GitHub repository URLs
REPO_PATTERN = re.compile(r'url\s*=\s*"(https://github\.com/[^"]+)"')

def convert_categories_to_dict(registry: CategoryRegistry) -> Dict[str, Dict]:
    """Convert category objects to the format expected by the report generator."""
    categories = {}
    
    for category in registry.get_all_categories():
        categories[category.name] = {
            'patterns': category.patterns,
            'negative_patterns': category.negative_patterns,
            'exclude_categories': category.exclude_categories,
            'threshold': category.threshold
        }
    
    # Add Uncategorized category
    categories["Uncategorized"] = {
        'patterns': [],
        'negative_patterns': [],
        'exclude_categories': [],
        'threshold': 0.0
    }
    
    return categories

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

def get_repo_text(repo_url: str) -> str:
    """Extract searchable text from repository URL."""
    # Split URL into parts
    parts = repo_url.split('/')
    if len(parts) >= 2:
        owner = parts[-2]
        repo_name = parts[-1]
        # Combine owner and repo name, replacing separators with spaces
        text = f"{owner} {repo_name.replace('-', ' ').replace('_', ' ')}"
        return text.lower()
    return repo_url.lower()

def categorize_repos(repos: List[str]) -> Dict[str, List[str]]:
    """Categorize repositories using the category registry."""
    categorized = defaultdict(list)
    
    for repo in repos:
        repo_text = get_repo_text(repo)
        matched_categories = []
        
        # Check each category
        for category in registry.get_all_categories():
            # Check negative patterns first
            skip = False
            for pattern in category.compiled_patterns['negative']:
                if pattern.search(repo_text):
                    skip = True
                    break
            
            if skip:
                continue
            
            # Check positive patterns and calculate score
            score = 0.0
            matches = []
            for pattern in category.compiled_patterns['positive']:
                if pattern.search(repo_text):
                    pattern_str = pattern.pattern
                    matches.append(pattern_str)
                    score += category.weights.get(pattern_str, 0.0)
            
            # If score exceeds threshold, add to matched categories
            if score >= category.threshold:
                matched_categories.append(category.name)
        
        # If no categories matched, mark as uncategorized
        if not matched_categories:
            categorized["Uncategorized"].append(repo)
        else:
            for category in matched_categories:
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

__all__ = [
    'REPO_PATTERN',
    'convert_categories_to_dict',
    'extract_repo_info',
    'categorize_repos',
    'calculate_category_stats',
] 
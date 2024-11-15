from collections import defaultdict
import re
from typing import List, Dict, Tuple, Set
from constants import PATTERN_WEIGHTS, CATEGORIES, REPO_PATTERN

def extract_repo_info(content: str) -> Tuple[int, List[str], Set[str], Dict, Dict, Dict]:
    """Extract repository information from TOML content."""
    total_repos = len(REPO_PATTERN.findall(content))
    repos = [match[0] for match in REPO_PATTERN.findall(content)]
    categories = set()
    return total_repos, repos, categories, {}, {}, {}

def categorize_repos(repos: List[str], categories: Dict[str, List[str]]) -> Tuple[Dict[str, List[str]], Dict[str, Dict[str, List[str]]]]:
    """
    Categorize repositories based on pattern matching.
    
    Returns:
        Tuple containing:
        - Dictionary mapping categories to unique repos
        - Dictionary of pattern matches for verbose output
    """
    # Changed from defaultdict(set) to defaultdict(list) since we're dealing with dicts
    categorized = defaultdict(list)
    pattern_matches = defaultdict(lambda: defaultdict(list))
    
    # Track which repos have been categorized using their URLs
    categorized_repos = set()
    
    # First pass: categorize repos based on patterns
    for category, patterns in categories.items():
        for pattern in patterns:
            for repo in repos:
                # Extract the URL from the repo dict if it's a dictionary
                repo_str = repo['url'] if isinstance(repo, dict) else repo
                if re.search(pattern, repo_str):
                    # Only append if the URL isn't already in this category
                    repo_url = repo['url'] if isinstance(repo, dict) else repo
                    if repo_url not in [r['url'] if isinstance(r, dict) else r for r in categorized[category]]:
                        categorized[category].append(repo)
                        categorized_repos.add(repo_url)
                        pattern_matches[category][pattern].append(repo)
    
    # Add remaining uncategorized repos
    uncategorized = [repo for repo in repos if (repo['url'] if isinstance(repo, dict) else repo) not in categorized_repos]
    if uncategorized:
        categorized["Uncategorized"] = uncategorized
    
    return dict(categorized), pattern_matches

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


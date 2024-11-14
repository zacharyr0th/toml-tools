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

def categorize_repos(repos: List[str], categories: Dict) -> Tuple[Dict, Dict, Dict]:
    """Categorize repositories based on defined patterns."""
    categorized_repos = defaultdict(list)
    pattern_matches = defaultdict(dict)
    pattern_counts = defaultdict(lambda: defaultdict(int))
    
    for repo in repos:
        repo_has_match = False
        
        for category, cat_data in categories.items():
            score = 0
            repo_patterns = set()
            
            for strength, patterns in cat_data['patterns']:
                weight = PATTERN_WEIGHTS[strength]
                for pattern in patterns:
                    if re.search(pattern, repo, re.IGNORECASE):
                        score += weight
                        repo_patterns.add(pattern)
                        pattern_counts[category][pattern] += 1
            
            if 'negative_patterns' in cat_data:
                for pattern in cat_data['negative_patterns']:
                    if re.search(pattern, repo, re.IGNORECASE):
                        score = 0
                        break
            
            if score >= cat_data.get('threshold', 1.0):
                categorized_repos[category].append(repo)
                pattern_matches[repo][category] = list(repo_patterns)
                repo_has_match = True
        
        # If repo didn't match any category, mark it as uncategorized
        if not repo_has_match:
            categorized_repos["Uncategorized"].append(repo)
            pattern_matches[repo]["Uncategorized"] = True
            pattern_counts["Uncategorized"]["uncategorized"] += 1
    
    return categorized_repos, pattern_matches, pattern_counts

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


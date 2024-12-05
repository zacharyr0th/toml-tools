from collections import defaultdict
import re
from typing import List, Dict, Tuple, Set
from constants import PATTERN_WEIGHTS, CATEGORIES, REPO_PATTERN
import logging

def extract_repo_info(content: str) -> Tuple[int, List[str], Set[str], Dict, Dict, Dict]:
    """Extract repository information from TOML content."""
    matches = REPO_PATTERN.findall(content)
    total_repos = len(matches)
    repos = [match[0] for match in matches]  # Get the full URL
    categories = set()
    return total_repos, repos, categories, {}, {}, {}

def categorize_repos(repos: List[str], categories: Dict[str, Dict]) -> Tuple[Dict[str, List[str]], Dict[str, Dict[str, List[str]]]]:
    """Categorize repositories based on pattern matching."""
    logging.info(f"Starting categorization of {len(repos)} repositories")
    
    categorized = defaultdict(list)
    pattern_matches = defaultdict(lambda: defaultdict(list))
    
    for i, repo in enumerate(repos):
        if i % 100 == 0:  # Log progress every 100 repos
            logging.info(f"Processing repo {i}/{len(repos)}")
            
        repo_matched = False
        
        # Check each category
        for category, cat_data in categories.items():
            if category == "Uncategorized":
                continue
                
            score = 0
            matched_patterns = []
            
            # Check patterns by strength
            for strength, patterns in cat_data['patterns']:
                weight = PATTERN_WEIGHTS[strength]
                for pattern in patterns:
                    if re.search(pattern, repo, re.IGNORECASE):
                        score += weight
                        matched_patterns.append(pattern)
                        logging.debug(f"Matched pattern '{pattern}' in repo '{repo}' for category '{category}'")
            
            # If score meets threshold, add to category
            if score >= cat_data.get('threshold', 1.0):
                categorized[category].append(repo)
                for pattern in matched_patterns:
                    pattern_matches[category][pattern].append(repo)
                repo_matched = True
                logging.debug(f"Categorized '{repo}' as '{category}' with score {score}")
        
        # If no category matched, mark as uncategorized
        if not repo_matched:
            categorized["Uncategorized"].append(repo)
            pattern_matches["Uncategorized"]["unmatched"].append(repo)
    
    # Log final categorization results
    for category, repos_list in categorized.items():
        logging.info(f"Category '{category}': {len(repos_list)} repositories")
    
    return dict(categorized), dict(pattern_matches)

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


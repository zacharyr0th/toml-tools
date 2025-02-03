import re
import logging
from typing import Dict
from collections import defaultdict
from .categories import CategoryRegistry
from .utils import categorize_repos

# Initialize category registry
registry = CategoryRegistry()

def analyze_ecosystem_patterns(ecosystem_data: Dict) -> Dict[str, Dict]:
    pattern_counts = defaultdict(int)
    pattern_matches = {}
    uncategorized_count = 0  # Add counter for debugging
    
    for repo_url in ecosystem_data['repos']:
        pattern_matches[repo_url] = {}
        repo_has_match = False
        
        # Check each category's patterns using the registry
        for category in registry.get_all_categories():
            matches = registry.get_pattern_matches(repo_url)
            if matches and category.name in matches:
                pattern_matches[repo_url][category.name] = matches[category.name]
                repo_has_match = True
                # Update pattern counts
                for pattern in matches[category.name]:
                    pattern_counts[pattern] += 1
        
        # If repo didn't match any category, mark it as uncategorized
        if not repo_has_match:
            pattern_matches[repo_url]["Uncategorized"] = True
            pattern_counts["Uncategorized"] += 1
            uncategorized_count += 1  # Increment counter
    
    logging.info(f"Found {uncategorized_count} uncategorized repositories")  # Add debug log
    return {
        'pattern_counts': dict(pattern_counts),
        'pattern_matches': pattern_matches
    }
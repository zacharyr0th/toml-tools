import re
import logging
from typing import Dict
from collections import defaultdict
from constants import CATEGORIES, PATTERN_WEIGHTS

def analyze_ecosystem_patterns(ecosystem_data: Dict) -> Dict[str, Dict]:
    pattern_counts = defaultdict(int)
    pattern_matches = {}
    uncategorized_count = 0  # Add counter for debugging
    
    for repo_url in ecosystem_data['repos']:
        pattern_matches[repo_url] = {}
        repo_has_match = False
        
        # Check each category's patterns
        for category, cat_data in CATEGORIES.items():
            score = 0
            matched_patterns = []
            
            # Process patterns by strength
            for strength, patterns in cat_data['patterns']:
                weight = PATTERN_WEIGHTS[strength]
                for pattern in patterns:
                    if re.search(pattern, repo_url, re.IGNORECASE):
                        score += weight
                        matched_patterns.append(pattern)
                        pattern_counts[pattern] += 1
            
            # Check negative patterns
            if 'negative_patterns' in cat_data:
                for pattern in cat_data['negative_patterns']:
                    if re.search(pattern, repo_url, re.IGNORECASE):
                        score = 0
                        matched_patterns = []
                        break
            
            # If score meets threshold, record the match
            if score >= cat_data.get('threshold', 1.0):
                pattern_matches[repo_url][category] = matched_patterns
                repo_has_match = True
        
        # If repo didn't match any category, mark it as uncategorized
        if not repo_has_match:
            pattern_matches[repo_url]["Uncategorized"] = True
            pattern_counts["Uncategorized"] += 1
            uncategorized_count += 1  # Increment counter
    
    logging.info(f"Found {uncategorized_count} uncategorized repositories")  # Add debug log
    return {
        "pattern_counts": dict(pattern_counts),
        "pattern_matches": pattern_matches
    }
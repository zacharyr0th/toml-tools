"""Utility functions for working with categories."""
from typing import Dict, List, Tuple

from ..categories import CategoryRegistry

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

def get_pattern_matches(text: str, registry: CategoryRegistry) -> Dict[str, List[str]]:
    """Get all pattern matches for a given text across all categories."""
    matches = {}
    
    for category in registry.get_all_categories():
        category_matches = []
        
        # Check negative patterns first
        skip = False
        for pattern in category.compiled_patterns['negative']:
            if pattern.search(text):
                skip = True
                break
        
        if skip:
            continue
            
        # Check positive patterns
        for pattern in category.compiled_patterns['positive']:
            if pattern.search(text):
                category_matches.append(pattern.pattern)
        
        if category_matches:
            matches[category.name] = category_matches
    
    return matches 
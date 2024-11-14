"""Module for generating verbose sections of repository analysis reports."""

from collections import defaultdict
from typing import List, Dict, TextIO

def generate_verbose_section(f: TextIO, category: str, ecosystem_data: List[Dict], category_data: Dict):
    """Generate detailed verbose section showing all pattern matches with ecosystem differentiation."""
    f.write(f"\n### {category}\n\n")
    
    # Collect all pattern matches across ecosystems with ecosystem source
    all_pattern_matches = defaultdict(lambda: defaultdict(list))
    ecosystems = set()
    
    for ecosystem in ecosystem_data:
        eco_name = ecosystem['name']
        ecosystems.add(eco_name)
        cat_stats = ecosystem['categories'].get(category, {})
        pattern_matches = cat_stats.get('pattern_matches', {})
        for pattern, repos in pattern_matches.items():
            all_pattern_matches[pattern][eco_name].extend(repos)
    
    # Process each strength level
    for strength, pattern_list in category_data['patterns']:
        matching_patterns = [p for p in pattern_list if all_pattern_matches.get(p)]
        
        if matching_patterns:
            f.write(f"\n#### {strength} Patterns\n\n")
            
            # Sort patterns by total number of matches across ecosystems
            sorted_patterns = sorted(
                matching_patterns,
                key=lambda p: sum(len(repos) for repos in all_pattern_matches[p].values()),
                reverse=True
            )
            
            for pattern in sorted_patterns:
                total_matches = sum(len(repos) for repos in all_pattern_matches[pattern].values())
                display_pattern = pattern.replace('\\b', '').replace('\\', '')
                f.write(f"Pattern `{display_pattern}` ({total_matches:,} matches)\n\n")
                
                # Show matches by ecosystem
                for eco_name in sorted(ecosystems):
                    repos = sorted(set(all_pattern_matches[pattern][eco_name]))
                    if repos:
                        f.write(f"{eco_name} ({len(repos)} repos):\n")
                        for repo in repos:
                            f.write(f"- {repo}\n")
                        f.write("\n")
                
    # Show negative patterns if any exist
    if 'negative_patterns' in category_data:
        f.write("\n#### Negative Patterns (Exclusions)\n")
        for pattern in category_data['negative_patterns']:
            display_pattern = pattern.replace('\\b', '').replace('\\', '')
            f.write(f"- `{display_pattern}`\n")
    
    f.write("\n---\n")
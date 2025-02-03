"""Utility functions for pattern compilation and matching."""
import re
from typing import Dict, List, Pattern, Union

def compile_pattern(pattern: str, flags: Union[int, re.RegexFlag] = re.IGNORECASE) -> Pattern:
    """Compile a single regex pattern."""
    return re.compile(pattern, flags)

def compile_patterns(patterns: List[str], flags: Union[int, re.RegexFlag] = re.IGNORECASE) -> List[Pattern]:
    """Compile a list of regex patterns."""
    return [compile_pattern(pattern, flags) for pattern in patterns]

def match_any_pattern(text: str, patterns: List[Pattern]) -> bool:
    """Check if text matches any of the compiled patterns."""
    return any(pattern.search(text) for pattern in patterns)

def get_matching_patterns(text: str, patterns: List[Pattern]) -> List[Pattern]:
    """Get list of patterns that match the text."""
    return [pattern for pattern in patterns if pattern.search(text)]

# Repository pattern for GitHub URLs
REPO_PATTERN = compile_pattern(
    r'\[\[repo\]\]\s*url\s*=\s*"(https://github\.com/([^/]+)/([^/"\s]+))"'
    r'(?:\s*missing\s*=\s*(true|false))?'
) 
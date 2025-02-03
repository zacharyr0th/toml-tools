"""Base category class for pattern matching."""
import re
from typing import Dict, List, Pattern, Tuple, Optional, Set, ClassVar
from functools import lru_cache

from ..config.pattern_weights import PATTERN_WEIGHTS, DEFAULT_THRESHOLD

class BaseCategory:
    """Base class for all categories."""
    
    # Class-level cache for compiled patterns
    _pattern_cache: ClassVar[Dict[str, Pattern]] = {}
    
    def __init__(
        self,
        name: str,
        patterns: List[Tuple[str, List[str]]],
        negative_patterns: Optional[List[str]] = None,
        exclude_categories: Optional[List[str]] = None,
        threshold: float = DEFAULT_THRESHOLD
    ):
        """Initialize category with optimized pattern handling.
        
        Args:
            name: Category name
            patterns: List of (strength, pattern_list) tuples
            negative_patterns: List of patterns to exclude
            exclude_categories: List of category names to exclude
            threshold: Minimum score threshold
        """
        self.name = name
        self.patterns = patterns
        self.negative_patterns = negative_patterns or []
        self.exclude_categories = set(exclude_categories or [])  # Using set for O(1) lookups
        self.threshold = threshold
        self.compiled_patterns = self._compile_patterns()
        self.weights = self._create_weights()
    
    @staticmethod
    @lru_cache(maxsize=1000)  # Cache compiled patterns
    def _compile_pattern(pattern: str) -> Pattern:
        """Compile and cache a single regex pattern."""
        return re.compile(pattern, re.IGNORECASE)
    
    def _compile_patterns(self) -> Dict[str, List[Pattern]]:
        """Compile all patterns with caching."""
        compiled = {
            'positive': [],
            'negative': [self._compile_pattern(p) for p in self.negative_patterns]
        }
        
        for strength, pattern_list in self.patterns:
            for pattern in pattern_list:
                compiled['positive'].append(self._compile_pattern(pattern))
        
        return compiled
    
    def _create_weights(self) -> Dict[str, float]:
        """Create pattern weight mapping."""
        weights = {}
        for strength, pattern_list in self.patterns:
            weight = PATTERN_WEIGHTS[strength]
            for pattern in pattern_list:
                weights[pattern] = weight
        return weights
    
    def get_pattern_matches(self, text: str) -> Optional[List[str]]:
        """Get all matching patterns for a text.
        
        Args:
            text: Text to check for pattern matches
            
        Returns:
            Optional[List[str]]: List of matching patterns if any, None otherwise
        """
        # Check negative patterns first
        for pattern in self.compiled_patterns['negative']:
            if pattern.search(text):
                return None
        
        # Check positive patterns
        matches = []
        total_score = 0.0
        
        for pattern in self.compiled_patterns['positive']:
            if pattern.search(text):
                pattern_str = pattern.pattern
                matches.append(pattern_str)
                total_score += self.weights.get(pattern_str, 0.0)
        
        # Return matches only if threshold is met
        if matches and total_score >= self.threshold:
            return matches
        return None

    def matches(self, text: str) -> bool:
        """Check if text matches category patterns with optimized matching.
        
        Args:
            text: Text to check for matches
            
        Returns:
            bool: True if matches exceed threshold, False otherwise
        """
        # Quick check for negative patterns first (fail fast)
        if any(pattern.search(text) for pattern in self.compiled_patterns['negative']):
            return False
        
        # Calculate score with early exit if threshold is reached
        score = 0.0
        for pattern in self.compiled_patterns['positive']:
            if pattern.search(text):
                pattern_str = pattern.pattern
                score += self.weights.get(pattern_str, 0.0)
                if score >= self.threshold:  # Early exit if threshold is reached
                    return True
        
        return score >= self.threshold 
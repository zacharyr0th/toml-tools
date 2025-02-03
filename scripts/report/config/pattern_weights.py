"""Configuration for pattern weights used in category matching."""

PATTERN_WEIGHTS = {
    'STRONG': 1.0,
    'MEDIUM': 0.5,
    'WEAK': 0.3
}

DEFAULT_THRESHOLD = 0.3  # Lower threshold for more inclusive matching
STRICT_THRESHOLD = 0.8  # High threshold for strict matching 
"""AI & Education category patterns and matching logic."""
from typing import List, Tuple

from .base import BaseCategory
from ..config.pattern_weights import STRICT_THRESHOLD

# Common AI-related terms for pattern generation
AI_CORE_TERMS = [
    r"ai", r"artificial[-_]intelligence",
    r"ml", r"machine[-_]learning",
    r"deep[-_]learning", r"neural[-_]network",
    r"llm[s]?", r"large[-_]language[-_]model[s]?",
    r"gpt", r"chatbot[s]?",
]

AI_FEATURES = [
    r"train(?:ing)?", r"model[s]?",
    r"predict(?:ion)?", r"classify",
    r"detect(?:ion)?", r"recognize",
    r"generate", r"synthesis",
    r"optimize", r"automate"
]

AI_PROJECTS = [
    r"aptos[-_]assistant", r"overlai",
    r"aioz[-_]network", r"nimble[-_]network",
    r"aptos[-_]learn", r"movespiders",
    r"easya", r"bitskwela"
]

class AICategory(BaseCategory):
    """Category for AI & Education projects."""
    
    def __init__(self):
        """Initialize AI category with optimized patterns."""
        # Generate word boundary patterns
        core_patterns = [fr"\b{term}\b" for term in AI_CORE_TERMS]
        feature_patterns = [fr"\b{term}\b" for term in AI_FEATURES]
        
        # Generate prefix/suffix patterns
        prefix_patterns = [fr"{term}[-_]" for term in AI_CORE_TERMS[:4]]  # Only use core AI terms
        
        super().__init__(
            name="AI & Education",
            patterns=[
                ('STRONG', [
                    *AI_PROJECTS,  # Known AI projects
                    *core_patterns,  # Core AI terms with word boundaries
                    
                    # AI Task Patterns
                    r"\binference\b", r"\bprediction[s]?\b",
                    r"\bclassification\b", r"\bregression\b",
                    r"\bclustering\b", r"\bsegmentation\b",
                ]),
                ('MEDIUM', [
                    *prefix_patterns,  # AI-related prefixes
                    *feature_patterns,  # AI features with word boundaries
                    
                    # Additional medium-strength patterns
                    r"\bintelligent[-_]", r"\bsmart[-_]",
                    r"\badaptive[-_]", r"\blearning[-_]"
                ])
            ],
            negative_patterns=[
                # Exclude test/demo patterns
                r"test[-_]ai",
                r"demo[-_]ai",
                r"example[-_]ai",
                r"sample[-_]ai",
                r"learning[-_]purpose",
                r"practice[-_]"
            ],
            threshold=STRICT_THRESHOLD
        ) 
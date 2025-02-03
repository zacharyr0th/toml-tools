"""Registry for managing all categories."""
from typing import Dict, List, Type, Optional, Set
from functools import lru_cache

from .base import BaseCategory
from .defi import DefiCategory
from .nft import NFTCategory
from .gaming import GamingCategory
from .infrastructure import InfrastructureCategory
from .social import SocialCategory
from .analytics import AnalyticsCategory
from .security import SecurityCategory
from .education import EducationCategory
from .identity import IdentityCategory
from .contracts import ContractsCategory
from .wallets import WalletsCategory
from .ai import AICategory

class CategoryRegistry:
    """Registry for managing and accessing all categories."""
    
    def __init__(self):
        """Initialize registry with optimized category management."""
        self._categories: Dict[str, BaseCategory] = {}
        self._category_names: Set[str] = set()
        self._initialize_categories()
    
    def _initialize_categories(self) -> None:
        """Initialize all category instances with optimized instantiation."""
        category_classes = [
            DefiCategory,
            NFTCategory,
            GamingCategory,
            InfrastructureCategory,
            SocialCategory,
            AnalyticsCategory,
            SecurityCategory,
            EducationCategory,
            IdentityCategory,
            ContractsCategory,
            WalletsCategory,
            AICategory,
        ]
        
        # Initialize all categories at once
        for category_class in category_classes:
            category = category_class()
            self._categories[category.name] = category
            self._category_names.add(category.name)
    
    @lru_cache(maxsize=100)  # Cache category lookups
    def get_category(self, name: str) -> Optional[BaseCategory]:
        """Get a category by name with caching.
        
        Args:
            name: Category name to retrieve
            
        Returns:
            Optional[BaseCategory]: Category instance if found, None otherwise
        """
        return self._categories.get(name)
    
    def get_all_categories(self) -> List[BaseCategory]:
        """Get all registered categories.
        
        Returns:
            List[BaseCategory]: List of all category instances
        """
        return list(self._categories.values())
    
    def get_category_names(self) -> Set[str]:
        """Get all registered category names.
        
        Returns:
            Set[str]: Set of category names
        """
        return self._category_names
    
    @lru_cache(maxsize=1000)  # Cache categorization results
    def categorize_text(self, text: str) -> List[str]:
        """Categorize text with optimized matching and caching.
        
        Args:
            text: Text to categorize
            
        Returns:
            List[str]: List of matching category names
        """
        # Pre-allocate results list with estimated size
        matches = []
        matches_append = matches.append  # Local var for faster appends
        
        # Use items() instead of values() to avoid extra dict lookups
        for name, category in self._categories.items():
            if category.matches(text):
                matches_append(name)
        
        return matches 
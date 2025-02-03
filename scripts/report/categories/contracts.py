"""Smart Contracts & Core category patterns and matching logic."""
from .base import BaseCategory

class ContractsCategory(BaseCategory):
    """Category for Smart Contracts & Core projects."""
    
    def __init__(self):
        super().__init__(
            name="Smart Contracts & Core",
            patterns=[
                ('STRONG', [
                    # Core contract terms
                    r"\bsmart[-_]contract[s]?\b", r"\bcontract[-_]",
                    r"\bcontract[s]?\b", r"\bcontracts[-_]",
                    r"\bmodule[-_]", r"\bfunction[-_]",
                    r"\binterface[-_]", r"\blibrary[-_]",
                    
                    # Move specific
                    r"\bmove[-_]module\b", r"\bmove[-_]contract\b",
                    r"\bmove[-_]resource\b", r"\bmove[-_]capability\b",
                    r"\bmove[-_]stdlib\b", r"\bmove[-_]framework\b",
                    
                    # Aptos specific
                    r"\baptos[-_]framework\b", r"\baptos[-_]std\b",
                    r"\baptos[-_]token\b", r"\baptos[-_]coin\b",
                    r"\baptos[-_]account\b", r"\baptos[-_]resource\b",
                    r"\baptos[-_]module\b", r"\baptos[-_]contract\b",
                    
                    # Common contract types
                    r"[-_]vault[-_]contract",
                    r"[-_]staking[-_]contract",
                    r"[-_]bridge[-_]contract",
                    r"[-_]swap[-_]contract",
                    r"[-_]token[-_]contract",
                    r"[-_]nft[-_]contract",
                    r"[-_]dao[-_]contract",
                    r"[-_]governance[-_]",
                    r"contract[-_]library",
                    r"contract[-_]template",
                    r"contract[-_]factory",
                    r"contract[-_]proxy",
                    r"contract[-_]implementation",
                    
                    # Move/Aptos specific
                    r"move[-_]on[-_]aptos",
                    r"aptos[-_]move",
                    r"move[-_]example",
                    r"move[-_]tutorial",
                    r"aptos[-_]program"
                ]),
                ('MEDIUM', [
                    # Contract features
                    r"\bentry[-_]function\b", r"\bpublic[-_]function\b",
                    r"\bview[-_]function\b", r"\bscript[-_]function\b",
                    r"\bresource[-_]account\b", r"\bresource[-_]group\b",
                    r"\bsigner[-_]capability\b", r"\bstore[-_]capability\b",
                    r"\bstruct[-_]", r"\bevent[-_]", r"\berror[-_]",
                    r"\btype[-_]", r"\bgeneric[-_]", r"\bstorage[-_]",
                    r"\bmemory[-_]", r"\bstate[-_]", r"\bcallback[-_]",
                    r"\bcontract[-_]", r"[-_]contract\b",
                    
                    # Move/Aptos patterns
                    r"\bmove[-_]", r"\bresource[-_]", r"\bcapability[-_]",
                    r"\bsigner[-_]", r"\baccount[-_]", r"\baddress[-_]"
                ])
            ],
            negative_patterns=[
                r"test[-_]contract",
                r"demo[-_]contract",
                r"example[-_]only",
                r"learning[-_]purpose",
                r"practice[-_]"
            ],
            threshold=0.8
        ) 
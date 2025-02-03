"""DeFi & Financial category patterns and matching logic."""
from .base import BaseCategory

class DefiCategory(BaseCategory):
    """Category for DeFi & Financial projects."""
    
    def __init__(self):
        super().__init__(
            name="DeFi & Financial",
            patterns=[
                ('STRONG', [
                    # Core DeFi terms
                    r"\b(?:de)?fi\b", r"defi[-_]", r"_(?:de)?fi\b",
                    r"\bvault[s]?\b", r"\byield[s]?\b", r"\byielding\b",
                    r"\bamm\b", r"\bperpetual[s]?\b", r"\bperp[s]?\b",
                    r"\bswap\b", r"\bswaps\b", r"\bswapper\b", r"\bswapping\b",
                    r"\bstaking\b", r"\bstake[s]?\b", r"\bstaked\b",
                    r"\bliquid(?:ity|ation)\b", r"\blp[s]?\b", r"\bpool[s]?\b",
                    r"\bfarm(?:ing)?\b", r"\bharvest(?:er|ing)?\b",
                    r"\blend(?:ing)?\b", r"\bloan[s]?\b",
                    r"\bborrow(?:ing)?\b", r"\bcollateral\b",
                    r"\bmargin\b", r"\bleverage\b",
                    r"\bdex\b", r"\bdexes\b", r"\bdecentralized[-_]exchange\b",
                    
                    # Specific DeFi Projects
                    r"echelon", r"echo[-_]protocol",
                    r"merkle[-_]trade", r"amnis[-_]finance",
                    r"baptswap", r"cellana[-_]finance",
                    r"coinsender", r"defy", r"econia",
                    r"pancake", r"sushi", r"curve",
                    r"aave", r"compound", r"balancer",
                    
                    # Common DeFi Protocol Types
                    r"(?:money|lending|credit)[-_]market[s]?",
                    r"liquid[-_]staking",
                    r"perpetual[-_]dex",
                    r"order[-_]book",
                    r"dex[-_]aggregator",
                    r"yield[-_]farm",
                    r"yield[-_]aggregator",
                    r"lending[-_]protocol",
                    r"borrowing[-_]protocol",
                    r"dex[-_]protocol",
                    r"dex[-_]core",
                    r"dex[-_]router",
                    r"dex[-_]factory",
                    
                    # Protocol types
                    r"\blending[-_]protocol\b", r"\bliquid[-_]staking\b",
                    r"\bstaking[-_]protocol\b", r"\bfinance[-_]", r"\bfinancial[-_]",
                    r"\bmonetary[-_]", r"\bvetoken[s]?\b",
                    r"\bvault[-_]strategy\b", r"\byield[-_]optimizer\b",
                    r"\byield[-_]booster\b", r"\bleveraged[-_]yield\b",
                    r"\bflash[-_]loan\b", r"\bflash[-_]mint\b",
                    r"\bliquidity[-_]mining\b", r"\bliquidity[-_]provision\b",
                ]),
                ('MEDIUM', [
                    r"\btoken[s]?\b", r"\bcoin[s]?\b",
                    r"\bcrypto\b", r"\bcurrency\b",
                    r"\bprice[s]?\b", r"\brate[s]?\b",
                    r"\bfee[s]?\b", r"\binterest\b",
                    r"\bmarket[s]?\b", r"\btrading\b",
                    r"\bexchange\b", r"\bswap\b",
                    r"\byield\b", r"\bapy\b",
                    r"\breward[s]?\b", r"\bincentive[s]?\b",
                    r"\bbridge\b", r"\bcross[-_]chain\b",
                    r"\bwrapped\b", r"\bsynthetic\b",
                    r"\bdex[-_]", r"[-_]dex\b",
                ]),
                ('WEAK', [
                    r"\btest[-_]token[s]?\b", r"\bdummy[-_]token[s]?\b",
                    r"\bsample[-_]token[s]?\b", r"\btoken[-_]test[s]?\b",
                    r"\bexample[-_]", r"\bdemo[-_]", r"\btest[-_]",
                ])
            ],
            negative_patterns=[
                r"test[-_]defi",
                r"demo[-_]defi",
                r"example[-_]defi",
                r"learning[-_]purpose",
                r"practice[-_]"
            ],
            exclude_categories=['Infrastructure & Tools']
        ) 
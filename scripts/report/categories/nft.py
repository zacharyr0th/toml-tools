"""NFTs & Digital Assets category patterns and matching logic."""
from .base import BaseCategory
from ..config.pattern_weights import STRICT_THRESHOLD

class NFTCategory(BaseCategory):
    """Category for NFTs & Digital Assets projects."""
    
    def __init__(self):
        super().__init__(
            name="NFTs & Digital Assets",
            patterns=[
                ('STRONG', [
                    # Core NFT terms
                    r"\bnft[s]?\b", r"[-_]nft[s]?\b", r"\bnft[-_]",
                    r"\bcollectible[s]?\b", r"\bdigital[-_]art\b",
                    r"\btoken[-_]standard\b", r"\btoken[-_]uri\b",
                    r"\bmetadata[-_]standard\b", r"\btoken[-_]metadata\b",
                    
                    # NFT Features
                    r"\bmint(?:ing|er)?\b", r"\bmint[-_]",
                    r"\bburn(?:ing|er)?\b", r"\bburn[-_]",
                    r"\btransfer(?:able)?\b", r"\btransfer[-_]",
                    r"\btoken[-_]id\b", r"\btoken[-_]uri\b",
                    r"\broyalt(?:y|ies)\b", r"\broyalty[-_]",
                    
                    # NFT Types
                    r"\bart[-_]", r"\bmusic[-_]", r"\baudio[-_]",
                    r"\bvideo[-_]", r"\bimage[-_]", r"\bphoto[-_]",
                    r"\bgame[-_]asset[s]?\b", r"\bvirtual[-_]",
                    r"\bdigital[-_]good[s]?\b", r"\bdigital[-_]item[s]?\b",
                    
                    # NFT Marketplaces
                    r"\bmarketplace\b", r"\bauction\b",
                    r"\bgallery\b", r"\bexhibition\b",
                    r"\bcollection[s]?\b", r"\bcurator\b",
                    r"\bartist[s]?\b", r"\bcreator[s]?\b",
                    
                    # Additional NFT Features
                    r"\bairdrop[s]?\b", r"\bdrop[s]?\b",
                    r"\blimited[-_]edition\b", r"\brare\b",
                    r"\bunique[-_]token[s]?\b", r"\bsoul[-_]bound\b",
                    r"\bpfp[s]?\b", r"\bavatar[s]?\b",
                    r"\bmetaverse\b", r"\bvirtual[-_]world\b",
                    r"\bwearable[s]?\b", r"\bdigital[-_]fashion\b",
                    r"\btoken[-_]gating\b", r"\baccess[-_]token[s]?\b",
                    
                    # NFT Standards
                    r"\berc[-_]721\b", r"\berc[-_]1155\b",
                    r"\btoken[-_]standard[s]?\b", r"\btoken[-_]interface\b",
                    r"\btoken[-_]contract[s]?\b", r"\bsmart[-_]nft[s]?\b",
                    
                    # NFT Trading
                    r"\bfloor[-_]price\b", r"\blisting[s]?\b",
                    r"\bbid[s]?\b", r"\boffer[s]?\b",
                    r"\btrade[s]?\b", r"\bswap[s]?\b",
                    r"\bescrow\b", r"\bsecondary[-_]market\b"
                ]),
                ('MEDIUM', [
                    r"\bcollection[-_]", r"\bgallery[-_]",
                    r"\bartist[-_]", r"\bcreator[-_]",
                    r"\bdigital[-_]", r"\bvirtual[-_]",
                    r"\btoken[-_]", r"\basset[-_]",
                    r"\bmetadata[-_]", r"\buri[-_]",
                    r"\bimage[-_]", r"\bmedia[-_]",
                    r"\brender[-_]", r"\bdisplay[-_]",
                    r"\bview[-_]", r"\bpreview[-_]",
                    
                    # Additional Medium Strength Patterns
                    r"\bcollectable[-_]", r"\brarity[-_]",
                    r"\bexclusive[-_]", r"\bpremium[-_]",
                    r"\bseries[-_]", r"\bedition[-_]",
                    r"\blaunch[-_]", r"\bdrop[-_]",
                    r"\bshowcase[-_]", r"\bexhibit[-_]",
                    r"\bfeature[-_]", r"\bproperty[-_]",
                    r"\battribute[-_]", r"\btrait[-_]"
                ])
            ],
            negative_patterns=[
                r"test[-_]nft",
                r"demo[-_]nft",
                r"example[-_]nft",
                r"sample[-_]token",
                r"learning[-_]purpose",
                r"practice[-_]",
                r"mock[-_]nft",
                r"fake[-_]token",
                r"placeholder[-_]nft",
                r"testing[-_]purpose"
            ],
            exclude_categories=['DeFi & Financial'],
            threshold=STRICT_THRESHOLD
        ) 
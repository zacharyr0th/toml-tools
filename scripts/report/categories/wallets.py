"""Wallets & Security category patterns and matching logic."""
from .base import BaseCategory

class WalletsCategory(BaseCategory):
    """Category for Wallets & Security projects."""
    
    def __init__(self):
        super().__init__(
            name="Wallets & Security",
            patterns=[
                ('STRONG', [
                    # Core Wallet Terms
                    r"\bwallet[s]?\b", r"\bwallet[-_]",
                    r"\baccount[s]?\b", r"\baccount[-_]",
                    r"\baddress[es]?\b", r"\baddress[-_]",
                    r"\bkey[s]?\b", r"\bkey[-_]",
                    r"\bsigner[s]?\b", r"\bsign(?:ing|er)?\b",
                    
                    # Wallet Types
                    r"\bhot[-_]wallet\b", r"\bcold[-_]wallet\b",
                    r"\bhardware[-_]wallet\b", r"\bsoftware[-_]wallet\b",
                    r"\bmobile[-_]wallet\b", r"\bweb[-_]wallet\b",
                    r"\bdesktop[-_]wallet\b", r"\bextension[-_]wallet\b",
                    r"\bmulti[-_]sig\b", r"\bmultisig\b",
                    
                    # Wallet Features
                    r"\btransaction[s]?\b", r"\btx[s]?\b",
                    r"\bsend\b", r"\breceive\b",
                    r"\btransfer[s]?\b", r"\bpayment[s]?\b",
                    r"\bbalance[s]?\b", r"\bhistory\b",
                    r"\bportfolio\b", r"\basset[s]?\b",
                    r"\btoken[-_]list\b", r"\btoken[-_]balance\b",
                    
                    # Security Features
                    r"\bencrypt(?:ion)?\b", r"\bdecrypt(?:ion)?\b",
                    r"\bhash(?:ing)?\b", r"\bsalt(?:ing)?\b",
                    r"\bsecure\b", r"\bprotect(?:ion)?\b",
                    r"\bbackup[s]?\b", r"\brecover[y]?\b",
                    r"\bsafe[ty]?\b", r"\bguard\b",
                    
                    # Key Management
                    r"\bprivate[-_]key\b", r"\bpublic[-_]key\b",
                    r"\bseed[-_]phrase\b", r"\bmnemonic\b",
                    r"\bkeystore\b", r"\bkeygen\b",
                    r"\bsigner\b", r"\bsigning\b",
                    r"\bkey[-_]management\b", r"\bkey[-_]store\b",
                    
                    # Specific Wallet Projects
                    r"petra[-_]wallet", r"abc[-_]wallet",
                    r"arculus[-_]wallet", r"msafe",
                    r"flipper", r"infinity[-_]wallet",
                    r"bitget[-_]wallet", r"blocto",
                    r"foxwallet", r"gem[-_]wallet",
                    r"math[-_]wallet", r"nightly",
                    r"martian", r"fewcha",
                    r"pontem", r"rise",
                    
                    # Additional Wallet Features
                    r"connect[-_]wallet", r"wallet[-_]connect",
                    r"disconnect[-_]wallet", r"wallet[-_]adapter",
                    r"wallet[-_]provider", r"wallet[-_]integration",
                    r"wallet[-_]service", r"wallet[-_]api",
                    r"wallet[-_]sdk", r"wallet[-_]library",
                    
                    # Transaction Features
                    r"\bgas[-_]fee[s]?\b", r"\bgas[-_]price\b",
                    r"\bgas[-_]limit\b", r"\bnonce\b",
                    r"\bblock[-_]height\b", r"\bconfirmation[s]?\b",
                    r"\bpending\b", r"\bcompleted\b",
                    r"\bfailed\b", r"\bsuccess\b",
                    
                    # Asset Management
                    r"\btoken[-_]management\b", r"\basset[-_]tracking\b",
                    r"\bportfolio[-_]view\b", r"\bbalance[-_]check\b",
                    r"\btoken[-_]list\b", r"\btoken[-_]metadata\b",
                    r"\btoken[-_]price\b", r"\btoken[-_]value\b",
                    
                    # Authentication
                    r"\bpassphrase\b", r"\bpin[-_]code\b",
                    r"\bbiometric[s]?\b", r"\bfingerprint\b",
                    r"\bface[-_]id\b", r"\btouch[-_]id\b",
                    r"\b2fa\b", r"\bmfa\b",
                    
                    # Network Features
                    r"\bnetwork[-_]fee[s]?\b", r"\bchain[-_]id\b",
                    r"\bnetwork[-_]switch\b", r"\bnetwork[-_]select\b",
                    r"\brpc[-_]url\b", r"\bnode[-_]url\b",
                    r"\bexplorer[-_]url\b", r"\bapi[-_]endpoint\b"
                ]),
                ('MEDIUM', [
                    r"\bwallet[-_]", r"\baccount[-_]",
                    r"\baddress[-_]", r"\bkey[-_]",
                    r"\btransaction[-_]", r"\btx[-_]",
                    r"\bsend[-_]", r"\breceive[-_]",
                    r"\btransfer[-_]", r"\bpayment[-_]",
                    r"\bbalance[-_]", r"\bhistory[-_]",
                    r"\bsecurity[-_]", r"\bsafe[-_]",
                    r"\bprotect[-_]", r"\bguard[-_]",
                    r"\bconnect[-_]", r"\bintegration[-_]",
                    r"\bprovider[-_]", r"\badapter[-_]",
                    r"\bsdk[-_]", r"\bapi[-_]",
                    r"\blibrary[-_]", r"\bservice[-_]",
                    
                    # Additional Medium Patterns
                    r"\btoken[-_]", r"\basset[-_]",
                    r"\bnetwork[-_]", r"\bchain[-_]",
                    r"\bblock[-_]", r"\btx[-_]",
                    r"\bgas[-_]", r"\bfee[-_]",
                    r"\bsign[-_]", r"\bverify[-_]",
                    r"\bauth[-_]", r"\bsecure[-_]",
                    r"\bbackup[-_]", r"\brestore[-_]",
                    r"\bimport[-_]", r"\bexport[-_]",
                    r"\bvalidate[-_]", r"\bcheck[-_]"
                ])
            ],
            negative_patterns=[
                r"test[-_]wallet",
                r"demo[-_]wallet",
                r"example[-_]wallet",
                r"sample[-_]wallet",
                r"learning[-_]purpose",
                r"practice[-_]",
                r"mock[-_]wallet",
                r"fake[-_]wallet",
                r"placeholder[-_]wallet",
                r"testing[-_]purpose",
                r"dummy[-_]wallet",
                r"temporary[-_]wallet"
            ],
            exclude_categories=['Infrastructure & Tools', 'Identity & Authentication']
        ) 
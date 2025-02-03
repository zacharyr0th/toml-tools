"""Security & Privacy category patterns and matching logic."""
from .base import BaseCategory

class SecurityCategory(BaseCategory):
    """Category for Security & Privacy projects."""
    
    def __init__(self):
        super().__init__(
            name="Security & Privacy",
            patterns=[
                ('STRONG', [
                    # Core Security Terms
                    r"\bsecurity\b", r"\bprivacy\b",
                    r"\bencrypt(?:ion)?\b", r"\bdecrypt(?:ion)?\b",
                    r"\bhash(?:ing)?\b", r"\bsalt(?:ing)?\b",
                    r"\bsecure\b", r"\bprotect(?:ion)?\b",
                    
                    # Security Features
                    r"\bfirewall\b", r"\bproxy\b",
                    r"\bvpn\b", r"\btunnel\b",
                    r"\bsandbox\b", r"\bcontainer\b",
                    r"\bisolat(?:e|ion)\b", r"\bquarantine\b",
                    
                    # Authentication & Authorization
                    r"\bauth(?:entication)?\b", r"\bauthoriz(?:ation)?\b",
                    r"\baccess[-_]control\b", r"\brbac\b",
                    r"\babac\b", r"\bpermission[s]?\b",
                    r"\brole[s]?\b", r"\bpolicy\b",
                    
                    # Cryptography
                    r"\bcrypto(?:graphy)?\b", r"\bcipher[s]?\b",
                    r"\bkey[s]?\b", r"\bsignature[s]?\b",
                    r"\bcertificate[s]?\b", r"\btls\b",
                    r"\bssl\b", r"\bpki\b",
                    
                    # Privacy Features
                    r"\banonymity\b", r"\banonymous\b",
                    r"\bpseudonym\b", r"\bprivate\b",
                    r"\bconfidential\b", r"\bsecret\b",
                    r"\bzero[-_]knowledge\b", r"\bzk[ps]?\b",
                    
                    # Blockchain Security
                    r"\bwallet[-_]security\b", r"\bsmart[-_]contract[-_]audit\b",
                    r"\bcontract[-_]security\b", r"\bsecurity[-_]audit\b",
                    r"\bvulnerability[-_]scan\b", r"\bpenetration[-_]test\b",
                    r"\bsecurity[-_]review\b", r"\bsecurity[-_]assessment\b",
                    
                    # Additional Security Features
                    r"\bmfa\b", r"\b2fa\b", r"\btwo[-_]factor\b",
                    r"\botp\b", r"\bone[-_]time[-_]password\b",
                    r"\bbiometric[s]?\b", r"\bfacial[-_]recognition\b",
                    r"\bfingerprint\b", r"\biris[-_]scan\b",
                    
                    # Security Operations
                    r"\bsoc\b", r"\bsecurity[-_]operations\b",
                    r"\bincident[-_]response\b", r"\bforensic[s]?\b",
                    r"\bmalware\b", r"\bvirus\b", r"\btrojan\b",
                    r"\bransomware\b", r"\bspyware\b",
                    
                    # Network Security
                    r"\bids\b", r"\bips\b", r"\bintrusion[-_]detection\b",
                    r"\bintrusion[-_]prevention\b", r"\bwaf\b",
                    r"\bddos\b", r"\bdos\b", r"\bbot[-_]protection\b",
                    
                    # Compliance & Standards
                    r"\bgdpr\b", r"\bhipaa\b", r"\bpci[-_]dss\b",
                    r"\biso27001\b", r"\bsox\b", r"\bcompliance\b",
                    r"\baudit[-_]log[s]?\b", r"\bactivity[-_]log[s]?\b"
                ]),
                ('MEDIUM', [
                    r"\bsecure[-_]", r"\bsecurity[-_]",
                    r"\bprivacy[-_]", r"\bprivate[-_]",
                    r"\bprotect[-_]", r"\bguard[-_]",
                    r"\bencrypt[-_]", r"\bdecrypt[-_]",
                    r"\bhash[-_]", r"\bsalt[-_]",
                    r"\baudit[-_]", r"\bverify[-_]",
                    r"\bvalidate[-_]", r"\bcheck[-_]",
                    r"\bmonitor[-_]", r"\bdetect[-_]",
                    r"\balert[-_]", r"\bnotify[-_]",
                    r"\bblock[-_]", r"\bfilter[-_]",
                    
                    # Additional Medium Patterns
                    r"\bscan[-_]", r"\banalyze[-_]",
                    r"\bprevent[-_]", r"\bmitigate[-_]",
                    r"\bthreshold[-_]", r"\blimit[-_]",
                    r"\bpolicy[-_]", r"\brule[-_]",
                    r"\bcontrol[-_]", r"\baccess[-_]",
                    r"\blog[-_]", r"\btrack[-_]",
                    r"\breport[-_]", r"\bmetric[-_]"
                ])
            ],
            negative_patterns=[
                r"test[-_]security",
                r"demo[-_]security",
                r"example[-_]security",
                r"sample[-_]security",
                r"learning[-_]purpose",
                r"practice[-_]",
                r"mock[-_]security",
                r"fake[-_]security",
                r"placeholder[-_]security",
                r"testing[-_]purpose"
            ],
            exclude_categories=['Infrastructure & Tools', 'Identity & Authentication']
        ) 
"""Identity & Authentication category patterns and matching logic."""
from .base import BaseCategory

class IdentityCategory(BaseCategory):
    """Category for Identity & Authentication projects."""
    
    def __init__(self):
        super().__init__(
            name="Identity & Authentication",
            patterns=[
                ('STRONG', [
                    # Core Identity Terms
                    r"\bidentity\b", r"\bauth(?:entication)?\b",
                    r"\bsso\b", r"\boauth\b", r"\boidc\b",
                    r"\bkyc\b", r"\bverif(?:y|ication)\b",
                    r"\bcredential[s]?\b", r"\bidentifier[s]?\b",
                    
                    # Authentication Methods
                    r"\bpassword[s]?\b", r"\btoken[s]?\b",
                    r"\bsession[s]?\b", r"\bcookie[s]?\b",
                    r"\bheader[s]?\b", r"\bbearer\b",
                    r"\bjwt\b", r"\bsaml\b",
                    
                    # Multi-Factor Auth
                    r"\bmfa\b", r"\b2fa\b",
                    r"\btwo[-_]factor\b", r"\bmulti[-_]factor\b",
                    r"\btotp\b", r"\bhotp\b",
                    r"\bauthenticator\b", r"\bfido\b",
                    
                    # Identity Providers
                    r"\bidp\b", r"\bidentity[-_]provider\b",
                    r"\bauth[-_]provider\b", r"\bauth[-_]service\b",
                    r"\bkeycloak\b", r"\bauth0\b",
                    r"\bokta\b", r"\bonelogin\b",
                    
                    # Access Control
                    r"\baccess[-_]control\b", r"\brbac\b",
                    r"\babac\b", r"\bpermission[s]?\b",
                    r"\brole[s]?\b", r"\bpolicy\b",
                    r"\brule[s]?\b", r"\bscope[s]?\b",
                    
                    # Blockchain Identity
                    r"\bwallet[-_]auth\b", r"\bwallet[-_]connect\b",
                    r"\bsign(?:er|ing)\b", r"\bsignature[s]?\b",
                    r"\bprivate[-_]key\b", r"\bpublic[-_]key\b",
                    r"\baddress[-_]verif\b", r"\bproof[-_]of[-_]"
                ]),
                ('MEDIUM', [
                    r"\bauth[-_]", r"\bidentity[-_]",
                    r"\blogin[-_]", r"\bsignin[-_]",
                    r"\bsignup[-_]", r"\bregister[-_]",
                    r"\bverify[-_]", r"\bvalidate[-_]",
                    r"\bcheck[-_]", r"\bsecure[-_]",
                    r"\bprotect[-_]", r"\bguard[-_]",
                    r"\baccess[-_]", r"\bpermission[-_]",
                    r"\brole[-_]", r"\buser[-_]",
                    r"\baccount[-_]", r"\bprofile[-_]",
                    r"\bsession[-_]", r"\btoken[-_]",
                    r"\bcookie[-_]", r"\bcredential[-_]",
                    r"\bpassword[-_]", r"\bsecret[-_]"
                ])
            ],
            negative_patterns=[
                r"test[-_]auth",
                r"demo[-_]auth",
                r"example[-_]auth",
                r"sample[-_]auth",
                r"learning[-_]purpose",
                r"practice[-_]"
            ],
            exclude_categories=['Infrastructure & Tools']
        ) 
"""Social & Community category patterns and matching logic."""
from .base import BaseCategory

class SocialCategory(BaseCategory):
    """Category for Social & Community projects."""
    
    def __init__(self):
        super().__init__(
            name="Social & Community",
            patterns=[
                ('STRONG', [
                    # Core Social Features
                    r"\bsocial[-_]network\b", r"\bsocial[-_]media\b",
                    r"\bcommunity[-_]platform\b", r"\bcommunity[-_]hub\b",
                    r"\bforum[s]?\b", r"\bchat\b", r"\bmessaging\b",
                    r"\bprofile[s]?\b", r"\buser[-_]profile\b",
                    r"\bfeed[s]?\b", r"\btimeline\b", r"\bstream\b",
                    
                    # Social Actions
                    r"\bpost[s]?\b", r"\bcomment[s]?\b",
                    r"\blike[s]?\b", r"\breact(?:ion[s]?)?\b",
                    r"\bshare[s]?\b", r"\brepost[s]?\b",
                    r"\bfollow(?:er[s]?)?\b", r"\bfriend[s]?\b",
                    r"\bconnect(?:ion[s]?)?\b", r"\bnetwork[s]?\b",
                    
                    # Community Features
                    r"\bgroup[s]?\b", r"\bchannel[s]?\b",
                    r"\bevent[s]?\b", r"\bmeet(?:ing|up)[s]?\b",
                    r"\bspace[s]?\b", r"\broom[s]?\b",
                    r"\bcommunity[-_]", r"\bsocial[-_]",
                    
                    # Specific Social Projects
                    r"chingari", r"donk", r"acornquest",
                    r"buidlerdao", r"cafeteria", r"kade",
                    r"metaschool", r"townesquare", r"mereo",
                    r"rndm", r"netsepio", r"springx",
                    
                    # Additional Social Features
                    r"\bmention[s]?\b", r"\btag[s]?\b",
                    r"\bhashtag[s]?\b", r"\btrend(?:ing)?\b",
                    r"\bviral\b", r"\bpopular\b",
                    r"\binfluencer[s]?\b", r"\bcreator[s]?\b",
                    
                    # Content Types
                    r"\bstory(?:ies)?\b", r"\breel[s]?\b",
                    r"\bvideo[-_]post[s]?\b", r"\blive[-_]stream\b",
                    r"\bpoll[s]?\b", r"\bsurvey[s]?\b",
                    r"\bquiz(?:zes)?\b", r"\bcontest[s]?\b",
                    
                    # Engagement Features
                    r"\bnotification[s]?\b", r"\balert[s]?\b",
                    r"\bmessage[s]?\b", r"\bdm[s]?\b",
                    r"\binbox\b", r"\bchat[-_]room\b",
                    r"\bthread[s]?\b", r"\bdiscussion[s]?\b",
                    
                    # Community Management
                    r"\bmoderator[s]?\b", r"\bmod[s]?\b",
                    r"\badmin[s]?\b", r"\bban\b",
                    r"\breport[-_]abuse\b", r"\bflag[-_]content\b",
                    r"\bguideline[s]?\b", r"\brule[s]?\b",
                    
                    # Social Analytics
                    r"\bengagement[-_]rate\b", r"\bimpression[s]?\b",
                    r"\breach\b", r"\bmetric[s]?\b",
                    r"\banalytics\b", r"\binsight[s]?\b",
                    r"\bperformance\b", r"\bstatistic[s]?\b"
                ]),
                ('MEDIUM', [
                    r"\buser[s]?\b", r"\bmember[s]?\b",
                    r"\baccount[s]?\b", r"\bprofile[s]?\b",
                    r"\bstatus\b", r"\bupdate[s]?\b",
                    r"\bactivity\b", r"\baction[s]?\b",
                    r"\binteraction[s]?\b", r"\bengagement\b",
                    r"\bmetric[s]?\b", r"\banalytics\b",
                    r"\btrend[s]?\b", r"\bpopular\b",
                    r"\bfeatured\b", r"\bhighlight[s]?\b",
                    
                    # Additional Medium Patterns
                    r"\bshare[-_]", r"\bpost[-_]",
                    r"\bcomment[-_]", r"\breply[-_]",
                    r"\bfollow[-_]", r"\bconnect[-_]",
                    r"\bgroup[-_]", r"\bchannel[-_]",
                    r"\bevent[-_]", r"\bmeet[-_]",
                    r"\bnotify[-_]", r"\balert[-_]",
                    r"\bmessage[-_]", r"\bchat[-_]",
                    r"\bmoderate[-_]", r"\bmanage[-_]",
                    r"\breport[-_]", r"\banalyze[-_]"
                ])
            ],
            negative_patterns=[
                r"test[-_]social",
                r"demo[-_]social",
                r"example[-_]social",
                r"sample[-_]community",
                r"learning[-_]purpose",
                r"practice[-_]",
                r"mock[-_]social",
                r"fake[-_]community",
                r"placeholder[-_]social",
                r"testing[-_]purpose"
            ],
            exclude_categories=['Infrastructure & Tools']
        ) 
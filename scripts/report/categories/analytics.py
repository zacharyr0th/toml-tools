"""Data & Analytics category patterns and matching logic."""
from .base import BaseCategory

class AnalyticsCategory(BaseCategory):
    """Category for Data & Analytics projects."""
    
    def __init__(self):
        super().__init__(
            name="Data & Analytics",
            patterns=[
                ('STRONG', [
                    # Core Analytics Terms
                    r"\banalytics\b", r"\banalysis\b",
                    r"\bdata[-_]", r"\bmetrics?\b",
                    r"\bstatistics?\b", r"\binsights?\b",
                    r"\breports?\b", r"\bdashboards?\b",
                    
                    # Data Processing
                    r"\betl\b", r"\bextract\b",
                    r"\btransform\b", r"\bload\b",
                    r"\bpipeline[s]?\b", r"\bprocessing\b",
                    r"\bstream(?:ing)?\b", r"\bbatch\b",
                    
                    # Data Storage
                    r"\bdatabase[s]?\b", r"\bdb\b",
                    r"\bwarehouse\b", r"\blake\b",
                    r"\bstorage\b", r"\brepository\b",
                    r"\bindex(?:er|ing)?\b", r"\bcache\b",
                    
                    # Data Types
                    r"\btime[-_]series\b", r"\bevent[s]?\b",
                    r"\blog[s]?\b", r"\btrace[s]?\b",
                    r"\bmetric[s]?\b", r"\bkpi[s]?\b",
                    r"\bindicator[s]?\b", r"\bmeasure[s]?\b",
                    
                    # Analysis Types
                    r"\bforecasting\b", r"\bprediction\b",
                    r"\bregression\b", r"\bclassification\b",
                    r"\bclustering\b", r"\bsegmentation\b",
                    r"\banomaly[-_]detection\b", r"\boutlier[s]?\b",
                    
                    # Blockchain Analytics
                    r"\bblock[-_]explorer\b", r"\btransaction[-_]",
                    r"\bchain[-_]data\b", r"\bchain[-_]analytics\b",
                    r"\bwallet[-_]tracking\b", r"\baddress[-_]",
                    r"\btoken[-_]analytics\b", r"\bdefi[-_]analytics\b"
                ]),
                ('MEDIUM', [
                    r"\bdata\b", r"\banalytics?\b",
                    r"\bmetric[s]?\b", r"\breport[s]?\b",
                    r"\bmonitor[s]?\b", r"\btrack[s]?\b",
                    r"\blog[s]?\b", r"\binsight[s]?\b",
                    r"\bvisualize\b", r"\bdisplay\b",
                    r"\bchart\b", r"\bgraph\b",
                    r"\bplot\b", r"\bquery\b",
                    r"\bsearch\b", r"\bfilter\b",
                    r"\bsort\b", r"\bgroup\b",
                    r"\baggregate\b", r"\bprocess\b",
                    r"\btransform\b", r"\bclean\b",
                    r"\bvalidate\b", r"\bverify\b",
                    r"\bcheck\b", r"\banalyze\b",
                    r"\bpredict\b", r"\bforecast\b"
                ])
            ],
            negative_patterns=[
                r"test[-_]data",
                r"demo[-_]data",
                r"example[-_]data",
                r"sample[-_]data",
                r"learning[-_]purpose",
                r"practice[-_]"
            ],
            exclude_categories=['Infrastructure & Tools']
        ) 
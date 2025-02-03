"""Education category patterns and matching logic."""
from .base import BaseCategory

class EducationCategory(BaseCategory):
    """Category for Education projects."""
    
    def __init__(self):
        super().__init__(
            name="Education",
            patterns=[
                ('STRONG', [
                    # Core Education Terms
                    r"\beducation\b", r"\blearning\b",
                    r"\bteaching\b", r"\btraining\b",
                    r"\bcourse[s]?\b", r"\bclass(?:es)?\b",
                    r"\blesson[s]?\b", r"\btutorial[s]?\b",
                    r"\bbootcamp[s]?\b", r"\blearn[-_]",
                    r"\btutorial[-_]", r"\bhello[-_]aptos\b",
                    
                    # Educational Content
                    r"\bcurriculum\b", r"\bsyllabus\b",
                    r"\bmodule[s]?\b", r"\bchapter[s]?\b",
                    r"\bsection[s]?\b", r"\bunit[s]?\b",
                    r"\blecture[s]?\b", r"\bworkshop[s]?\b",
                    
                    # Learning Materials
                    r"\bguide[s]?\b", r"\bmanual[s]?\b",
                    r"\bdocumentation\b", r"\bdocs\b",
                    r"\bexample[s]?\b", r"\bsample[s]?\b",
                    r"\btemplate[s]?\b", r"\bstarter[s]?\b",
                    r"\bcreate[-_]aptos[-_]dapp\b",
                    
                    # Assessment
                    r"\bquiz(?:zes)?\b", r"\btest[s]?\b",
                    r"\bexam[s]?\b", r"\bassessment[s]?\b",
                    r"\bexercise[s]?\b", r"\bpractice[s]?\b",
                    r"\bchallenge[s]?\b", r"\bproblem[s]?\b",
                    
                    # Blockchain Education
                    r"\bblockchain[-_]101\b", r"\bcrypto[-_]basics\b",
                    r"\bmove[-_]tutorial\b", r"\baptos[-_]learn\b",
                    r"\bsmart[-_]contract[-_]course\b", r"\bweb3[-_]education\b",
                    r"\bdefi[-_]learning\b", r"\bnft[-_]basics\b",
                    r"\bmovegochi\b", r"\baptogotchi\b",
                    
                    # Specific Educational Projects
                    r"movegochi", r"aptogotchi",
                    r"create[-_]aptos[-_]dapp",
                    r"hello[-_]aptos",
                    r"learn[-_]aptos",
                    r"learn[-_]move",
                    r"aptos[-_]tutorial",
                    r"move[-_]tutorial",
                    r"aptos[-_]bootcamp",
                    r"move[-_]bootcamp"
                ]),
                ('MEDIUM', [
                    r"\blearn\b", r"\btutorial\b",
                    r"\bguide\b", r"\bexample\b",
                    r"\bdemo\b", r"\bsample\b",
                    r"\bstarter\b", r"\btemplate\b",
                    r"\bworkshop\b", r"\bbootcamp\b",
                    r"\bcourse\b", r"\bclass\b",
                    r"\blesson\b", r"\bmodule\b",
                    r"\bexercise\b", r"\bpractice\b"
                ])
            ],
            negative_patterns=[
                r"test[-_]only",
                r"demo[-_]only",
                r"example[-_]only",
                r"sample[-_]only"
            ],
            exclude_categories=['Infrastructure & Tools']
        ) 
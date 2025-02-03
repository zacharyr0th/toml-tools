"""Gaming & Entertainment category patterns and matching logic."""
from .base import BaseCategory
from ..config.pattern_weights import STRICT_THRESHOLD

class GamingCategory(BaseCategory):
    """Category for Gaming & Entertainment projects."""
    
    def __init__(self):
        super().__init__(
            name="Gaming & Entertainment",
            patterns=[
                ('STRONG', [
                    # Core Gaming Terms
                    r"\bgame[s]?\b", r"\bgaming\b",
                    r"\bplay\b", r"\bplayer[s]?\b",
                    r"\barcade\b", r"\bcasino\b",
                    r"\bgamefi\b", r"\bp2e\b",
                    r"\bplay[-_]to[-_]earn\b",
                    
                    # Game Types
                    r"\brpg\b", r"\bmmorpg\b",
                    r"\bpvp\b", r"\bpve\b",
                    r"\bstrategy\b", r"\bpuzzle\b",
                    r"\bradio\b", r"\bmusic\b",
                    r"\bdice\b", r"\bpoker\b",
                    r"\bcard[-_]game\b", r"\bboard[-_]game\b",
                    r"\brace\b", r"\bracing\b",
                    r"\bsport[s]?\b", r"\bsoccer\b",
                    r"\bfootball\b", r"\bbasketball\b",
                    
                    # Game Features
                    r"\bscore[s]?\b", r"\bleaderboard\b",
                    r"\brank[s]?\b", r"\branking\b",
                    r"\blevel[s]?\b", r"\bleveling\b",
                    r"\bquest[s]?\b", r"\bmission[s]?\b",
                    r"\breward[s]?\b", r"\bachievement[s]?\b",
                    r"\binventory\b", r"\bitem[s]?\b",
                    r"\bweapon[s]?\b", r"\barmor\b",
                    r"\bcharacter[s]?\b", r"\bavatar[s]?\b",
                    r"\bpet[s]?\b", r"\bcreature[s]?\b",
                    
                    # Specific Game Projects
                    r"aptogotchi", r"movegotchi",
                    r"wolf[-_]game", r"dice[-_]casino",
                    r"rock[-_]paper[-_]scissors",
                    r"tic[-_]tac[-_]toe",
                    r"chess", r"checkers",
                    r"blackjack", r"poker",
                    r"slot[-_]machine",
                    
                    # Game Infrastructure
                    r"\bgame[-_]engine\b", r"\bgame[-_]server\b",
                    r"\bgame[-_]client\b", r"\bgame[-_]core\b",
                    r"\bgame[-_]assets\b", r"\bgame[-_]items\b",
                    r"\bgame[-_]token[s]?\b", r"\bgame[-_]coin[s]?\b",
                    r"\bgame[-_]nft[s]?\b", r"\bgame[-_]marketplace\b",
                    
                    # Metaverse
                    r"\bmetaverse\b", r"\bvirtual[-_]world\b",
                    r"\bvirtual[-_]reality\b", r"\bvr[-_]",
                    r"\baugmented[-_]reality\b", r"\bar[-_]"
                ]),
                ('MEDIUM', [
                    r"\bplay[-_]", r"\bgame[-_]",
                    r"\bscore[-_]", r"\blevel[-_]",
                    r"\bquest[-_]", r"\breward[-_]",
                    r"\bitem[-_]", r"\bcharacter[-_]",
                    r"\bvirtual[-_]", r"\bdigital[-_]",
                    r"\binteractive[-_]", r"\bimmersive[-_]",
                    r"\bentertainment[-_]", r"\bfun[-_]"
                ])
            ],
            negative_patterns=[
                r"test[-_]game",
                r"demo[-_]game",
                r"example[-_]game",
                r"sample[-_]game",
                r"learning[-_]purpose",
                r"practice[-_]"
            ],
            exclude_categories=['Infrastructure & Tools'],
            threshold=STRICT_THRESHOLD
        ) 
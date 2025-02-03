"""Infrastructure & Tools category patterns and matching logic."""
from .base import BaseCategory

class InfrastructureCategory(BaseCategory):
    """Category for Infrastructure & Tools projects."""
    
    def __init__(self):
        super().__init__(
            name="Infrastructure & Tools",
            patterns=[
                ('STRONG', [
                    # Core infrastructure
                    r"\bnode[-_]", r"\bvalidator[-_]", r"\binfrastructure[-_]",
                    r"\bframework[-_]", r"\bprotocol[-_]", r"\bnetwork[-_]",
                    r"\bsdk[-_]", r"\bapi[-_]", r"\bcli[-_]", r"\btoolkit[-_]",
                    r"\bapi[s]?\b", r"\brest[-_]api\b", r"\bgraphql[-_]api\b",
                    r"\bwormhole\b", r"\bwormhole[-_]",
                    r"\bbridge[-_]", r"\brelayer[-_]",
                    r"\bindexer[-_]", r"\bexplorer[-_]",
                    
                    # Development tools
                    r"\bcompiler[-_]", r"\bdeployer[-_]", r"\bdebugger[-_]",
                    r"\bmonitor[-_]", r"\banalyzer[-_]", r"\bexplorer[-_]",
                    r"\blibrary[-_]", r"\bpackage[-_]", r"\bmodule[-_]",
                    r"\bboilerplate\b", r"\btemplate\b", r"\bstarter[-_]kit\b",
                    r"\bscaffold\b", r"\bexample[s]?\b", r"\bdemo[s]?\b",
                    
                    # Move/Aptos specific
                    r"\bmove[-_]lang\b", r"\bmove[-_]compiler\b",
                    r"\bmove[-_]framework\b", r"\bmove[-_]stdlib\b",
                    r"\baptos[-_]framework\b", r"\baptos[-_]sdk\b",
                    r"\baptos[-_]cli\b", r"\baptos[-_]core\b",
                    r"\baptos[-_]node\b", r"\baptos[-_]validator\b",
                    r"aptos[-_]core", r"aptos[-_]labs",
                    r"aptos[-_]client", r"aptos[-_]sdk",
                    r"aptos[-_]api", r"aptos[-_]indexer",
                    
                    # Common tool types
                    r"[-_]indexer\b", r"[-_]explorer\b",
                    r"[-_]monitor\b", r"[-_]dashboard\b",
                    r"[-_]scanner\b", r"[-_]tracker\b",
                    r"[-_]adapter\b", r"[-_]provider\b",
                    r"[-_]service\b", r"[-_]backend\b",
                    r"[-_]frontend\b", r"[-_]interface\b",
                    r"[-_]api\b", r"api[-_]",
                    
                    # Additional Infrastructure Projects
                    r"apscan", r"aptstats",
                    r"blockeden", r"blockpi",
                    r"fewcha", r"module[-_]labs",
                    r"mokshya[-_]protocol", r"switchboard",
                    r"hashkey[-_]did", r"kycdao",
                    r"nongeek(?:dao)?", r"pontem[-_]network",
                    r"wormhole[-_]bridge", r"wormhole[-_]network",
                    r"layerzero", r"chainlink",
                    r"switchboard[-_]", r"oracle[-_]",
                    
                    # Development Features
                    r"\btest[-_]framework\b", r"\btest[-_]runner\b",
                    r"\bci[-_]cd\b", r"\bpipeline[s]?\b",
                    r"\bdocker\b", r"\bkubernetes\b",
                    r"\bhelm\b", r"\bterraform\b",
                    r"\bansible\b", r"\bjenkins\b",
                    r"\bgithub[-_]action[s]?\b"
                ]),
                ('MEDIUM', [
                    # Development features
                    r"\bintegration[-_]", r"\binterface[-_]",
                    r"\bwrapper[-_]", r"\bbridge[-_]",
                    r"\bclient[-_]", r"\bserver[-_]",
                    r"\blog(?:ging|ger)?[-_]", r"\bmetric[-_]",
                    r"\btool[-_]", r"\butil(?:s|ity|ities)?[-_]",
                    r"\bhelper[-_]", r"\bscript[-_]",
                    r"\bconfig[-_]", r"\bsetup[-_]", r"\bbuild[-_]",
                    r"\bapi[-_]", r"\bendpoint[-_]", r"\bservice[-_]",
                    r"\bsdk[-_]", r"\bcli[-_]", r"\bframework[-_]",
                    r"\bprotocol[-_]", r"\bnetwork[-_]", r"\bbridge[-_]",
                    
                    # Move/Aptos specific
                    r"\bmove[-_]module\b", r"\bmove[-_]contract\b",
                    r"\bmove[-_]resource\b", r"\bmove[-_]capability\b",
                    r"\bmove[-_]signer\b", r"\bmove[-_]account\b",
                    r"\baptos[-_]module\b", r"\baptos[-_]contract\b"
                ])
            ],
            negative_patterns=[
                r"test[-_]api",
                r"demo[-_]api",
                r"example[-_]api",
                r"sample[-_]api",
                r"learning[-_]purpose",
                r"practice[-_]"
            ],
            exclude_categories=['Smart Contracts & Core']
        ) 
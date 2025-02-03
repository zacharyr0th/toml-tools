import re

# Simplified pattern weights
PATTERN_WEIGHTS = {
    'STRONG': 3.0,
    'MEDIUM': 2.0,
    'WEAK': 1.0
}

CATEGORIES = {
    "DeFi & Financial": {
        'patterns': [
            ('STRONG', [
                # Core DeFi terms
                r"\b(?:de)?fi\b", r"defi[-_]", r"_(?:de)?fi\b",
                r"\bvault[s]?\b", r"\byield[s]?\b", r"\byielding\b",
                r"\bamm\b", r"\bperpetual[s]?\b", r"\bperp[s]?\b",
                r"\bswap\b", r"\bswaps\b", r"\bswapper\b", r"\bswapping\b",
                r"\bstaking\b", r"\bstake[s]?\b", r"\bstaked\b",
                r"\bliquid(?:ity|ation)\b", r"\blp[s]?\b", r"\bpool[s]?\b",
                r"\bfarm(?:ing)?\b", r"\bharvest(?:er|ing)?\b",
                r"\blend(?:ing)?\b", r"\bloan[s]?\b", r"\bborrow(?:ing)?\b",
                r"\bcollateral\b", r"\bmargin\b", r"\bleverage\b",
                
                # Protocol names
                r"\baave\b", r"\bcompound\b", r"\bfrax\b", r"\bcurve\b",
                r"\buniswap\b", r"\bsushiswap\b", r"\bpancakeswap\b",
                r"\bliquity\b", r"\balchemix\b", r"\bsynthetix\b",
                r"\bribbon\b", r"\bconvex\b", r"\bbalancer\b",
                
                # Protocol types
                r"\blending[-_]protocol\b", r"\bliquid[-_]staking\b",
                r"\bstaking[-_]protocol\b", r"\bfinance\b", r"\bfinancial\b",
                r"\bmonetary\b", r"\bvetoken[s]?\b", r"\bbridge\b",
                
                # Specific features
                r"\bflash[-_]loan\b", r"\bflash[-_]mint\b",
                r"\bliquidity[-_]mining\b", r"\bliquidity[-_]provision\b",
                r"\bstaking[-_]rewards\b", r"\brebase[-_]token\b",
                r"\belastic[-_]supply\b", r"\bvoting[-_]escrow\b",
                r"\btoken[-_]bridge\b", r"\btoken[-_]swap\b",
                r"\btoken[-_]sale\b", r"\btoken[-_]launch\b",
                r"\btoken[-_]vesting\b", r"\btoken[-_]lock\b",
                
                # Move/Aptos specific
                r"\bcoin\b", r"\bcoins\b", r"\btoken\b", r"\btokens\b",
                r"\bliquid[-_]staking\b", r"\bstaking[-_]pool\b",
                r"\byield[-_]farming\b", r"\byield[-_]optimizer\b",
                r"\bswap[-_]pool\b", r"\bamm[-_]pool\b",
                r"\blending[-_]pool\b", r"\bstable[-_]coin\b",
                r"\bstable[-_]swap\b", r"\bliquidity[-_]pool\b"
            ]),
            ('MEDIUM', [
                # Financial terms
                r"\btrade[rs]?\b", r"\btrading\b", r"\bexchange[s]?\b",
                r"\bmarket[s]?\b", r"\bprice[s]?\b", r"\bfee[s]?\b",
                r"\bwallet[s]?\b", r"\basset[s]?\b", r"\bportfolio\b",
                r"\binvestment[s]?\b", r"\btreasury\b", r"\bvault[s]?\b",
                
                # Protocol features
                r"\binterest[-_]rate\b", r"\binterest[-_]bearing\b",
                r"\bmarket[-_]maker\b", r"\bimpermanent[-_]loss\b",
                r"\bslippage\b", r"\bgas[-_]optimization\b",
                r"\bmulti[-_]sig\b", r"\btime[-_]lock\b",
                r"\bprice[-_]impact\b", r"\bfee[-_]sharing\b",
                
                # Move/Aptos specific
                r"\bmodule\b", r"\bresource\b", r"\bcapability\b",
                r"\bsigner\b", r"\baccount\b", r"\baddress\b",
                r"\btransaction\b", r"\bscript\b", r"\bentry\b",
                r"\bstruct\b", r"\bevent\b", r"\berror\b"
            ]),
            ('WEAK', [
                # Generic blockchain terms
                r"\bblockchain\b", r"\bcrypto\b", r"\bweb3\b",
                r"\bdecentralized\b", r"\bdistributed\b",
                r"\bconsensus\b", r"\bvalidator[s]?\b",
                r"\bsmart[-_]contract[s]?\b", r"\bcontract[s]?\b",
                
                # Move/Aptos ecosystem
                r"\bmove[-_]lang\b", r"\baptos\b", r"\bsui\b",
                r"\bmove[-_]module\b", r"\bmove[-_]contract\b",
                r"\baptos[-_]framework\b", r"\baptos[-_]token\b",
                r"\baptos[-_]coin\b", r"\baptos[-_]std\b"
            ])
        ],
        'negative_patterns': [
            r"\btest[-_]token[s]?\b", r"\bdummy[-_]token[s]?\b",
            r"\bsample[-_]token[s]?\b", r"\btoken[-_]test[s]?\b",
            r"\bexample[-_]", r"\bdemo[-_]", r"\btest[-_]",
            r"\bmock[-_]", r"\bfake[-_]"
        ],
        'exclude_categories': ['Gaming & Entertainment'],
        'threshold': 2.0
    },

    "NFTs & Digital Assets": {
        'patterns': [
            ('STRONG', [
                r"\bnft[s]?\b", r"[-_]nft[s]?\b", r"\bnft[-_]",
                r"\berc[-\s]?721\b", r"\berc[-\s]?1155\b",
                r"\bopensea\b", r"\brarible\b", r"\bnifty\b",
                r"\bcollectible[s]?\b", r"\bdigital[-_]collectible[s]?\b",
                r"\bnon[-_]fungible\b", r"\btokenid\b",
                r"\bseaport\b", r"\blooksrare\b", r"\bx2y2\b", r"\bmagic[-_]eden\b",
                r"\bblur\b", r"\bfoundation\b", r"\bsuperrare\b", r"\bmanifold\b",
                r"\bartblocks\b", r"\bzora\b", r"\bcatalyst\b", r"\bknown[-_]origin\b",
                r"\bnft[-_]marketplace\b", r"\bnft[-_]auction\b", r"\bnft[-_]bridge\b",
                r"\btoken[-_]gating\b", r"\bsoulbound\b", r"\bpoap[s]?\b",
                r"\berc[-_]4907\b", r"\berc[-_]5643\b", r"\berc[-_]2981\b",
                r"\bpfp[s]?\b", r"\bavatar[-_]generator\b", r"\bmetadata[-_]standard\b",
            ]),
            ('MEDIUM', [
                r"\bmint(?:ing|er)?\b", r"\bmint[-_]",
                r"\broyalt(?:y|ies)\b", r"\bmarket[-_]?place\b",
                r"\bauction[s]?\b", r"\bgallery\b", r"\bexhibition\b",
                r"\bart[-_]", r"\bartist[s]?\b", r"\bcreator[s]?\b",
                r"\btoken[-_]uri\b", r"\btoken[-_]metadata\b",
                r"\btoken[-_]standard\b", r"\btoken[-_]collection\b",
                r"\bdrop[s]?\b", r"\bwhitelist\b", r"\ballowlist\b", r"\bpresale\b",
                r"\brarity\b", r"\btrading[-_]volume\b", r"\bfloor[-_]price\b",
                r"\bsweep\b", r"\bsnipe\b", r"\bbid[s]?\b", r"\breserve[-_]price\b",
                r"\bcollection[-_]stats\b", r"\btoken[-_]gate[d]?\b",
                r"\bmetadata[-_]api\b", r"\brender\b", r"\bgenerate\b",
                r"\btoken[-_]bound\b", r"\bsbt[s]?\b", r"\bpermanent[-_]token\b",
                r"\blazy[-_]mint\b", r"\bbatch[-_]mint\b", r"\bpremint\b",
            ]),
            ('WEAK', [
                r"\bmetadata\b", r"\basset[s]?\b", r"\btoken[s]?\b",
                r"\bsale[s]?\b", r"\blisting[s]?\b", r"\btrade[s]?\b",
                r"\bcollection\b", r"\bdigital[-_]art\b", r"\bvirtual[-_]asset[s]?\b",
                r"\btoken[-_]holder[s]?\b", r"\btoken[-_]owner[s]?\b",
                r"\btoken[-_]transfer\b", r"\btoken[-_]approval\b",
                r"\btoken[-_]balance\b", r"\btoken[-_]supply\b",
                r"\btoken[-_]burn\b", r"\btoken[-_]lock\b",
                r"\btoken[-_]vault\b", r"\btoken[-_]bridge\b",
                r"\btoken[-_]swap\b", r"\btoken[-_]sale\b",
                r"\btoken[-_]distribution\b", r"\btoken[-_]economics\b",
                r"\btoken[-_]utility\b", r"\btoken[-_]standard\b",
                r"\btoken[-_]interface\b", r"\btoken[-_]factory\b",
            ])
        ],
        'negative_patterns': [
            r"\btest[-_]token[s]?\b", r"\bdummy[-_]token[s]?\b",
            r"\bsample[-_]token[s]?\b", r"\btoken[-_]test[s]?\b",
            r"\btest[-_]nft\b", r"\bdemo[-_]nft\b",
            r"\bsample[-_]nft\b", r"\bexample[-_]nft\b",
            r"\bmock[-_]nft\b", r"\bfake[-_]nft\b",
            r"\btest[-_]collection\b", r"\bdemo[-_]collection\b",
            r"\bsample[-_]metadata\b", r"\bexample[-_]metadata\b",
        ],
        'exclude_categories': [],
        'threshold': 1.0
    },

    "Gaming & Entertainment": {
        'patterns': [
            ('STRONG', [
                r"\bgame\b", r"\bplay\b", r"\bgaming\b", r"\barcade\b",
                r"\bmetaverse\b", r"\bvirtual[-\s]world\b",
                r"\bagar\b", r"\bstickman\b", r"\bclicker\b", r"\bcoin[-\s]?flip\b",
                r"\brock[-\s]?paper[-\s]?scissors\b", r"\bchess\b", r"\bpoker\b",
                r"\bslots?\b", r"\bcasino\b", r"\bbet(?:ting)?\b",
                r"\bgamefi\b", r"\bp2e\b", r"\bplay[-_]to[-_]earn\b",
                r"\bmmo(?:rpg)?\b", r"\brpg\b", r"\bpvp\b", r"\bpve\b",
                r"\braid[s]?\b", r"\bdungeon[s]?\b", r"\barena\b",
                r"\bstrategy[-_]game\b", r"\bcard[-_]game\b", r"\bboard[-_]game\b",
                r"\bgame[-_]engine\b", r"\bgame[-_]asset[s]?\b",
                r"\bgame[-_]mechanics\b", r"\bgame[-_]economy\b",
                r"\bgame[-_]token[s]?\b", r"\bgame[-_]nft[s]?\b",
                r"\bgame[-_]marketplace\b", r"\bgame[-_]studio\b",
                r"\bsandbox[-_]game\b", r"\bdecentraland\b", r"\bgala[-_]games\b",
                r"\byield[-_]guild\b", r"\bguild[-_]fi\b",
            ]),
            ('MEDIUM', [
                r"\bcharacter\b", r"\bavatar\b", r"\bitem\b", r"\binventory\b",
                r"\bquest\b", r"\bmission\b", r"\blevel\b", r"\bscore\b",
                r"\bplayer[s]?\b", r"\bleaderboard\b", r"\bachievement[s]?\b",
                r"\breward[s]?\b", r"\bpower[-_]up[s]?\b", r"\bboost[s]?\b",
                r"\bweapon[s]?\b", r"\barmor\b", r"\bequipment\b",
                r"\bspell[s]?\b", r"\bskill[s]?\b", r"\bability\b",
                r"\bcraft(?:ing)?\b", r"\bresource[s]?\b", r"\bloot\b",
                r"\bbattle\b", r"\bcombat\b", r"\bfight(?:ing)?\b",
                r"\bteam[s]?\b", r"\bguild[s]?\b", r"\bclan[s]?\b",
                r"\btournament[s]?\b", r"\bevent[s]?\b", r"\bseason[s]?\b",
            ]),
            ('WEAK', [
                r"\baptogotchi\b", r"\baxie\b", r"\bpixel\b",
                r"\bgambl(?:e|ing)\b", r"\bcasino\b", r"\bbet(?:ting)?\b", r"\blotter(?:y|ies)\b",
                r"\bprediction[-\s]?market\b", r"\bsports[-\s]?betting\b",
                r"\bmetaverse\b", r"\bvirtual[-\s]?world\b", r"\bvr[-\s]?world\b",
                r"\bdigital[-\s]?realm\b", r"\bvirtual[-\s]?land\b", r"\bparcel\b",
                r"\bentertain(?:ment)?\b", r"\bmedia[-\s]?platform\b", r"\bcontent[-\s]?hub\b",
                r"\bstream(?:ing)?\b", r"\bvideo[-\s]?platform\b",
                r"\bplay[-_]", r"\bgame[-_]", r"\bgaming[-_]",
                r"\barcade[-_]", r"\bcasino[-_]", r"\bbet[-_]",
                r"\bvirtual[-_]", r"\bdigital[-_]", r"\bonline[-_]",
                r"\binteractive[-_]", r"\bimmersive[-_]", r"\bplayable[-_]",
                r"\bmulti[-_]player\b", r"\bsingle[-_]player\b",
                r"\bcross[-_]platform\b", r"\bcross[-_]chain\b",
                r"\bgame[-_]design\b", r"\bgame[-_]dev\b",
                r"\bgame[-_]logic\b", r"\bgame[-_]state\b",
                r"\bgame[-_]server\b", r"\bgame[-_]client\b",
                r"\bgame[-_]api\b", r"\bgame[-_]sdk\b",
            ])
        ],
        'negative_patterns': [
            r"\btest[-_]game\b", r"\bdemo[-_]game\b",
            r"\bsample[-_]game\b", r"\bexample[-_]game\b",
            r"\bmock[-_]game\b", r"\bfake[-_]game\b",
            r"\btest[-_]play\b", r"\bdemo[-_]play\b",
            r"\bsample[-_]player\b", r"\bexample[-_]player\b",
            r"\btest[-_]collection\b", r"\bdemo[-_]collection\b",
            r"\bsample[-_]metadata\b", r"\bexample[-_]metadata\b",
        ],
        'exclude_categories': ['DeFi & Financial'],
        'threshold': 2.0
    },

    "Social": {
        'patterns': [
            ('STRONG', [
                r"\bsocial\b", r"\bcommunity\b", r"\bprofile\b", r"\bmessag(?:e|ing)\b",
                r"\bchat\b", r"\bforum\b", r"\bpost(?:ing)?\b", r"\bcomment\b",
                r"\bfeed\b", r"\bfollow(?:er)?\b", r"\bfriend\b", r"\bgroup\b",
                r"\bsocial[-_]network\b", r"\bsocial[-_]media\b",
                r"\bsocial[-_]platform\b", r"\bsocial[-_]token[s]?\b",
                r"\bcommunity[-_]hub\b", r"\bcommunity[-_]portal\b",
                r"\bcommunity[-_]management\b", r"\bcommunity[-_]reward[s]?\b",
                r"\bdiscord\b", r"\btelegram\b", r"\btwitter\b",
                r"\bsocial[-_]graph\b", r"\bsocial[-_]feed\b",
                r"\bsocial[-_]engagement\b", r"\bsocial[-_]interaction\b",
                r"\bsocial[-_]connection[s]?\b", r"\bsocial[-_]profile[s]?\b",
                r"\bsocial[-_]identity\b", r"\bsocial[-_]verification\b",
                r"\bsocial[-_]recovery\b", r"\bsocial[-_]wallet\b",
            ]),
            ('MEDIUM', [
                r"\bblog\b", r"\bvideo\b", r"\bstream(?:ing)?\b", r"\bmedia\b",
                r"\bcontent\b", r"\bshare\b", r"\bupload\b",
                r"\bnotification[s]?\b", r"\balert[s]?\b", r"\bping[s]?\b",
                r"\breaction[s]?\b", r"\blike[s]?\b", r"\bshare[s]?\b",
                r"\breputation\b", r"\bkarma\b", r"\bstatus\b",
                r"\bthread[s]?\b", r"\btopic[s]?\b", r"\bdiscussion[s]?\b",
                r"\bmention[s]?\b", r"\btag[s]?\b", r"\bhashtag[s]?\b",
                r"\bmoderation\b", r"\bmod[-_]tool[s]?\b", r"\breport[s]?\b",
                r"\bspam[-_]filter\b", r"\bblock[-_]list\b", r"\bmute[-_]list\b",
                r"\bfriend[-_]list\b", r"\bcontact[s]?\b", r"\bconnection[s]?\b",
            ]),
            ('WEAK', [
                r"\bdao\b", r"\bgovernance\b", r"\bvot(?:e|ing)\b", r"\bproposal\b",
                r"\bpoll\b", r"\belection\b", r"\bdecision\b",
                r"\bcommunity[-_]", r"\bsocial[-_]", r"\bgroup[-_]",
                r"\bchat[-_]", r"\bmessage[-_]", r"\bforum[-_]",
                r"\bprofile[-_]", r"\buser[-_]", r"\bmember[-_]",
                r"\bfeed[-_]", r"\bpost[-_]", r"\bcomment[-_]",
                r"\bshare[-_]", r"\blike[-_]", r"\breact[-_]",
                r"\bfollow[-_]", r"\bfriend[-_]", r"\bconnect[-_]",
                r"\bnotify[-_]", r"\balert[-_]", r"\bping[-_]",
                r"\bmoderate[-_]", r"\breport[-_]", r"\bblock[-_]",
            ])
        ],
        'negative_patterns': [
            r"\btest[-_]social\b", r"\bdemo[-_]social\b",
            r"\bsample[-_]community\b", r"\bexample[-_]community\b",
            r"\bmock[-_]profile\b", r"\bfake[-_]profile\b",
            r"\btest[-_]message\b", r"\bdemo[-_]chat\b",
            r"\bsample[-_]forum\b", r"\bexample[-_]post\b",
        ],
        'exclude_categories': [],
        'threshold': 1.0
    },

    "Data & Analytics": {
        'patterns': [
            ('STRONG', [
                r"\bdata\b", r"\banalytics\b", r"\bmetrics\b", r"\bindex(?:er|ing)?\b",
                r"\bgraph\b", r"\bquery\b", r"\bsubgraph\b", r"\boracle\b",
                r"\bdata[-_]analytics\b", r"\bdata[-_]science\b",
                r"\bbig[-_]data\b", r"\bmachine[-_]learning\b",
                r"\bai\b", r"\bml\b", r"\bdeep[-_]learning\b",
                r"\bdata[-_]mining\b", r"\bdata[-_]warehouse\b",
                r"\bdata[-_]lake\b", r"\bdata[-_]pipeline\b",
                r"\bdata[-_]engineering\b", r"\bdata[-_]processing\b",
                r"\bdata[-_]visualization\b", r"\bdata[-_]reporting\b",
                r"\bdata[-_]collection\b", r"\bdata[-_]aggregation\b",
                r"\bdata[-_]transformation\b", r"\bdata[-_]modeling\b",
                r"\bdata[-_]quality\b", r"\bdata[-_]governance\b",
                r"\bdata[-_]catalog\b", r"\bdata[-_]dictionary\b",
                r"\bdata[-_]lineage\b", r"\bdata[-_]profiling\b",
            ]),
            ('MEDIUM', [
                r"\bdashboard\b", r"\bvisualization\b", r"\breport(?:ing)?\b",
                r"\btracking\b", r"\bmonitor(?:ing)?\b", r"\balert(?:ing)?\b",
                r"\bretl\b", r"\betl\b", r"\belt\b",
                r"\bstatistics\b", r"\bforecasting\b", r"\bprediction\b",
                r"\bregression\b", r"\bclassification\b", r"\bclustering\b",
                r"\banomaly[-_]detection\b", r"\bpattern[-_]recognition\b",
                r"\btime[-_]series\b", r"\btrend[-_]analysis\b",
                r"\bmetric[-_]tracking\b", r"\bkpi[-_]monitoring\b",
                r"\bperformance[-_]analytics\b", r"\busage[-_]analytics\b",
                r"\bweb[-_]analytics\b", r"\buser[-_]analytics\b",
                r"\bchain[-_]analytics\b", r"\btransaction[-_]analytics\b",
                r"\bmarket[-_]analytics\b", r"\btrading[-_]analytics\b",
                r"\brisk[-_]analytics\b", r"\bfraud[-_]analytics\b",
            ]),
            ('WEAK', [
                r"\bdata[-_]", r"\banalytics[-_]",
                r"\bmetric[-_]", r"\breport[-_]",
                r"\bmonitor[-_]", r"\btrack[-_]", r"\blog[-_]",
                r"\binsight[-_]", r"\bvisualize[-_]", r"\bdisplay[-_]",
                r"\bchart[-_]", r"\bgraph[-_]", r"\bplot[-_]",
                r"\bquery[-_]", r"\bsearch[-_]", r"\bfilter[-_]",
                r"\bsort[-_]", r"\bgroup[-_]", r"\baggregate[-_]",
                r"\bprocess[-_]", r"\btransform[-_]", r"\bclean[-_]",
                r"\bvalidate[-_]", r"\bverify[-_]", r"\bcheck[-_]",
                r"\banalyze[-_]", r"\bpredict[-_]", r"\bforecast[-_]",
            ])
        ],
        'exclude_categories': [],
        'threshold': 1.0
    },

    "Security & Privacy": {
        'patterns': [
            ('STRONG', [
                r"\bsecurity\b", r"\baudit\b", r"\bpenetration[-\s]?test\b",
                r"\bvulnerability\b", r"\bexploit\b", r"\bsandbox\b",
            ]),
            ('MEDIUM', [
                r"\bprivacy\b", r"\bencryption\b", r"\bzk\b", r"\bzero[-\s]?knowledge\b",
                r"\banonymity\b", r"\bmixer\b", r"\bconfidential\b",
            ]),
            ('WEAK', [
                r"\bsecurity[-_]", r"\bprivacy[-_]",
            ])
        ],
        'exclude_categories': [],
        'threshold': 1.0
    },

    "Education": {
        'patterns': [
            ('STRONG', [
                r"\blearn(?:ing)?\b", r"\btutorial\b", r"\bcourse\b", r"\bworkshop\b",
                r"\bguide\b", r"\bdoc(?:s|umentation)?\b", r"\bexample\b",
                r"\bsample\b", r"\bstarter\b", r"\btemplate\b",
                r"\beducation(?:al)?\b", r"\bteach(?:ing)?\b", r"\binstruct(?:ion|or)?\b",
                r"\bcurriculum\b", r"\bsyllabus\b", r"\blesson[s]?\b",
                r"\bbootcamp\b", r"\bwebinar\b", r"\btraining\b",
                r"\bonboarding\b", r"\bwalkthrough\b", r"\bhow[-_]to\b",
                r"\blearn[-_]by[-_]example\b", r"\bstep[-_]by[-_]step\b",
                r"\binteractive[-_]tutorial\b", r"\bvideo[-_]course\b",
                r"\blearning[-_]path\b", r"\blearning[-_]module\b",
                r"\beducation[-_]platform\b", r"\blearning[-_]platform\b",
                r"\bskill[-_]tree\b", r"\bknowledge[-_]base\b",
                r"\bresource[-_]center\b", r"\blearning[-_]center\b",
            ]),
            ('MEDIUM', [
                r"\bexam\b", r"\bquiz\b", r"\btest\b", r"\bassignment\b",
                r"\bproject\b", r"\bhomework\b", r"\bexercise\b",
                r"\bsolution\b", r"\banswer\b",
                r"\bmodule[s]?\b", r"\bchapter[s]?\b", r"\bsection[s]?\b",
                r"\bpractice\b", r"\bworksheet[s]?\b",
                r"\bchallenge[s]?\b", r"\bproblem[-_]set[s]?\b",
                r"\bgrading\b", r"\bscoring\b", r"\bfeedback\b",
                r"\bcertificat(?:e|ion)\b", r"\bbadge[s]?\b",
                r"\bprogress\b", r"\bachievement[s]?\b",
                r"\bmentoring\b", r"\bcoaching\b", r"\btutoring\b",
                r"\bstudent[s]?\b", r"\bteacher[s]?\b", r"\bmentor[s]?\b",
                r"\bclass(?:room)?\b", r"\bcourse[-_]material[s]?\b",
                r"\bstudy[-_]guide[s]?\b", r"\breference[-_]material[s]?\b",
            ]),
            ('WEAK', [
                r"hello[-_]world", r"getting[-_]started",
                r"\blearn[-_]", r"\bteach[-_]", r"\beducate[-_]",
                r"\bguide[-_]", r"\btutorial[-_]", r"\bcourse[-_]",
                r"\btraining[-_]", r"\bworkshop[-_]", r"\bwebinar[-_]",
                r"\blesson[-_]", r"\bmodule[-_]", r"\bchapter[-_]",
                r"\bexercise[-_]", r"\bpractice[-_]", r"\bchallenge[-_]",
                r"\bquiz[-_]", r"\btest[-_]", r"\bexam[-_]",
                r"\bstudy[-_]", r"\blearn[-_]more\b", r"\bread[-_]more\b",
                r"\bstart[-_]here\b", r"\bquick[-_]start\b",
            ])
        ],
        'negative_patterns': [
            r"\btest[-_]tutorial\b", r"\bdemo[-_]tutorial\b",
            r"\bsample[-_]course\b", r"\bexample[-_]course\b",
            r"\bmock[-_]test\b", r"\bfake[-_]test\b",
            r"\btest[-_]exercise\b", r"\bdemo[-_]exercise\b",
            r"\bsample[-_]quiz\b", r"\bexample[-_]quiz\b",
        ],
        'exclude_categories': [],
        'threshold': 0.5
    },

    "Infrastructure & Tools": {
        'patterns': [
            ('STRONG', [
                # Core infrastructure
                r"\bnode[s]?\b", r"\bvalidator[s]?\b", r"\binfrastructure\b",
                r"\bframework[s]?\b", r"\bprotocol[s]?\b", r"\bnetwork[s]?\b",
                r"\bsdk[s]?\b", r"\bapi[s]?\b", r"\bcli\b", r"\btoolkit[s]?\b",
                
                # Development tools
                r"\bcompiler\b", r"\bdeployer\b", r"\bdebugger\b",
                r"\bmonitor\b", r"\banalyzer\b", r"\bexplorer\b",
                r"\blibrary\b", r"\bpackage\b", r"\bmodule\b",
                
                # Move/Aptos specific
                r"\bmove[-_]lang\b", r"\bmove[-_]compiler\b",
                r"\bmove[-_]framework\b", r"\bmove[-_]stdlib\b",
                r"\baptos[-_]framework\b", r"\baptos[-_]sdk\b",
                r"\baptos[-_]cli\b", r"\baptos[-_]core\b",
                r"\baptos[-_]node\b", r"\baptos[-_]validator\b"
            ]),
            ('MEDIUM', [
                # Development features
                r"\bintegration[s]?\b", r"\binterface[s]?\b",
                r"\bwrapper[s]?\b", r"\bbridge[s]?\b",
                r"\bclient[s]?\b", r"\bserver[s]?\b",
                r"\blog(?:ging|ger)?\b", r"\bmetric[s]?\b",
                
                # Tools and utilities
                r"\btool[s]?\b", r"\butil(?:s|ity|ities)?\b",
                r"\bhelper[s]?\b", r"\bscript[s]?\b",
                r"\bconfig\b", r"\bsetup\b", r"\bbuild\b",
                
                # Move/Aptos specific
                r"\bmove[-_]tool\b", r"\bmove[-_]prover\b",
                r"\bmove[-_]analyzer\b", r"\bmove[-_]cli\b",
                r"\baptos[-_]tool\b", r"\baptos[-_]config\b"
            ]),
            ('WEAK', [
                # Generic terms
                r"\bdev\b", r"\bdevelopment\b", r"\bcode\b",
                r"\bimplementation\b", r"\brepository\b",
                r"\bproject\b", r"\bsolution\b", r"\bplatform\b",
                
                # Technical terms
                r"\bfunction[s]?\b", r"\bmethod[s]?\b",
                r"\bclass[es]?\b", r"\bstruct[s]?\b",
                r"\binterface[s]?\b", r"\bmodule[s]?\b"
            ])
        ],
        'negative_patterns': [
            r"\btest[-_]infra\b", r"\bdemo[-_]infra\b",
            r"\bsample[-_]tool\b", r"\bexample[-_]tool\b",
            r"\bmock[-_]service\b", r"\bfake[-_]service\b",
            r"\btest[-_]api\b", r"\bdemo[-_]api\b",
            r"\bsample[-_]sdk\b", r"\bexample[-_]sdk\b",
        ],
        'exclude_categories': [],
        'threshold': 1.0
    },

    "Identity & Authentication": {
        'patterns': [
            ('STRONG', [
                r"\bidentity\b", r"\bauth(?:entication)?\b", r"\bsso\b", r"\boauth\b",
                r"\bkyc\b", r"\bverif(?:y|ication)\b", r"\bcredential\b",
                r"\bidentity[-_]provider\b", r"\bauth[-_]provider\b",
                r"\bsingle[-_]sign[-_]on\b", r"\bmulti[-_]factor\b",
                r"\b2fa\b", r"\bmfa\b", r"\btotp\b", r"\bhotp\b",
                r"\bsaml\b", r"\boidc\b", r"\bjwt\b", r"\bbearer\b",
                r"\bpassport[-_]js\b", r"\bkeycloak\b", r"\bauth0\b",
                r"\bokta\b", r"\bonelogin\b", r"\bping[-_]identity\b",
                r"\bauthentik\b", r"\bfido\b", r"\bwebauthn\b",
                r"\bu2f\b", r"\byubikey\b", r"\bbiometric[s]?\b",
            ]),
            ('MEDIUM', [
                r"\bpassword[s]?\b", r"\bcredential[s]?\b", r"\btoken[s]?\b",
                r"\bsession[s]?\b", r"\bcookie[s]?\b", r"\bheader[s]?\b",
                r"\bclaim[s]?\b", r"\bscope[s]?\b", r"\brole[s]?\b",
                r"\bpermission[s]?\b", r"\bpolicy\b", r"\brule[s]?\b",
                r"\baccess[-_]control\b", r"\brbac\b", r"\babac\b",
                r"\bgroup[s]?\b", r"\buser[s]?\b", r"\btenant[s]?\b",
                r"\bdomain[s]?\b", r"\brealm[s]?\b", r"\bnamespace[s]?\b",
                r"\bprovider[s]?\b", r"\bstrategy\b", r"\bflow[s]?\b",
            ]),
            ('WEAK', [
                r"\bauth[-_]", r"\bidentity[-_]", r"\blogin[-_]",
                r"\bsignin[-_]", r"\bsignup[-_]", r"\bregister[-_]",
                r"\bverify[-_]", r"\bvalidate[-_]", r"\bcheck[-_]",
                r"\bsecure[-_]", r"\bprotect[-_]", r"\bguard[-_]",
                r"\baccess[-_]", r"\bpermission[-_]", r"\brole[-_]",
                r"\buser[-_]", r"\baccount[-_]", r"\bprofile[-_]",
                r"\bsession[-_]", r"\btoken[-_]", r"\bcookie[-_]",
                r"\bcredential[-_]", r"\bpassword[-_]", r"\bsecret[-_]",
            ])
        ],
        'negative_patterns': [
            r"\btest[-_]auth\b", r"\bdemo[-_]auth\b",
            r"\bsample[-_]login\b", r"\bexample[-_]login\b",
            r"\bmock[-_]user\b", r"\bfake[-_]user\b",
            r"\btest[-_]account\b", r"\bdemo[-_]account\b",
            r"\bsample[-_]token\b", r"\bexample[-_]token\b",
        ],
        'exclude_categories': [],
        'threshold': 1.0
    },

    "Smart Contracts & Core": {
        'patterns': [
            ('STRONG', [
                # Core contract terms
                r"\bsmart[-_]contract[s]?\b", r"\bcontract[s]?\b",
                r"\bmodule[s]?\b", r"\bfunction[s]?\b",
                r"\binterface[s]?\b", r"\blibrary\b",
                
                # Move specific
                r"\bmove[-_]module\b", r"\bmove[-_]contract\b",
                r"\bmove[-_]resource\b", r"\bmove[-_]capability\b",
                r"\bmove[-_]signer\b", r"\bmove[-_]account\b",
                
                # Aptos specific
                r"\baptos[-_]framework\b", r"\baptos[-_]std\b",
                r"\baptos[-_]token\b", r"\baptos[-_]coin\b",
                r"\baptos[-_]account\b", r"\baptos[-_]resource\b"
            ]),
            ('MEDIUM', [
                # Contract features
                r"\bentry[-_]function\b", r"\bpublic[-_]function\b",
                r"\bview[-_]function\b", r"\bscript[-_]function\b",
                r"\bresource[-_]account\b", r"\bresource[-_]group\b",
                r"\bsigner[-_]capability\b", r"\bstore[-_]capability\b",
                
                # Technical terms
                r"\bstruct[s]?\b", r"\bevent[s]?\b", r"\berror[s]?\b",
                r"\btype[s]?\b", r"\bgeneric[s]?\b", r"\bstorage\b",
                r"\bmemory\b", r"\bstate\b", r"\bcallback[s]?\b"
            ]),
            ('WEAK', [
                # Generic terms
                r"\bimplementation\b", r"\bdeployment\b",
                r"\bupgrade\b", r"\bmigration\b", r"\bversion\b",
                r"\brelease\b", r"\bupdate\b", r"\bpatch\b",
                
                # Technical concepts
                r"\bpattern[s]?\b", r"\bstandard[s]?\b",
                r"\bprotocol[s]?\b", r"\binterface[s]?\b",
                r"\bwrapper[s]?\b", r"\bproxy\b"
            ])
        ],
        'threshold': 1.0
    }
}

# Compile patterns for efficiency
def compile_patterns(patterns, negative_patterns=None):
    """Compile both positive and negative regex patterns with case-insensitive flag."""
    compiled = {
        'positive': [re.compile(pattern, re.IGNORECASE) for pattern in patterns],
        'negative': [re.compile(pattern, re.IGNORECASE) for pattern in (negative_patterns or [])]
    }
    return compiled

COMPILED_CATEGORIES = {
    category: {
        'patterns': compile_patterns(
            [p for strength, patterns in cat_data['patterns'] for p in patterns],
            cat_data.get('negative_patterns', [])
        ),
        'weights': {pattern: PATTERN_WEIGHTS[strength]
                   for strength, patterns in cat_data['patterns']
                   for pattern in patterns},
        'threshold': cat_data['threshold']
    }
    for category, cat_data in CATEGORIES.items()
}

REPO_PATTERN = re.compile(
    r'\[\[repo\]\]\s*url\s*=\s*"(https://github\.com/([^/]+)/([^/"\s]+))"'
    r'(?:\s*missing\s*=\s*(true|false))?',
    re.IGNORECASE
)

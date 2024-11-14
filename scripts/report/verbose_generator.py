"""Module for generating verbose sections of repository analysis reports."""

from collections import defaultdict
from typing import List, Dict, TextIO, Tuple
from constants import CATEGORIES, PATTERN_WEIGHTS

def get_human_readable_pattern(pattern: str) -> str:
    """Convert regex pattern to human readable format."""
    translations = {
        # DeFi & Financial
        r"\b(?:de)?fi\b": "DeFi",
        r"\bdefi[-_]": "DeFi Projects",
        r"_(?:de)?fi\b": "DeFi Suffix",
        r"\bvault[s]?\b": "Vaults",
        r"\byield[s]?\b": "Yield",
        r"\byielding\b": "Yielding",
        r"\bamm\b": "AMM",
        r"\bperpetual[s]?\b": "Perpetuals",
        r"\bperp[s]?\b": "Perps",
        r"\baave\b": "Aave",
        r"\bcompound\b": "Compound",
        r"\bfrax\b": "Frax",
        r"\bcurve\b": "Curve",
        r"\buniswap\b": "Uniswap",
        r"\bsushiswap\b": "Sushiswap",
        r"\blending[-_]protocol\b": "Lending Protocol",
        r"\bliquid[-_]staking\b": "Liquid Staking",
        r"\bstaking[-_]protocol\b": "Staking Protocol",
        r"\bfinance\b": "Finance",
        r"\bfinancial\b": "Financial",
        r"\bmonetary\b": "Monetary",
        r"\bcurve[-_]pool\b": "Curve Pool",
        r"\bcurve[-_]gauge\b": "Curve Gauge",
        r"\baave[-_]v[2-3]\b": "Aave v2/v3",
        r"\bcompound[-_]v[2-3]\b": "Compound v2/v3",
        r"\bliquity\b": "Liquity",
        r"\balchemix\b": "Alchemix",
        r"\bsynthetix\b": "Synthetix",
        r"\bribbon\b": "Ribbon",
        r"\bconvex\b": "Convex",
        r"\bbalancer\b": "Balancer",
        r"\bvetoken[s]?\b": "veTokens",
        r"\bvault[-_]strategy\b": "Vault Strategy",
        r"\byield[-_]optimizer\b": "Yield Optimizer",
        r"\byield[-_]booster\b": "Yield Booster",
        r"\bleveraged[-_]yield\b": "Leveraged Yield",
        r"\bflash[-_]mint\b": "Flash Mint",
        r"\bliquidity[-_]mining\b": "Liquidity Mining",
        r"\bliquidity[-_]provision\b": "Liquidity Provision",
        r"\bstaking[-_]rewards\b": "Staking Rewards",
        r"\brebase[-_]token\b": "Rebase Token",
        r"\belastic[-_]supply\b": "Elastic Supply",
        r"\bvoting[-_]escrow\b": "Voting Escrow",
        r"\btoken[-_]bridge(?:[-_]func)?\b": "Token Bridge",
        r"\bliquid(?:ity|ation)\b": "Liquidity",
        r"\bswap[s]?\b": "Swaps",
        r"\bswapping\b": "Swapping",
        r"\bstaking\b": "Staking",
        r"\bstake[s]?\b": "Stakes",
        r"\blp[s]?\b": "LPs",
        r"\bpool[s]?\b": "Pools",
        r"\bfarm(?:ing)?\b": "Farming",
        r"\bharvest(?:er|ing)?\b": "Harvesting",
        r"\blend(?:ing)?\b": "Lending",
        r"\bloan[s]?\b": "Loans",
        r"\bborrow(?:ing)?\b": "Borrowing",
        r"\bcollateral\b": "Collateral",
        r"\bmargin\b": "Margin",
        r"\bleverage\b": "Leverage",
        r"\binterest[-_]rate\b": "Interest Rate",
        r"\binterest[-_]bearing\b": "Interest Bearing",
        r"\btoken[-_]swap\b": "Token Swap",
        r"\bmarket[-_]maker\b": "Market Maker",
        r"\bimpermanent[-_]loss\b": "Impermanent Loss",
        r"\bslippage\b": "Slippage",
        r"\bgas[-_]optimization\b": "Gas Optimization",
        r"\bmulti[-_]sig\b": "Multi-sig",
        r"\btime[-_]lock\b": "Time Lock",
        r"\bprice[-_]impact\b": "Price Impact",
        r"\bliquidity[-_]bootstrapping\b": "Liquidity Bootstrapping",
        r"\bfee[-_]sharing\b": "Fee Sharing",
        r"\byield[-_]bearing\b": "Yield Bearing",
        r"\byield[-_]generating\b": "Yield Generating",
        r"\bcollateral[-_]ratio\b": "Collateral Ratio",
        r"\bdebt[-_]ratio\b": "Debt Ratio",
        r"\brisk[-_]management\b": "Risk Management",
        r"\bportfolio[-_]management\b": "Portfolio Management",
        r"\btreasury[-_]management\b": "Treasury Management",
        r"\basset[-_]management\b": "Asset Management",
        r"\bvault[-_]management\b": "Vault Management",
        r"\bpool[-_]management\b": "Pool Management",
        r"\bstaking[-_]management\b": "Staking Management",

        # NFTs & Digital Assets
        r"\bnft[s]?\b": "NFTs",
        r"[-_]nft[s]?\b": "NFT Suffix",
        r"\bnft[-_]": "NFT Prefix",
        r"\berc[-\s]?721\b": "ERC-721",
        r"\berc[-\s]?1155\b": "ERC-1155",
        r"\bopensea\b": "OpenSea",
        r"\brarible\b": "Rarible",
        r"\bnifty\b": "Nifty",
        r"\bcollectible[s]?\b": "Collectibles",
        r"\bdigital[-_]collectible[s]?\b": "Digital Collectibles",
        r"\bnon[-_]fungible\b": "Non-Fungible",
        r"\btokenid\b": "TokenID",
        r"\bseaport\b": "Seaport",
        r"\blooksrare\b": "LooksRare",
        r"\bx2y2\b": "X2Y2",
        r"\bmagic[-_]eden\b": "Magic Eden",
        r"\bblur\b": "Blur",
        r"\bfoundation\b": "Foundation",
        r"\bsuperrare\b": "SuperRare",
        r"\bmanifold\b": "Manifold",
        r"\bartblocks\b": "ArtBlocks",
        r"\bzora\b": "Zora",
        r"\bcatalyst\b": "Catalyst",
        r"\bknown[-_]origin\b": "KnownOrigin",
        r"\bnft[-_]marketplace\b": "NFT Marketplace",
        r"\bnft[-_]auction\b": "NFT Auction",
        r"\bnft[-_]bridge\b": "NFT Bridge",
        r"\btoken[-_]gating\b": "Token Gating",
        r"\bsoulbound\b": "Soulbound",
        r"\bpoap[s]?\b": "POAPs",
        r"\berc[-_]4907\b": "ERC-4907",
        r"\berc[-_]5643\b": "ERC-5643",
        r"\berc[-_]2981\b": "ERC-2981",
        r"\bpfp[s]?\b": "PFPs",
        r"\bavatar[-_]generator\b": "Avatar Generator",
        r"\bmetadata[-_]standard\b": "Metadata Standard",

        # Infrastructure & Tools
        r"\bnode[s]?\b": "Nodes",
        r"\bvalidator[s]?\b": "Validators",
        r"\binfrastructure\b": "Infrastructure",
        r"\bprotocol[s]?\b": "Protocols",
        r"\bframework[s]?\b": "Frameworks",
        r"\bsdk[s]?\b": "SDKs",
        r"\bapi[s]?\b": "APIs",
        r"\bcli\b": "CLI",
        r"\btoolkit[s]?\b": "Toolkits",
        r"\btool[-_]suite\b": "Tool Suite",
        r"\bsmart[-_]contract[s]?\b": "Smart Contracts",
        r"\bcontract[-_]framework\b": "Contract Framework",
        r"\bblockchain[-_](?:node|validator|infrastructure)\b": "Blockchain Infrastructure",
        r"\binfra[-_]as[-_]code\b": "Infrastructure as Code",
        r"\bdevops\b": "DevOps",
        r"\bci[-_]cd\b": "CI/CD",
        r"\bpipeline[s]?\b": "Pipelines",
        r"\bdeployment[s]?\b": "Deployments",
        r"\bcontainer[s]?\b": "Containers",
        r"\bdocker\b": "Docker",
        r"\bkubernetes\b": "Kubernetes",
        r"\bk8s\b": "K8s",
        r"\bterraform\b": "Terraform",
        r"\bansible\b": "Ansible",
        r"\bchef\b": "Chef",
        r"\bpuppet\b": "Puppet",
        r"\bjenkins\b": "Jenkins",
        r"\bgithub[-_]action[s]?\b": "GitHub Actions",

        # Data & Analytics
        r"\bdata\b": "Data",
        r"\banalytics\b": "Analytics",
        r"\bmetrics\b": "Metrics",
        r"\bindex(?:er|ing)?\b": "Indexing",
        r"\bgraph\b": "Graph",
        r"\bquery\b": "Query",
        r"\bsubgraph\b": "Subgraph",
        r"\boracle\b": "Oracle",
        r"\bdata[-_]analytics\b": "Data Analytics",
        r"\bdata[-_]science\b": "Data Science",
        r"\bbig[-_]data\b": "Big Data",
        r"\bmachine[-_]learning\b": "Machine Learning",
        r"\bai\b": "AI",
        r"\bml\b": "ML",
        r"\bdeep[-_]learning\b": "Deep Learning",

        # Gaming & Entertainment
        r"\bgame\b": "Game",
        r"\bplay\b": "Play",
        r"\bgaming\b": "Gaming",
        r"\barcade\b": "Arcade",
        r"\bmetaverse\b": "Metaverse",
        r"\bvirtual[-\s]world\b": "Virtual World",
        r"\bgamefi\b": "GameFi",
        r"\bp2e\b": "P2E",
        r"\bplay[-_]to[-_]earn\b": "Play to Earn",

        # Identity & Authentication
        r"\bidentity\b": "Identity",
        r"\bauth(?:entication)?\b": "Authentication",
        r"\bsso\b": "SSO",
        r"\boauth\b": "OAuth",
        r"\bkyc\b": "KYC",
        r"\bverif(?:y|ication)\b": "Verification",
        r"\bcredential\b": "Credential",

        # Social
        r"\bsocial\b": "Social",
        r"\bcommunity\b": "Community",
        r"\bprofile\b": "Profile",
        r"\bmessag(?:e|ing)\b": "Messaging",
        r"\bchat\b": "Chat",
        r"\bforum\b": "Forum",
        r"\bpost(?:ing)?\b": "Posting",
        r"\bcomment\b": "Comment",
        r"\bfeed\b": "Feed",
        r"\bfollow(?:er)?\b": "Follower",
        r"\bfriend\b": "Friend",
        r"\bgroup\b": "Group",

        # Security & Privacy
        r"\bsecurity\b": "Security",
        r"\baudit\b": "Audit",
        r"\bpenetration[-\s]?test\b": "Penetration Test",
        r"\bvulnerability\b": "Vulnerability",
        r"\bexploit\b": "Exploit",
        r"\bsandbox\b": "Sandbox",
        r"\bprivacy\b": "Privacy",
        r"\bencryption\b": "Encryption",
        r"\bzk\b": "ZK",
        r"\bzero[-\s]?knowledge\b": "Zero Knowledge",
    }
    return translations.get(pattern, pattern.replace(r"\b", "").replace(r"[-_]", " "))

def generate_verbose_section(f: TextIO, primary_category: str, all_ecosystem_data: List[Dict]) -> None:
    """Generate a verbose section for a specific category."""
    # Handle uncategorized section differently
    if primary_category == "Uncategorized":
        f.write(f"\n### Uncategorized Repositories\n\n")
        f.write("| Chain | Account | Repository |\n")
        f.write("|-------|---------|------------|\n")
        
        # Collect repositories with no pattern matches
        uncategorized = []
        for eco_data in all_ecosystem_data:
            eco_name = eco_data['name']
            pattern_matches = eco_data.get('pattern_matches', {})
            
            for repo_url, category_patterns in pattern_matches.items():
                if "Uncategorized" in category_patterns:  # This is the correct check
                    uncategorized.append({
                        'chain': eco_name,
                        'repo': repo_url
                    })
        
        # Sort and write uncategorized matches
        uncategorized.sort(key=lambda x: (x['chain'], x['repo']))
        for match in uncategorized:
            repo_parts = match['repo'].split('/')
            account_name = repo_parts[-2]
            repo_name = repo_parts[-1]
            f.write(f"| {match['chain']} | [{account_name}](https://github.com/{account_name}) | [{repo_name}]({match['repo']}) |\n")
        
        return

    if primary_category not in CATEGORIES:
        return
        
    # Get all patterns for this category
    all_patterns = []
    for strength, patterns in CATEGORIES[primary_category]['patterns']:
        for pattern in patterns:
            all_patterns.append((pattern, strength))
    
    # Collect all matches across ecosystems
    matches_by_pattern = defaultdict(list)
    
    for eco_data in all_ecosystem_data:
        eco_name = eco_data['name']
        pattern_matches = eco_data.get('pattern_matches', {})
        
        # For each repository and its matched patterns
        for repo_url, category_patterns in pattern_matches.items():
            # For each category and its patterns
            for category, patterns in category_patterns.items():
                # Only process patterns from our primary category
                if category == primary_category:
                    for pattern in patterns:
                        matches_by_pattern[pattern].append({
                            'chain': eco_name,
                            'repo': repo_url
                        })
    
    # Write section header
    total_matches = sum(len(matches) for matches in matches_by_pattern.values())
    f.write(f"\n### {primary_category} (Total Matches: {total_matches})\n\n")

    # Process patterns by strength
    for strength in ['STRONG', 'MEDIUM', 'WEAK']:
        strength_patterns = [(p, s) for p, s in all_patterns if s == strength]
        for pattern, _ in strength_patterns:
            matches = matches_by_pattern.get(pattern, [])
            if not matches:
                continue
            
            readable_name = get_human_readable_pattern(pattern)
            f.write(f"<details>\n")
            f.write(f"<summary>{readable_name} ({strength}) - {len(matches)} matches</summary>\n\n")
            f.write("| Chain | Account | Repository |\n")
            f.write("|-------|---------|------------|\n")
            
            # Sort and write matches
            matches.sort(key=lambda x: (x['chain'], x['repo']))
            for match in matches:
                repo_parts = match['repo'].split('/')
                account_name = repo_parts[-2]
                repo_name = repo_parts[-1]
                f.write(f"| {match['chain']} | [{account_name}](https://github.com/{account_name}) | [{repo_name}]({match['repo']}) |\n")
            
            f.write("\n</details>\n\n")
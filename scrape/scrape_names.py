import json
import logging
import os
import time
from typing import Dict, Optional, Tuple, List, Generator
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from urllib.parse import quote
import re

import backoff

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@backoff.on_exception(backoff.expo, HTTPError, max_tries=5, giveup=lambda e: e.code not in [403, 429])
def make_github_request(url: str, headers: Dict[str, str]) -> Dict:
    req = Request(url, headers=headers)
    with urlopen(req) as response:
        return json.loads(response.read())

def github_search_repos(project_name: str, token: Optional[str] = None) -> Generator[Tuple[str, str], None, None]:
    """
    Simplified search for repositories matching the project name.
    """
    headers = {
        'User-Agent': 'Python Script',
        'Accept': 'application/vnd.github.v3+json'
    }
    if token:
        headers['Authorization'] = f'Bearer {token}'
    
    # Create basic variations of the name
    name_variations = [
        project_name.lower(),
        project_name.lower().replace(' ', ''),
        project_name.lower().replace(' ', '-'),
    ]
    
    # Simple search query that looks for the name in repository names and descriptions
    search_query = f'{project_name} in:name,description'
    encoded_query = quote(search_query)
    
    page = 1
    while True:
        url = f'https://api.github.com/search/repositories?q={encoded_query}&page={page}&per_page=100'
        
        try:
            data = make_github_request(url, headers)
            logger.info(f"Searching: {project_name} - Found {data['total_count']} repositories")
            
            if not data['items']:
                break
                
            for item in data['items']:
                repo_name = item['name'].lower()
                repo_description = (item.get('description') or '').lower()
                
                # Simple match if repository name contains any variation of the project name
                if any(variation in repo_name for variation in name_variations):
                    yield (item['owner']['login'], item['name'])
            
            page += 1
            
        except HTTPError as e:
            logger.error(f"Error fetching search results: {e.code} - {e.reason}")
            break

def main():
    token = os.environ.get('GITHUB_TOKEN')
    if not token:
        logger.warning("GITHUB_TOKEN not found. Rate limits will be restricted!")
        response = input("Do you want to continue anyway? (y/n): ")
        if response.lower() != 'y':
            return

    # Define the project names to search
    project_names = [
        "RareGoods Loyalty", "Crossmint", "Toymak3rs", "Tevi", "MyCo",
        "GuardianLink", "Reliance", "Ambitious Dirt", "Midnight", "STAN",
        "Ready Games", "Macroverse", "Aptos Monkeys", "Meereo", "Wapal",
        "XenoShot", "Muwpay", "Propbase", "TowneSquare", "CRED",
        "Pixel Pirates", "Proud Lions", "DeFy", "Qiro", "Arculus",
        "Verichains", "Fibonacci Finance", "Recoop Rentals", "Canal Group",
        "Chromata", "LHDao", "StreamFlow", "SendinAir", "Kaptos", "Patronus",
        "MemPools", "ZKPayment", "Echo Protocol", "LoveAI", "Nautilus AI Agent",
        "Cipher Wallet", "Rimosafe", "DOVE Finance", "Playside", "Aptomingos",
        "Aptorobos", "Arkpia", "ASTX", "Creatures", "Infinity Sound",
        "Mercato", "TradePort", "Indexer", "Metatokyo", "Zaaptos", "Ice Blue",
        "Spooks", "NMKR", "Slime Revolution", "Quiccs", "FireX", "Quid.li",
        "Spawnpoint", "Armur.ai", "Monstos", "Dappworld", "Spheron",
        "Sport Trade", "Huddle01", "Push protocol", "Envelop DAO"
    ]

    # Create a dictionary to store results for each project
    project_results = {}

    # Search for each project name
    for project_name in project_names:
        logger.info(f"Searching for project: {project_name}")
        project_repos = list(github_search_repos(project_name, token))
        project_results[project_name] = project_repos
        logger.info(f"Found {len(project_repos)} repositories for {project_name}")

    # Save results as markdown table
    os.makedirs('output', exist_ok=True)
    with open('output/repos_results.md', 'w') as f:
        f.write("# Project Repositories\n\n")
        
        # Write table header
        f.write("| Project Name | Repository Links |\n")
        f.write("|--------------|------------------|\n")
        
        # Write table rows
        for project_name, repos in project_results.items():
            if repos:
                # Join multiple repos with <br> for markdown line breaks
                repo_links = "<br>".join([f"[{repo}](https://github.com/{owner}/{repo})" 
                                        for owner, repo in repos])
                f.write(f"| {project_name} | {repo_links} |\n")
            else:
                f.write(f"| {project_name} | No repositories found |\n")
    
    logger.info(f"Saved results to output/repos_results.md")

if __name__ == "__main__":
    main()
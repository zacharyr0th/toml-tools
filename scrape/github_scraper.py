from urllib.request import Request, urlopen
import json
from urllib.error import HTTPError
import time
from typing import Dict, Optional, Tuple, List
import os

def github_search_repos(query: str, token: Optional[str] = None) -> List[Tuple[str, str]]:
    """
    Search for repositories matching the query.
    
    Returns:
        List[Tuple[str, str]]: List of (owner, repo) tuples
    """
    headers = {
        'User-Agent': 'Python Script',
        'Accept': 'application/vnd.github.v3+json'
    }
    if token:
        headers['Authorization'] = f'Bearer {token}'
        
    repos = []
    page = 1
    
    while True:
        try:
            url = f'https://api.github.com/search/repositories?q={query}&page={page}&per_page=100'
            req = Request(url, headers=headers)
            with urlopen(req) as response:
                data = json.loads(response.read())
                if not data['items']:
                    break
                    
                for item in data['items']:
                    repos.append((item['owner']['login'], item['name']))
                
                page += 1
                time.sleep(2)  # Rate limiting
                
        except HTTPError as e:
            print(f"Error fetching search results: {e.code} - {e.reason}")
            break
            
    return repos

def github_scrape(owner: str, repo: str, token: Optional[str] = None, silent: bool = False) -> Optional[Dict[str, Tuple[float, int]]]:
    """
    Scrape language information from a GitHub repository.
    
    Args:
        owner (str): Repository owner
        repo (str): Repository name
        token (str, optional): GitHub personal access token
        silent (bool, optional): If True, suppresses print output
        
    Returns:
        Dict[str, Tuple[float, int]]: Dictionary of languages with their percentages and byte counts
        None: If there was an error fetching data
    """
    
    headers = {
        'User-Agent': 'Python Script',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    if token:
        headers['Authorization'] = f'Bearer {token}'
    
    try:
        for attempt in range(3):
            try:
                req = Request(f'https://api.github.com/repos/{owner}/{repo}/languages', headers=headers)
                with urlopen(req) as response:
                    languages_data = json.loads(response.read())
                    
                    if not languages_data:
                        return None
                        
                    total_bytes = sum(languages_data.values())
                    result = {
                        lang: ((bytes_count / total_bytes) * 100, bytes_count)
                        for lang, bytes_count in languages_data.items()
                    }
                    
                    if not silent:
                        print(f"\nLanguages in {owner}/{repo}:")
                        for lang, (percentage, bytes_count) in result.items():
                            print(f"{lang}: {percentage:.1f}% ({bytes_count:,} bytes)")
                        
                    return result
                    
            except HTTPError as e:
                if e.code == 403 and attempt < 2:
                    time.sleep(2 ** attempt)
                    continue
                raise
                
    except HTTPError as e:
        if not silent:
            print(f"Error: {e.code} - {e.reason}")
            if e.code == 403:
                print("Rate limit exceeded. Try using a token.")
            elif e.code == 404:
                print("Repository not found.")
        return None
        
    except Exception as e:
        if not silent:
            print(f"Unexpected error: {str(e)}")
        return None

if __name__ == "__main__":
    token = None  # "your-token-here"
    
    # Search for Move language repositories
    repos = github_search_repos("language:Move", token)
    print(f"Found {len(repos)} repositories total")
    
    # Take only first 20 repositories
    repos = repos[:20]
    print(f"Processing first {len(repos)} repositories...")
    
    # Collect language stats for each repo
    results = {}
    for owner, repo in repos:
        langs = github_scrape(owner, repo, token, silent=True)
        if langs and 'Move' in langs:
            results[(owner, repo)] = langs['Move']
        time.sleep(1)  # Rate limiting
    
    # Create output directory if it doesn't exist
    os.makedirs('output', exist_ok=True)
    
    # Save to file
    with open('output/move_repos.txt', 'w') as f:
        f.write("# Move Language Repositories\n\n")
        for (owner, repo), (percentage, bytes_count) in results.items():
            f.write(f"https://github.com/{owner}/{repo}\n")
    
    print(f"\nSaved {len(results)} repositories to output/move_repos.txt")
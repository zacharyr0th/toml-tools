from urllib.request import Request, urlopen
import json
from urllib.error import HTTPError
import time
from typing import Dict, Optional, Tuple

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
    github_scrape(
        owner="zacharyr0th",
        repo="toml-tools",
        token=None  # "your-token-here"
    )
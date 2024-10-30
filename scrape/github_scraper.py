import json
import logging
import os
import time
from typing import Dict, Optional, Tuple, List, Generator
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from urllib.parse import quote

import backoff

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@backoff.on_exception(backoff.expo, HTTPError, max_tries=5, giveup=lambda e: e.code not in [403, 429])
def make_github_request(url: str, headers: Dict[str, str]) -> Dict:
    req = Request(url, headers=headers)
    with urlopen(req) as response:
        return json.loads(response.read())

def github_search_repos(query: str, token: Optional[str] = None) -> Generator[Tuple[str, str], None, None]:
    """
    Search for repositories matching the query, breaking down by creation date to bypass the 1000 result limit.
    
    Yields:
        Tuple[str, str]: (owner, repo) tuples
    """
    headers = {
        'User-Agent': 'Python Script',
        'Accept': 'application/vnd.github.v3+json'
    }
    if token:
        headers['Authorization'] = f'Bearer {token}'
    
    # Define time ranges to search (adjust as needed)
    date_ranges = [
        "created:2020-01-01..2021-12-31",
        "created:2022-01-01..2022-12-31",
        "created:2023-01-01..2023-12-31",
        "created:2024-01-01..2024-12-31"
    ]
    
    for date_range in date_ranges:
        page = 1
        while True:
            search_query = f"{query} {date_range}"
            encoded_query = quote(search_query)
            url = f'https://api.github.com/search/repositories?q={encoded_query}&page={page}&per_page=100'
            
            try:
                data = make_github_request(url, headers)
                logger.info(f"Searching: {search_query} - Found {data['total_count']} repositories")
                
                if not data['items']:
                    break
                    
                for item in data['items']:
                    yield (item['owner']['login'], item['name'])
                
                page += 1
                
            except HTTPError as e:
                logger.error(f"Error fetching search results: {e.code} - {e.reason}")
                break

def github_scrape(owner: str, repo: str, token: Optional[str] = None) -> Optional[Dict[str, Tuple[float, int]]]:
    """
    Scrape language information from a GitHub repository.
    
    Args:
        owner (str): Repository owner
        repo (str): Repository name
        token (str, optional): GitHub personal access token
        
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
        url = f'https://api.github.com/repos/{owner}/{repo}/languages'
        languages_data = make_github_request(url, headers)
        
        if not languages_data:
            return None
            
        total_bytes = sum(languages_data.values())
        result = {
            lang: ((bytes_count / total_bytes) * 100, bytes_count)
            for lang, bytes_count in languages_data.items()
        }
        
        logger.info(f"Languages in {owner}/{repo}:")
        for lang, (percentage, bytes_count) in result.items():
            logger.info(f"{lang}: {percentage:.1f}% ({bytes_count:,} bytes)")
        
        return result
                
    except HTTPError as e:
        logger.error(f"Error: {e.code} - {e.reason}")
        if e.code == 403:
            logger.warning("Rate limit exceeded. Try using a token.")
        elif e.code == 404:
            logger.warning("Repository not found.")
        return None
        
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return None

def save_results(results: Dict, filename: str):
    os.makedirs('output', exist_ok=True)
    with open(filename, 'w') as f:
        f.write("# Move Language Repositories\n\n")
        for (owner, repo), (percentage, bytes_count) in results.items():
            f.write(f"https://github.com/{owner}/{repo}\n")
    logger.info(f"Saved {len(results)} repositories to {filename}")

def compile_and_cleanup_results(final_filename: str):
    """Combines all batch files into a single file and deletes the batch files."""
    all_results = []
    batch_files = [f for f in os.listdir('output') if f.startswith('move_repos_batch_')]
    
    for batch_file in batch_files:
        with open(os.path.join('output', batch_file), 'r') as f:
            # Skip the header line
            next(f)
            next(f)
            all_results.extend(f.readlines())
            
        # Delete the batch file
        os.remove(os.path.join('output', batch_file))
        
    # Write combined results
    with open(final_filename, 'w') as f:
        f.write("# Move Language Repositories\n\n")
        f.writelines(all_results)
    
    logger.info(f"Combined {len(batch_files)} batch files into {final_filename}")
    logger.info(f"Cleaned up {len(batch_files)} batch files")

def main():
    token = os.environ.get('GITHUB_TOKEN')
    if not token:
        logger.error("GITHUB_TOKEN not found. This will take ~40 hours without authentication!")
        response = input("Do you want to continue anyway? (y/n): ")
        if response.lower() != 'y':
            return

    # Add rate limit tracking
    start_time = time.time()
    processed = 0

    repos = list(github_search_repos("language:Move", token))
    total_repos = len(repos)
    logger.info(f"Found {total_repos} repositories total")
    
    # Process in smaller batches
    batch_size = 100
    for i in range(0, len(repos), batch_size):
        batch = repos[i:i+batch_size]
        logger.info(f"Processing batch {i//batch_size + 1} ({i+1} to {min(i+batch_size, total_repos)} of {total_repos})")
        
        results = {}
        for owner, repo in batch:
            langs = github_scrape(owner, repo, token)
            if langs and 'Move' in langs:
                results[(owner, repo)] = langs['Move']
            processed += 1
            
            # Show progress
            elapsed = time.time() - start_time
            rate = processed / elapsed
            remaining = (total_repos - processed) / rate if rate > 0 else 0
            logger.info(f"Progress: {processed}/{total_repos} ({processed/total_repos*100:.1f}%) - Est. remaining time: {remaining/60:.1f} minutes")
            
        # Save batch results
        save_results(results, f'output/move_repos_batch_{i//batch_size + 1}.txt')
    
    # After all batches are processed, combine them and cleanup
    compile_and_cleanup_results('output/move_repos_final.txt')

if __name__ == "__main__":
    main()
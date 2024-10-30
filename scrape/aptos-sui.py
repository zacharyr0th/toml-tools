import os
import requests
import time
from typing import Dict, List, Optional
from urllib.parse import urlparse
import toml
from github import Github
from pathlib import Path
from datetime import timedelta

def setup_github_client(token: Optional[str] = None) -> Github:
    if token is None:
        token = os.getenv('GITHUB_TOKEN')
    if not token:
        raise ValueError("GitHub token is required. Set GITHUB_TOKEN environment variable.")
    return Github(token)

def get_move_toml_content(repo_full_name: str, github_client: Github) -> Optional[str]:
    try:
        repo = github_client.get_repo(repo_full_name)
        contents = repo.get_contents("Move.toml")
        if contents:
            return contents.decoded_content.decode('utf-8')
    except:
        return None
    return None

def analyze_dependencies(toml_content: str) -> str:
    try:
        parsed_toml = toml.loads(toml_content)
        dependencies = parsed_toml.get('dependencies', {})
        
        for dep_name in dependencies:
            dep_name_lower = dep_name.lower()
            if any(x in dep_name_lower for x in ['aptos', 'apt-']):
                return 'Aptos'
            if 'sui' in dep_name_lower:
                return 'Sui'
                
        addresses = parsed_toml.get('addresses', {})
        for addr_name, addr_value in addresses.items():
            addr_str = str(addr_value).lower()
            if addr_str.startswith('0x1'):
                return 'Aptos'
            if addr_str.startswith('0x2'):
                return 'Sui'
                
    except:
        pass
    
    return 'Unknown'

def categorize_repo(repo_url: str, github_client: Github) -> str:
    repo_name = repo_url.lower()
    
    if any(x in repo_name for x in ['aptos', 'apt-']):
        return 'Aptos'
    if any(x in repo_name for x in ['sui', 'suins']):
        return 'Sui'
    
    parsed_url = urlparse(repo_url)
    path_parts = parsed_url.path.strip('/').split('/')
    if len(path_parts) >= 2:
        repo_full_name = f"{path_parts[0]}/{path_parts[1]}"
        toml_content = get_move_toml_content(repo_full_name, github_client)
        if toml_content:
            return analyze_dependencies(toml_content)
    
    return 'Unknown'

def analyze_repos(repos: List[str], github_token: Optional[str] = None) -> Dict[str, List[str]]:
    github_client = setup_github_client(github_token)
    
    categorized_repos = {
        'Aptos': [],
        'Sui': [],
        'Unknown': []
    }
    
    total = len(repos)
    start_time = time.time()
    processed = 0
    
    # Calculate and display initial ETA
    test_sample = min(5, total)
    sample_start = time.time()
    for repo in repos[:test_sample]:
        categorize_repo(repo, github_client)
    sample_duration = time.time() - sample_start
    
    estimated_total_time = (sample_duration / test_sample) * total
    eta = timedelta(seconds=int(estimated_total_time))
    print(f"Estimated time to completion: {eta}")
    
    for repo in repos:
        category = categorize_repo(repo, github_client)
        categorized_repos[category].append(repo)
        processed += 1
        
        # Update progress every 10%
        if processed % (total // 10) == 0:
            elapsed = time.time() - start_time
            progress = processed / total
            estimated_total = elapsed / progress
            remaining = estimated_total - elapsed
            eta = timedelta(seconds=int(remaining))
            print(f"{int(progress*100)}% complete. ETA: {eta}")
    
    return categorized_repos

def save_results(categorized_repos: Dict[str, List[str]], output_dir: str = "results"):
    os.makedirs(output_dir, exist_ok=True)
    
    for category, repos in categorized_repos.items():
        output_file = os.path.join(output_dir, f"{category.lower()}_repos.txt")
        with open(output_file, 'w') as f:
            for repo in repos:
                f.write(f"{repo}\n")

def main():
    with open('repos.txt', 'r') as f:
        repos = [line.strip() for line in f if line.strip()]
    
    github_token = os.getenv('GITHUB_TOKEN')
    if not github_token:
        raise ValueError("Please set the GITHUB_TOKEN environment variable")
    
    print(f"Analyzing {len(repos)} repositories...")
    categorized_repos = analyze_repos(repos, github_token)
    
    print("\nResults:")
    print(f"Aptos: {len(categorized_repos['Aptos'])} repos")
    print(f"Sui: {len(categorized_repos['Sui'])} repos")
    print(f"Unknown: {len(categorized_repos['Unknown'])} repos")
    
    save_results(categorized_repos)
    print("Results saved to 'results' directory")

if __name__ == "__main__":
    main()
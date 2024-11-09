import requests
from bs4 import BeautifulSoup
import time
import os
from typing import List, Optional, Dict
from dataclasses import dataclass, field
from enum import Enum
import argparse
import random
import json
import csv
from concurrent.futures import ThreadPoolExecutor, as_completed

@dataclass
class ScraperConfig:
    repo: str
    package_id: Optional[str] = None
    base_url: str = "https://github.com"
    api_url: str = "https://api.github.com"
    delay: float = 1.0
    max_retries: int = 3
    retry_delay: float = 2.0
    output_file: Optional[str] = None
    output_format: str = "txt"
    headers: Dict[str, str] = field(default_factory=lambda: {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/115.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Authorization": f"token {os.getenv('GITHUB_TOKEN')}"
    })

    def __post_init__(self):
        if not self.output_file:
            self.output_file = f"dependents_{self.repo.replace('/', '_')}.{self.output_format}"

def scrape_page(url: str, config: ScraperConfig) -> tuple[List[str], Optional[str]]:
    """Scrape a single page of GitHub dependents."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/115.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Cache-Control": "max-age=0"
    }
    
    if config.headers.get("Authorization"):
        headers["Authorization"] = config.headers["Authorization"]

    for attempt in range(config.max_retries):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")
            
            # Look for repository links in the dependents page
            repos = []
            for row in soup.findAll("div", {"class": "Box-row"}):
                repo_link = row.find("a", {"data-hovercard-type": "repository"})
                if repo_link:
                    repos.append(repo_link["href"].strip("/"))
            
            # Look for the "Next" pagination link
            next_link = None
            pagination = soup.find("div", {"class": "paginate-container"})
            if pagination:
                next_button = pagination.find("a", string="Next")  # Look for the "Next" text
                if next_button:
                    next_link = next_button.get("href")
            
            return repos, next_link
            
        except requests.RequestException as e:
            if attempt == config.max_retries - 1:
                print(f"Error scraping {url}: {e}")
                return [], None
            time.sleep(config.retry_delay)
    
    return [], None

def save_progress_markdown(repos: List[str], stats: dict, config: ScraperConfig):
    """Save the scraping progress and results to a markdown file.

    Args:
        repos (List[str]): List of repository URLs
        stats (dict): Statistics about the scraping process
        config (ScraperConfig): Configuration object containing output parameters
    """
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output")
    os.makedirs(output_dir, exist_ok=True)
    
    md_file = os.path.join(output_dir, f"scraping_results_{config.repo.replace('/', '_')}.md")
    
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write(f"# GitHub Dependents Scraping Results\n\n")
        f.write(f"## Repository: {config.repo}\n\n")
        
        if config.package_id:
            f.write(f"Package ID: {config.package_id}\n\n")
        
        f.write("## Statistics\n\n")
        f.write(f"- Total repositories found: {len(repos)}\n")
        f.write(f"- Time elapsed: {stats['time_elapsed']} seconds\n")
        
        f.write("\n## Dependent Repositories\n\n")
        for repo in repos:
            f.write(f"- {repo}\n")

def scrape_github_dependents(config: ScraperConfig, log_file) -> List[str]:
    """Scrape GitHub dependent repositories for a given repository or package."""
    url_path = f'{config.repo}/network/dependents'
    if config.package_id:
        url_path += f'?package_id={config.package_id}'
    url = f'{config.base_url}/{url_path}'
    
    repos = []
    start_time = time.time()
    page = 1
    
    print(f"Starting to scrape dependents for {config.repo}")
    log_file.write(f"Starting to scrape dependents for {config.repo}\n")

    while url:
        page_repos, next_url = scrape_page(url, config)
        repos.extend(page_repos)
        progress_msg = f"Found {len(repos)} repos (Time elapsed: {int(time.time() - start_time)}s) - Page {page}"
        print(f"\r{progress_msg}", end="")
        log_file.write(f"{progress_msg}\n")
        
        if next_url:
            url = f"{config.base_url}{next_url}" if not next_url.startswith('http') else next_url
            page += 1
        else:
            url = None
            
        time.sleep(config.delay + random.uniform(0, 1))

    elapsed = int(time.time() - start_time)
    done_msg = f"Done! Scraped {len(repos)} repositories in {elapsed} seconds (Total pages: {page})"
    print(f"\n{done_msg}")
    log_file.write(f"{done_msg}\n")
    
    return repos

def save_results(repos: List[str], config: ScraperConfig):
    """Save the scraped repository URLs to a file.

    Args:
        repos (List[str]): List of repository URLs to save
        config (ScraperConfig): Configuration object containing output parameters
    """
    if config.output_file:
        with open(config.output_file, 'w', encoding='utf-8') as f:
            if config.output_format == 'txt':
                f.write('\n'.join(repos))
            elif config.output_format == 'json':
                json.dump(repos, f, indent=2)
            elif config.output_format == 'csv':
                writer = csv.writer(f)
                writer.writerows([[url] for url in repos])

def get_full_repo_name(repo_name: str) -> str:
    """Convert a repository name to its full form.

    Args:
        repo_name (str): Repository name, either short (e.g., 'repo') or full (e.g., 'owner/repo')

    Returns:
        str: Full repository name in the format 'owner/repo'
    """
    return repo_name if '/' in repo_name else f"aptos-labs/{repo_name}"

def scrape_all_package_dependents(config: ScraperConfig) -> List[str]:
    """Scrape dependents for all packages in a repository.

    Args:
        config (ScraperConfig): Configuration object containing scraping parameters

    Returns:
        List[str]: List of all unique dependent repository URLs across all packages
    """
    url = f'{config.base_url}/{config.repo}/network/dependents'
    response = requests.get(url, headers=config.headers, timeout=10)
    soup = BeautifulSoup(response.content, "html.parser")
    packages_dropdown = soup.find("select", {"name": "package_id"})

    if not packages_dropdown:
        print(f"No packages found for {config.repo}, scraping general dependents...")
        return scrape_github_dependents(config)

    all_repos = set()
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = []
        for option in packages_dropdown.find_all("option"):
            package_id = option.get("value")
            package_name = option.text.strip()
            print(f"\nScraping dependents for package: {package_name}")
            package_config = ScraperConfig(
                repo=config.repo,
                package_id=package_id,
                delay=config.delay,
                output_file=None,
                headers=config.headers
            )
            futures.append(executor.submit(scrape_github_dependents, package_config))

        for future in as_completed(futures):
            all_repos.update(future.result())

    print(f"\nTotal unique dependent repositories found: {len(all_repos)}")
    return list(all_repos)

def list_package_ids(config: ScraperConfig) -> Dict[str, str]:
    """List all available packages and their IDs for a repository.

    Args:
        config (ScraperConfig): Configuration object containing repository information

    Returns:
        Dict[str, str]: Dictionary mapping package names to their IDs
    """
    base_url = f'{config.base_url}/{config.repo}/network/dependents'
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/115.0",
        "Accept": "text/html",
        "Authorization": config.headers.get("Authorization", "")
    }
    try:
        response = requests.get(base_url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        packages = {item.find("span", class_="select-menu-item-text").get_text(strip=True): 
                    item.get("href").split("package_id=")[-1]
                    for item in soup.find_all("a", class_="select-menu-item")
                    if "package_id=" in item.get("href", "")}
        
        save_packages_markdown(packages, config)
        return packages
    except requests.RequestException as e:
        print(f"Error fetching packages: {str(e)}")  # Keep error message for debugging
        return {}

def create_repo_output_dir(config: ScraperConfig) -> str:
    """Create and return the path to the repository-specific output directory.

    Args:
        config (ScraperConfig): Configuration object containing repository information

    Returns:
        str: Path to the repository-specific output directory
    """
    # Create base output directory
    base_output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output")
    os.makedirs(base_output_dir, exist_ok=True)
    
    # Create repository-specific directory
    repo_name = config.repo.split('/')[-1]
    repo_output_dir = os.path.join(base_output_dir, repo_name)
    os.makedirs(repo_output_dir, exist_ok=True)
    
    return repo_output_dir

def save_packages_markdown(packages: Dict[str, str], config: ScraperConfig):
    """Save the list of packages to a markdown file.

    Args:
        packages (Dict[str, str]): Dictionary mapping package names to their IDs
        config (ScraperConfig): Configuration object containing repository information
    """
    # Create single output directory for the repository
    repo_name = config.repo.split('/')[-1]
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output", repo_name)
    os.makedirs(output_dir, exist_ok=True)
    
    output_file = os.path.join(output_dir, "packages.md")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"# {config.repo} Packages\n\n")
        f.write(f"Generated on: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("## Available Packages\n\n")
        for package_name, package_id in sorted(packages.items()):
            f.write(f"- {package_name}\n")
            f.write(f"  - ID: `{package_id}`\n")

def search_package_dependents_chain(config: ScraperConfig) -> Dict[str, List[str]]:
    """Search for all packages in a repo and their dependent repositories."""
    repo_name = config.repo.split('/')[-1]
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output", repo_name)
    os.makedirs(output_dir, exist_ok=True)
    
    cli_log_file = os.path.join(output_dir, f"{config.repo.replace('/', '_')}_cli.txt")
    with open(cli_log_file, 'w', encoding='utf-8') as log:
        log.write(f"CLI Output Log for {config.repo}\n")
        log.write(f"Generated on: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        msg = f"Step 1: Finding all packages in {config.repo}..."
        print(f"\n{msg}")
        log.write(f"{msg}\n\n")
        
        packages = list_package_ids(config)
        if not packages:
            msg = "No packages found!"
            print(msg)
            log.write(f"{msg}\n")
            return {}
        
        msg = f"Found {len(packages)} packages"
        print(f"\n{msg}")
        log.write(f"{msg}\n\n")
        
        msg = "Step 2: Searching for repositories dependent on each package..."
        print(f"\n{msg}")
        log.write(f"{msg}\n\n")
        
        results = {}
        all_repos = set()
        
        for package_name, package_id in packages.items():
            msg = f"Searching dependents for {package_name}"
            print(f"\n{msg}")
            log.write(f"{msg}\n")
            
            package_config = ScraperConfig(
                repo=config.repo,
                package_id=package_id,
                delay=config.delay,
                headers=config.headers
            )
            
            start_msg = f"Starting to scrape dependents for {config.repo}"
            print(start_msg)
            log.write(f"{start_msg}\n")
            
            dependents = scrape_github_dependents(package_config, log)
            msg = f"Found {len(dependents)} repositories for {package_name}"
            print(msg)
            log.write(f"{msg}\n\n")
            
            results[package_name] = dependents
            all_repos.update(dependents)
            
            # Save individual package results to markdown
            safe_package_name = package_name.replace('/', '_').replace('@', '').replace('.', '_')
            package_file = os.path.join(output_dir, f"{safe_package_name}.md")
            with open(package_file, 'w', encoding='utf-8') as f:
                f.write(f"# {package_name} Dependents\n\n")
                f.write(f"Generated on: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                f.write(f"Total dependents: {len(dependents)}\n\n")
                f.write("## Dependent Repositories\n\n")
                for dep in sorted(dependents):
                    f.write(f"- {dep}\n")
        
        # Save plain list of all repos to txt file
        repos_txt_file = os.path.join(output_dir, f"{config.repo.replace('/', '_')}_repos.txt")
        with open(repos_txt_file, 'w', encoding='utf-8') as f:
            for repo in sorted(all_repos):
                f.write(f"{repo}\n")
        
        msg = f"\n✓ Results saved to output/{repo_name}/"
        print(msg)
        log.write(f"{msg}\n\n")
        
        # Add final statistics to both console and log
        stats_msg = (
            f"Final Statistics:\n"
            f"Total unique repositories found: {len(all_repos)}\n"
            f"Total packages processed: {len(packages)}\n"
        )
        print(f"\n{stats_msg}")  # Print to console
        log.write(f"{stats_msg}")  # Write to log file
    
    return results

def main():
    parser = argparse.ArgumentParser(description='Scrape GitHub repository dependents')
    parser.add_argument('repo', help='Repository name (e.g., mystenlabs/sui)')
    parser.add_argument('--list-packages', action='store_true', help='List all available packages and their IDs')
    parser.add_argument('--list-repos', action='store_true', help='List all repositories dependent on any package')
    parser.add_argument('--package-id', help='Specific package ID to scrape dependents for')
    parser.add_argument('--package-name', help='Search for dependents of a specific package by name')
    parser.add_argument('--output', help='Output file path')
    parser.add_argument('--format', choices=['txt', 'json', 'csv'], default='txt', help='Output format (default: txt)')
    parser.add_argument('--delay', type=float, default=1.0, help='Delay between requests in seconds (default: 1.0)')
    args = parser.parse_args()

    config = ScraperConfig(
        repo=args.repo,
        package_id=args.package_id,
        output_file=args.output,
        output_format=args.format,
        delay=args.delay
    )

    if args.list_repos:
        print(f"Starting comprehensive package dependency search for {args.repo}")
        search_package_dependents_chain(config)
    elif args.list_packages:
        list_package_ids(config)
    elif args.package_name:
        print(f"Searching dependents for package: {args.package_name}")
        dependents = get_package_dependents(config, args.package_name)
        save_results(dependents, config)
    elif args.package_id:
        print(f"Scraping dependents for package ID: {args.package_id}")
        dependents = scrape_github_dependents(config)
        save_results(dependents, config)
    else:
        print("Please specify an action: --list-repos, --list-packages, --package-name, or --package-id")

if __name__ == '__main__':
    main()
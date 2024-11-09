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
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": f"GitHub-Scraper-{random.randint(1000, 9999)}",
        "Authorization": f"token {os.getenv('GITHUB_TOKEN')}"
    })

    def __post_init__(self):
        if not self.output_file:
            self.output_file = f"dependents_{self.repo.replace('/', '_')}.{self.output_format}"

def scrape_page(url: str, config: ScraperConfig) -> List[str]:
    for attempt in range(config.max_retries):
        try:
            response = requests.get(url, headers=config.headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")
            repos = [f"{config.base_url}{row.find('a', {'data-hovercard-type':'repository'})['href']}"
                     for row in soup.findAll("div", {"class": "Box-row"})
                     if row.find('a', {"data-hovercard-type":"repository"})]
            next_link = soup.find("a", {"class": "next_page"})
            return repos, f"{config.base_url}{next_link['href']}" if next_link else None
        except requests.RequestException as e:
            if attempt == config.max_retries - 1:
                print(f"Error: Failed after {config.max_retries} attempts: {e}")
                return [], None
            time.sleep(config.retry_delay * (attempt + 1))

def scrape_github_dependents(config: ScraperConfig) -> List[str]:
    url_path = f'{config.repo}/network/dependents'
    if config.package_id:
        url_path += f'?package_id={config.package_id}'
    url = f'{config.base_url}/{url_path}'
    
    repos = []
    start_time = time.time()
    print(f"Starting to scrape dependents for {config.repo}")

    while url:
        page_repos, next_url = scrape_page(url, config)
        repos.extend(page_repos)
        print(f"\rFound {len(repos)} repos (Time elapsed: {int(time.time() - start_time)}s)", end="")
        url = next_url
        time.sleep(config.delay + random.uniform(0, 1))

    print(f"\nDone! Scraped {len(repos)} repositories in {int(time.time() - start_time)} seconds")
    save_results(repos, config)
    return repos

def save_results(repos: List[str], config: ScraperConfig):
    if config.output_file:
        with open(config.output_file, 'w') as f:
            if config.output_format == 'txt':
                f.write('\n'.join(repos))
            elif config.output_format == 'json':
                json.dump(repos, f, indent=2)
            elif config.output_format == 'csv':
                writer = csv.writer(f)
                writer.writerows([[url] for url in repos])

def get_full_repo_name(repo_name: str) -> str:
    return repo_name if '/' in repo_name else f"aptos-labs/{repo_name}"

def scrape_all_package_dependents(config: ScraperConfig) -> List[str]:
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
    save_results(list(all_repos), config)
    return list(all_repos)

def list_package_ids(config: ScraperConfig) -> Dict[str, str]:
    base_url = f'{config.base_url}/{config.repo}/network/dependents'
    print(f"Fetching packages from: {base_url}")
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
        for package_name in packages:
            print(f"Found package: {package_name}")
        
        # Save to markdown file
        save_packages_markdown(packages, config)
        return packages
    except requests.RequestException as e:
        print(f"Error fetching packages: {str(e)}")
        return {}

def save_packages_markdown(packages: Dict[str, str], config: ScraperConfig):
    # Go up one directory from scrape/ to the project root
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output")
    output_file = f"{output_dir}/aptos_core_packages.md"
    os.makedirs(output_dir, exist_ok=True)
    
    with open(output_file, 'w') as f:
        f.write("# Aptos Core Package Dependencies\n\n")
        f.write("List of packages that depend on aptos-core:\n\n")
        for package_name in sorted(packages.keys()):
            f.write(f"- {package_name}\n")

def main():
    parser = argparse.ArgumentParser(description='Scrape GitHub repository dependents')
    parser.add_argument('repo', help='Repository name (e.g., aptos-core)')
    parser.add_argument('--list-packages', action='store_true', help='List all available packages and their IDs')
    parser.add_argument('--package-id', help='Specific package ID to scrape dependents for')
    parser.add_argument('--output', help='Output file path (default: dependents_repo.txt)')
    parser.add_argument('--format', choices=['txt', 'json', 'csv'], default='txt', help='Output format (default: txt)')
    parser.add_argument('--delay', type=float, default=1.0, help='Delay between requests in seconds (default: 1.0)')
    args = parser.parse_args()

    full_repo_name = get_full_repo_name(args.repo)
    config = ScraperConfig(
        repo=full_repo_name,
        package_id=args.package_id,
        output_file=args.output,
        output_format=args.format,
        delay=args.delay
    )

    if args.list_packages:
        list_package_ids(config)
    elif args.package_id:
        print(f"Scraping dependents for package ID: {args.package_id}")
        scrape_github_dependents(config)
    else:
        print("Scraping all dependents...")
        scrape_all_package_dependents(config)

if __name__ == '__main__':
    main()
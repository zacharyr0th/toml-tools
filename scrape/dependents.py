import requests
from bs4 import BeautifulSoup
import time
import os

def scrape_github_dependents():
    repo = "aptos-labs/aptos-core"
    package_id = "UGFja2FnZS0zODAxNTY1NTky"  # specific package ID for @aptos-labs/aptos-client
    url = f'https://github.com/{repo}/network/dependents?package_id={package_id}'
    repos = []
    page_num = 1
    start_time = time.time()

    print(f"Starting to scrape dependents for {repo} (@aptos-labs/aptos-client)")
    print(f"Expected total: ~2,696 repositories and 2,149 packages (based on GitHub UI)")

    while True:
        print(f"\rScraping page {page_num}... Found {len(repos)} repos (Time elapsed: {int(time.time() - start_time)}s)", end="")
        
        response = requests.get(url)
        if response.status_code != 200:
            print(f"\nError: {response.status_code}")
            break
            
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Find all repository rows
        for row in soup.findAll("div", {"class": "Box-row"}):
            repo_link = row.find('a', {"data-hovercard-type":"repository"})
            if repo_link:
                repo_url = f"https://github.com{repo_link['href']}"
                repos.append(repo_url)
        
        # Look for "Next" pagination link
        next_link = None
        pagination = soup.find("div", {"class": "paginate-container"})
        if pagination:
            for link in pagination.findAll('a'):
                if link.text == "Next":
                    next_link = link['href']
                    break
        
        if not next_link:
            break
            
        url = next_link
        page_num += 1
        time.sleep(1)  # Be nice to GitHub's servers

    print(f"\nDone! Scraped {len(repos)} repositories in {int(time.time() - start_time)} seconds")
    
    # Write results to file
    with open('dependent_repos.txt', 'w') as f:
        for url in repos:
            f.write(f"{url}\n")

if __name__ == '__main__':
    scrape_github_dependents()
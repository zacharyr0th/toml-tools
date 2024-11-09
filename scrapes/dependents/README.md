# GitHub Dependency Scraper

A Python tool for scraping GitHub repository dependencies and generating comprehensive reports. This tool finds both packages used by a repository and repositories that depend on specific packages.

## Features

- Scrape repositories that depend on a GitHub repository
- List all packages used in a repository 
- Find dependents of specific packages
- Generate reports in multiple formats (TXT, JSON, CSV)
- GitHub token authentication
- Rate limiting and retry logic
- Concurrent processing for performance
- Detailed logging and progress tracking

## Installation

Required Python packages:
- requests 
- beautifulsoup4

Install via pip:
> pip install requests beautifulsoup4

## Usage

| Command | Description | Example |
|---------|-------------|---------|
| `python3 dependents.py owner/repo --list-packages` | List all packages used in a repository | `python3 dependents.py aptos-labs/aptos-core --list-packages` |
| `python3 dependents.py owner/repo --list-repos` | Find all dependent repositories | `python3 dependents.py aptos-labs/aptos-core --list-repos` |
| `python3 dependents.py owner/repo --package-name PACKAGE` | Search for dependents of a specific package | `python3 dependents.py aptos-labs/aptos-core --package-name aptos-NPM` |
| `python3 dependents.py owner/repo --package-id ID` | Search using a specific package ID | `python3 dependents.py aptos-labs/aptos-core --package-id UGFja2FnZS0zMDYzNDc5NjM0` |
| `python3 dependents.py owner/repo --format json` | Output results in JSON format | `python3 dependents.py aptos-labs/aptos-core --list-repos --format json` |
| `python3 dependents.py owner/repo --format csv` | Output results in CSV format | `python3 dependents.py aptos-labs/aptos-core --list-repos --format csv` |

## Authentication

For better rate limits, setup a fine-tuned GitHub token and run this in your CLI:

> export GITHUB_TOKEN=your_token_here

## Output Files

Results are saved in the `output/` directory:

| File | Description |
|------|-------------|
| packages.md | List of detected packages and IDs |
| {owner}_{repo}_repos.txt | Dependent repositories list |
| scraper.log | Detailed execution log |
| {owner}_{repo}_packages.{format} | Package data in specified format |
| {owner}_{repo}_repos.{format} | Repository data in specified format |

## Error Handling 

- Automatic retries for failed requests
- Exponential backoff between retry attempts 
- Rate limit detection and handling
- Detailed error logging

## Notes

- Uses random delays between requests to avoid rate limiting
- GitHub API token recommended for better rate limits
- Both human-readable and machine formats supported
- Logs saved for debugging and auditing
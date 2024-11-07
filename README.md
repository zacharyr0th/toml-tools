# Ecosystem Analysis Tools

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Python tools for analyzing TOML files from Electric Capital's crypto-ecosystems.

## Directory Structure

### /scrape
Repository scraping and dependency analysis tools:
- [`aptos-sui.py`](/scrape/aptos-sui.py): Categorizes scraped Move repos
- [`dependents.py`](/scrape/dependents.py): Analyzes dependencies on specific packages
- [`github_scraper.py`](/scrape/github_scraper.py): Scrapes Move language repos on GitHub
- [`scrape_names.py`](/scrape/scrape_names.py): Extracts repository names

### /scripts
Core analysis and management scripts:

#### Analysis Tools
- [`stats.py`](/scripts/stats.py): Generates repository statistics and ecosystem metrics
- [`report.py`](/scripts/report.py): Creates detailed ecosystem analysis reports like [this](/public/report-example.webp).

#### Repo Management
- [`organize.py`](/scripts/organize.py): Standardizes new TOML entries
- [`rm-sui-solana.py`](/scripts/rm-sui-solana.py): Removes Sui/Solana specific entries
- [`check-repos`](/scripts/check-repos): Checks if repos in a .txt file are in a .toml
- [`merge`](/scripts/merge): Merges new .toml file with the associated Electric Capital .toml file
- [`remove-duplicates`](/scripts/remove-duplicates): Cleans up duplicate entries

### /output
Generated output directory

### /input
A collection of the top .toml files used in Electric Capital's calculations

## Usage
Run each script independently from the command line. See individual script headers for specific usage instructions.

## License
This project is licensed under the MIT License.
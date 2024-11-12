# Ecosystem Analysis Tools

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Python tools for analyzing TOML files from Electric Capital's crypto-ecosystems.

## Directory Structure

### /scrape
Repository scraping and dependency analysis tools:
- [`Dependents`](/scrape/dependents): Analyzes dependencies on specific packages with features:
  - List all packages dependent on a GitHub repository
  - List all repositroes dependent on the packages from step 1
  - Generate reports in multiple formats (MD, TXT, JSON, CSV)
  - Rate limiting and retry logic
  - Concurrent processing for performance - takes ~20 minutes to pull 5,000 repos
- [`Languages`](/scrape/languages): Scrapes Move language repos on GitHub

### /scripts
Core analysis and management scripts:

| Script | Description |
|--------|-------------|
| [`stats.py`](/scripts/stats.py) | Generates repository statistics and ecosystem metrics |
| [`report.py`](/scripts/report.py) | Creates detailed ecosystem analysis reports like [this](/public/report-example.webp) |
| [`organize.py`](/scripts/organize.py) | Standardizes new TOML entries |
| [`rm-sui-solana.py`](/scripts/rm-sui-solana.py) | Removes Sui and Solana specific entries from a .txt file |
| [`check-repos`](/scripts/check-repos) | Checks if repos in a .txt file are in a .toml |
| [`merge`](/scripts/merge) | Merges new .toml file with the associated Electric Capital .toml file |
| [`dedupe`](/scripts/dedupe) | Cleans up duplicate entries from a .txt file |
| [`aptos-sui.py`](/scrape/aptos-sui.py) | Categorizes scraped Move repos |

### /output
Generated output directory. Scripts produce single files, Scrapes produces files within a folder

### /input
A collection of the top 20 .toml files used in Electric Capital's calculations

## Usage
Run each script independently from the command line. See individual script headers for specific usage instructions.

### Dependency Analysis Examples
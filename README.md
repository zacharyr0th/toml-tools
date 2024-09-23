# Ecosystem Analysis Tools

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A few Python scripts for analyzing, categorizing, and organizing TOML files from Electric Capital's [crypto-ecosystems](https://github.com/electric-capital/crypto-ecosystems) directory.

PSA - There is a strong need to fix the categorization filtering in stats.py. The filtering is currently insufficient so the category results in the reports should be taken with a grain of salt. 

## Features

### 1. stats.py

Generates detailed statistics from individual TOML repository files.

**Key features:**
- Generates a detailed report with the following information:
  - Overview
    - Total repositories
    - Valid repositories
    - Missing repositories
    - Unique GitHub accounts
    - Estimated individual accounts
    - Estimated organization/team accounts
  - Ecosystem Analysis
    - Estimated number of repositories in each category
    - Categories: DeFi, Gaming, Social, Infrastructure and Tools, Marketplaces, Unrelated
  - Account Analysis
    - List of repositories by accounts with > 5 contributions
  - Category Analysis
    - Detailed breakdown of repositories in each category
- Generates `<input_filename>-stats-<date>.txt` for each TOML file

### 2. organize.py

Processes TOML files to create standardized **# Repository** sections. 

**Key features:**
- Extracts and normalizes GitHub repository URLs
- Deduplicates and sorts URLs (case-insensitive)
- Formats output in Electric Capital's TOML structure
- Generates `<input>-organized-<date>.toml` for each file

**Usage:**
```
python3 organize/organize.py <file-name>
```
Example:
```
python3 organize/organize.py test
```
Note: Omit the `.toml` extension when specifying the file name.

### 3. report.py

Generates a comprehensive report from all the TOML files in the `input` directory.

[Here's](./output/report-09-13-24.md) the report generated on 09/13/24.

**Key features:**
- Generates a detailed master report with the following information:
  - Overall summary across all ecosystems
    - Total repositories
    - Total unique GitHub accounts
  - Summary table for each ecosystem
    - Total, valid, and missing repositories
    - GitHub accounts (total, individual, and organization)
    - Percentage breakdown of repositories by category
  - Detailed category breakdown for each ecosystem
- Categorizes repositories into: DeFi, Gaming, Social, Infrastructure, NFTs, and Uncategorized
- Generates a single `report-<date>.md` file for all processed TOML files

## Usage

1. Place your TOML files in the `input` directory.

2. Run the desired script:

   - Generate statistics for a specific file:
     ```
     python scripts/stats.py <filename>
     ```
     Replace `<filename>` with the name of the TOML file (without extension).

   - Organize TOML files:
     ```
     python scripts/organize.py
     ```

   - Generate a master report:
     ```
     python scripts/report.py
     ```

## Edit the Categories

You can modify the category definitions and regex patterns in each script to customize the analysis according to your needs. Look for the `categories` dictionary in each script.

## Acknowledgments

- [Electric Capital](https://github.com/electric-capital/crypto-ecosystems) for providing the crypto-ecosystems data.
- All future contributors who will help to improve and maintain this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

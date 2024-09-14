# Ecosystem Analysis Tools

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A few Python scripts for analyzing, categorizing, and organizing TOML files from Electric Capital's [crypto-ecosystems](https://github.com/electric-capital/crypto-ecosystems) directory.

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

Sorts and deduplicates repository sections in TOML files based on Electric Capital's framework.

**Key features:**
- Re-organizes repository sections in TOML files
  - Extracts [[repo]] sections
  - Deduplicates based on URL (case-insensitive)
  - Sorts unique sections alphabetically
  - Reconstructs content with original header and sorted sections
- Generates `<input_filename>-organized-<date>.txt` for each TOML file

### 3. report.py

Generates a comprehensive master report from multiple TOML repository files.

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

## Installation

1. Ensure you have Python 3.7+ installed on your system.

2. Clone the repository:
   ```
   git clone https://github.com/yourusername/ecosystem-analysis-tools.git
   cd ecosystem-analysis-tools
   ```

3. Install required dependencies:
   ```
   pip install -r requirements.txt
   ```

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

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Acknowledgments

- [Electric Capital](https://github.com/electric-capital/crypto-ecosystems) for providing the crypto-ecosystems data.
- All future contributors who will help to improve and maintain this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
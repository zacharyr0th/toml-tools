# Ecosystem Analysis Tools

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A suite of Python scripts for analyzing, categorizing, and organizing TOML files from Electric Capital's [crypto-ecosystems](https://github.com/electric-capital/crypto-ecosystems) directory.

## Organization

- archive - previously generated files & input data 
- scripts
  - merge - tools for merging repository lists
  - report - generates ecosystem analysis reports
  - organize.py - deduplicates and standardizes repository entries
  - stats.py - generates detailed  for individual TOML files

### 1. stats.py

Generates detailed statistics from individual TOML repository files.

**Key features:**
- Comprehensive report generation including:
  - Overview (total repositories, valid/missing repositories, unique GitHub accounts)
  - Ecosystem Analysis (estimated repositories per category)
  - Account Analysis (repositories by accounts with > 5 contributions)
  - Category Analysis (detailed breakdown per category)
- Output: `<input_filename>-stats-<date>.txt`

### 2. organize.py

Processes TOML files to create standardized **# Repository** sections.

**Key features:**
- GitHub repository URL extraction and normalization
- URL deduplication and case-insensitive sorting
- Electric Capital TOML structure formatting
- Output: `<input>-organized-<date>.toml`

### 3. report.py

Generates a comprehensive report from all TOML files in the `input` directory.

**Key features:**
- Overall ecosystem summary (total repositories, unique GitHub accounts)
- Per-ecosystem summary table (repositories, GitHub accounts, category breakdown)
- Comparative table for all ecosystems
- Repository categorization (DeFi, Gaming, Social, Infrastructure, NFTs, Uncategorized)
- Output: `report-<date>.md`

![Ecosystem Analysis Report](archive/public/report-example.webp)

### 4. merge

Tools for merging repository lists:
- Supports merging new repository URLs from .txt files into existing TOML files
- Handles duplicate detection and standardization
- Maintains Electric Capital's TOML format

## Acknowledgments

- [Electric Capital](https://github.com/electric-capital/crypto-ecosystems) for the crypto-ecosystems data.
- Future contributors to this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

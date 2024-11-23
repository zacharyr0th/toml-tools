# Repository Report Scripts

Scripts for generating repository analysis reports for blockchain ecosystem repositories.

## Quick Start

```bash
# Generate basic report for all ecosystems
python -m scripts.report.main

# Generate verbose report for specific ecosystems
python -m scripts.report.main ethereum solana --verbose
```

## File Structure

```
scripts/report/
├── main.py              # Main entry point and CLI handling
├── report_generator.py  # Core report generation logic
├── ecosystem_analyzer.py # Pattern matching and analysis
├── verbose_generator.py # Detailed pattern analysis output
├── constants.py        # Pattern definitions and weights
└── utils.py           # Helper functions
```

## Scripts Overview

### `main.py`

Entry point for report generation with command-line argument handling.

**Features:**
- 📊 Process single or multiple ecosystem TOML files
- 🔍 Optional verbose pattern analysis
- 📁 Automatic output directory management
- 📝 Configurable ecosystem selection

### `report_generator.py`

Generates comprehensive ecosystem analysis reports.

**Capabilities:**
- 📈 Repository categorization
- 👥 Account type analysis (individual vs organization)
- 🔍 Pattern matching across categories
- 📊 Statistical analysis
- 📝 Markdown report generation

## Usage Guide

1. **Basic Report Generation**
   ```bash
   python -m scripts.report.main
   ```
   Generates a report for all TOML files in the input directory

2. **Specific Ecosystem Analysis**
   ```bash
   python -m scripts.report.main ethereum solana polkadot
   ```
   Analyzes only the specified ecosystems

3. **Verbose Analysis**
   ```bash
   python -m scripts.report.main --verbose
   ```
   Includes detailed pattern matching results

## Report Sections

Generated reports include:
- 📊 Overall Statistics
- 🔍 Ecosystem Comparisons
- 📈 Category Analysis
- 👥 Account Distribution
- 📝 Pattern Matching (verbose mode)

## Categories

The analysis includes these primary categories:
- 💰 DeFi & Financial
- 🎨 NFTs & Digital Assets
- 🛠️ Infrastructure & Tools
- 🔐 Identity & Authentication
- 📊 Data & Analytics
- 🎮 Gaming & Entertainment
- 🤝 Social
- 🔒 Security & Privacy

## Output Format

Reports are generated in Markdown format with:
- 📈 Statistical tables
- 📊 Category breakdowns
- 🔍 Pattern analysis (in verbose mode)
- 📝 Repository listings

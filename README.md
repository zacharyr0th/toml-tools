# Ecosystem Analysis Tools

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Python tools for analyzing and interacting with TOML files from Electric Capital's crypto-ecosystemshttps://github.com/electric-capital/crypto-ecosystems directory.

## Directory Structure

### /scrape
Repository scraping and dependency analysis tools:

- [`Dependents`](/scrape/dependents): GitHub dependency analysis with features:
  - List packages used by a repository
  - Find repositories dependent on specific packages
  - Generate reports in multiple formats (MD, TXT, JSON, CSV)
  - GitHub token authentication and rate limiting
  - Concurrent processing (~20 min for 5,000 repos)
  - Detailed logging and progress tracking

- [`DeFi-Llama`](/scrape/defi-llama): DeFi ecosystem data collection and visualization:
  - Fetches protocol details, yields, DEX volumes, and fees
  - Generates comprehensive visualizations
  - Supports multiple chains analysis
  - Includes progress tracking and error handling

- [`Languages`](/scrape/languages): Scrapes Move language repos on GitHub

### /scripts
Core analysis and management scripts:

| Script | Description |
|--------|-------------|
| [`report`](/scripts/report) | Generates detailed ecosystem analysis reports with: <br>- Overall statistics and comparisons<br>- Category analysis (DeFi, NFTs, Infrastructure, etc.)<br>- Account distribution<br>- Pattern matching (verbose mode) |
| [`merge`](/scripts/merge) | Merges new repos with Electric Capital .toml files:<br>- URL normalization and validation<br>- Duplicate removal<br>- TOML format preservation |
| [`check`](/scripts/check) | Cross-references repos between .txt and .toml files:<br>- Supports top 20 ecosystems<br>- Generates detailed comparison reports |
| [`dedupe`](/scripts/dedupe) | Cleans duplicate entries from URL lists:<br>- Timestamp analysis<br>- Statistics generation<br>- Sorted unique output |
| [`/misc/stats.py`](/scripts/stats.py) | Generates repository statistics and ecosystem metrics |
| [`/misc/organize.py`](/scripts/organize.py) | Standardizes new TOML entries |
| [`/misc/make-https.py`](/scrape/aptos-sui.py) | Adds in https:// to each repo in a .txt file |

### /output
Generated output directory:
- /script outputs saved as single files
- /scrapes results organized in subdirectories

### /input
Collection of the top 20 .toml files used in Electric Capital's ecosystem calculations

## Installation

1. Create and activate a virtual environment:
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
.\venv\Scripts\activate
```

2. Install required Python packages:
```bash
pip install requests beautifulsoup4 pandas matplotlib seaborn numpy
# Or install from requirements.txt if available:
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
# Create .env file
touch .env

# Add GitHub token to .env (optional but recommended)
echo "GITHUB_TOKEN=your_token_here" >> .env

# Load environment variables
source .env
```

### Example Commands

```bash
# Generate ecosystem report (from project root)
python -m scripts.report.main ethereum --verbose

# Alternative method:
cd scripts/report
python main.py ethereum --verbose

# Check repositories against TOML
python scripts/check/check_repos.py solana

# Analyze GitHub dependencies
python3 scrape/dependents/dependents.py owner/repo --list-packages

# Collect DeFi data
python scrape/defi-llama/main.py ethereum solana
```

## Detailed Features

### Scraping Tools

#### Dependency Analysis

| Feature | Description |
|---------|-------------|
| Repository Mapping | Comprehensive dependency mapping for repositories |
| Package Analysis | Detailed usage analysis of packages |
| API Handling | Rate-limited requests (~20 min for 5,000 repos) |
| Output Formats | Multiple formats supported (JSON, CSV, TXT, MD) |
| Processing | Concurrent processing with backoff strategy |
| Monitoring | Progress tracking and detailed error logging |

#### DeFi Data Collection

| Feature | Description |
|---------|-------------|
| Protocol Analysis | Metrics and TVL tracking |
| Yield Analysis | Comprehensive pool analysis |
| Volume Tracking | DEX volume monitoring |
| Fee Analysis | Protocol fee calculations |
| Chain Support | Multi-chain compatibility |
| Visualizations | High-resolution outputs (300 DPI) |
| Data Management | Automated organization systems |

### Analysis Scripts

#### Report Generation

| Category | Description |
|----------|-------------|
| 💰 DeFi & Financial | Financial protocols and services |
| 🎨 NFTs & Digital Assets | Digital collectibles and assets |
| 🛠️ Infrastructure & Tools | Development and utility tools |
| 🔐 Identity & Authentication | Identity management solutions |
| 📊 Data & Analytics | Data processing and analysis |
| 🎮 Gaming & Entertainment | Gaming and entertainment platforms |
| 🤝 Social | Social platforms and protocols |
| 🔒 Security & Privacy | Security and privacy solutions |

| Output Type | Description |
|-------------|-------------|
| Statistics | Detailed statistical tables |
| Categories | Comprehensive category breakdowns |
| Patterns | In-depth pattern analysis |
| Repositories | Complete repository listings |
| Accounts | Account distribution metrics |
| Ecosystems | Cross-ecosystem comparisons |

#### Repository Management

| URL Requirements | Status | Description |
|-----------------|--------|-------------|
| HTTPS Protocol | ✅ | Required for all URLs |
| Standard Format | ✅ | Must follow `https://github.com/owner/repo` |
| Branch References | ❌ | No `/tree/` or `/blob/` allowed |
| URL Extras | ❌ | No trailing slashes or quotes |

| Feature | Description |
|---------|-------------|
| URL Processing | Automatic normalization of URLs |
| Duplicate Handling | Detection and removal of duplicates |
| Validation | Comprehensive format validation |
| Sorting | Case-insensitive sorting capability |
| TOML Handling | Structure preservation in TOML files |

#### Error Handling

| Error Type | Description |
|------------|-------------|
| API Issues | Connection failures and timeout handling |
| Rate Limits | Detection and management of rate limits |
| Data Processing | Handling of data processing errors |
| File Operations | Management of file I/O errors |
| URL Validation | Invalid URL format handling |
| Authentication | Authentication failure management |

## Output Directory Structure

output/
├── reports/
│   ├── ecosystem-analysis-{date}.md
│   └── pattern-matching-{date}.md
├── defi-data/
│   ├── {chain}/
│   │   ├── protocols-{date}.csv
│   │   ├── yields-{date}.csv
│   │   └── summary-{date}.csv
│   └── visualizations/
├── dependencies/
│   ├── packages.md
│   ├── {owner}_{repo}_repos.txt
│   └── scraper.log
└── repository-lists/
    └── {ecosystem}-unique-{date}.txt

## Environment Setup

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Set up GitHub token (optional but recommended):
```bash
export GITHUB_TOKEN=your_token_here
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License - see LICENSE file for details
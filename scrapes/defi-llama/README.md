DeFi Llama Data Scraper and Visualizer
=====================================

This project consists of two main components that work together to collect and visualize DeFi ecosystem data from DeFi Llama:

1. main.py: Data collection script
2. visualization.py: Data visualization generator

## MAIN SCRIPT (main.py)

### Overview
The main script fetches comprehensive DeFi data from the DeFi Llama API for specified blockchain ecosystems. It collects information about:
- Protocols and their details
- Yield pools
- DEX volumes
- Protocol fees

### Usage
    python main.py <chains> [--output-dir OUTPUT_DIR]

### Examples:
    python main.py ethereum                    # Single chain
    python main.py ethereum solana arbitrum    # Multiple chains
    python main.py ethereum --output-dir data  # Custom output directory

### Features:
- Robust error handling and retry mechanism
- Rate limiting to respect API constraints
- Organized output structure for single/multiple chains
- Automatic creation of chain-specific subdirectories
- Comprehensive data collection with progress tracking
- Summary statistics generation

Output Structure:
    output/
    └── {chain}-defi-llama-data/
        ├── {chain}/
        │   ├── protocols-{date}.csv
        │   ├── protocol-details-{date}.csv
        │   ├── yields-{date}.csv
        │   ├── dexes-{date}.csv
        │   ├── fees-{date}.csv
        │   └── summary-{date}.csv
        └── visualizations/
            └── [generated plots]

## VISUALIZATION SCRIPT (visualization.py)
------------------------------------

Overview:
The visualization script generates comprehensive analytical visualizations from the collected DeFi Llama data.

Usage:
    python visualization.py <ecosystem>

Example:
    python visualization.py ethereum

Generated Visualizations:

    Protocol Analysis:
    - Top protocols by TVL
    - Protocol category distribution
    - Chain TVL distribution
    - Audit distribution
    - Protocol launch timeline
    - TVL changes analysis
    - Protocol age vs TVL correlation
    - Monthly protocol growth
    - TVL distribution analysis

    DEX Analysis:
    - Top DEXes by daily trading volume

    Yields Analysis:
    - Top pools by APY
    - APY vs TVL distribution

### Features
- Concurrent visualization generation
- Consistent styling and formatting
- Automated file organization
- Comprehensive error handling
- Performance-optimized plotting
- Human-readable number formatting

## DEPENDENCIES
-----------
- pandas
- matplotlib
- seaborn
- requests
- numpy

## INSTALLATION
-----------
    pip install pandas matplotlib seaborn requests numpy

NOTES
-----
- Ensure you have sufficient disk space for data storage
- The API has rate limits; the script includes automatic retry mechanisms
- Large datasets might require significant processing time
- Visualizations are saved in high resolution (300 DPI)
- the output is not yet optimzied so can produce files greater than 100mb

ERROR HANDLING
-------------
Both scripts include comprehensive error handling and logging:
- API connection issues
- Data processing errors
- File I/O operations
- Visualization generation failures
# GitHub Repository URL Deduplicator

Takes in and deduplicates .txt files with lists of URLs corresponding to Github repos. 

## Quick Start
```bash
python3 scripts/dedupe/dedupe.py <ecosystem>
```

## Installation & Setup
1. Clone this repository, have python setup
2. Place your list of GitHub repository URLs in `potential-duplicates.txt`
3. Run the command with the ecosystem name as the argument
4. Check the output file in `output/<ecosystem>-unique-YY-MM-DD.txt`

## Supported Ecosystems
- Includes top 20 ecosystem TOML files from Electric Capital's 2024 mid-year [Developer Report](https://www.developerreport.com/)
- Use name of the file as the argument (e.g 'cosmos-ecosystem' rather than 'cosmos')
- New ecosystems require manual TOML file addition

## Example Usage
```bash
python3 scripts/dedupe/dedupe.py aptos
```

### CLI Output
```
Found 1500 total URLs
Found 1200 unique repositories
Removed 300 duplicates
Results written to: output/aptos-unique-24-03-15.txt
```

## Output Details
The generated output file includes:
- Timestamp of analysis
- Total URLs analyzed
- Number of unique repositories
- Number of duplicates removed
- Percentage of duplicates
- Sorted list of unique repository URLs

View complete results in [`output/aptos-check-24-11-12.txt`](../../output/aptos-check-24-11-12.txt)
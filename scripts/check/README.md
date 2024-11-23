# GitHub Repository Checker for Ecosystem TOML Files

Checks if the URLs in new-repos.txt are in a specific .toml file in the /input directory. 

## Quick Start
```bash
python3 scripts/check-repos/check_repos.py <ecosystem>
```
## Installation & Setup
1. Clone this repository, have python setup
2. Erase everything in [`new-repos.txt`](./new-repos.txt) and add in your list of GitHub repository URLs that you want to cross-reference with the .toml file
3. type in the commmand with the name of the ecosystem as the argument like the example below 
4. Check the output file in `toml-tools/output/<ecosystem>_check_results.txt`

## Supported Ecosystems
- Includes top 20 ecosystem TOML files from Electric Capital's 2024 mid-year [Developer Report](https://www.developerreport.com/)
- Use name of the file as the argument (e.g 'cosmos-ecosystem' rather than 'cosmos')
- New ecosystems require manual TOML file addition

## Example Usage
```bash
python3 scripts/check-repos/check_repos.py solana
```

### CLI Output
```
Found 49505 unique repositories in solana.toml
Found 6241 unique repositories in new-repos.txt
Results written to: output/solana_check_results.txt
Total repos already in solana.toml: 2681
Total repos not in solana.toml: 3560
```

View complete results in [`output/solana-check-24-11-12.txt`](../../output/solana-check-24-11-12.txt)
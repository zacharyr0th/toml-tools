def read_repo_list(filename):
    repos = set()
    with open(filename, 'r') as f:
        for line in f:
            if line.strip() and not line.strip().endswith('|'):  # Skip empty lines and line numbers
                repos.add(line.strip())
    return repos

def filter_solana_sui(repos):
    """Filter out repositories containing 'solana' or 'sui' (case insensitive)"""
    return {repo for repo in repos 
            if 'solana' not in repo.lower() 
            and 'sui' not in repo.lower()}

def main():
    # Read both files
    not_in_aptos = read_repo_list('scripts/check/quick-check/not-in-aptos.txt')
    removed_repos = read_repo_list('scripts/check/quick-check/removed-repos.txt')
    
    # Find repos that are in not_in_aptos but not in removed_repos
    final_repos = not_in_aptos - removed_repos
    
    # Filter out solana and sui repositories
    filtered_repos = filter_solana_sui(final_repos)
    
    # Print results
    print(f"not-in-aptos.txt contains {len(not_in_aptos)} repositories")
    print(f"removed-repos.txt contains {len(removed_repos)} repositories")
    print(f"Found {len(final_repos)} repositories that are only in not-in-aptos.txt")
    print(f"After filtering solana/sui: {len(filtered_repos)} repositories remain")
    
    # Write filtered repos to a file
    output_file = 'scripts/check/quick-check/unique-new-repos.txt'
    with open(output_file, 'w') as f:
        for repo in sorted(filtered_repos):
            f.write(f"{repo}\n")
    
    print(f"\nFinal repository list has been saved to {output_file}")

if __name__ == "__main__":
    main()

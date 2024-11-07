def filter_repos(input_path, output_path):
    """Filter repositories by removing entries containing 'solana' or 'sui' keywords.

    Args:
        input_path (str): Path to input file containing repository URLs
        output_path (str): Path to output file for filtered repository URLs
    """
    with open(input_path, 'r', encoding='utf-8') as f:
        repos = f.readlines()

    filtered_repos = []
    for repo in repos:
        # Skip empty lines
        if not repo.strip():
            continue
            
        # Remove line numbers if they exist
        if '|' in repo:
            repo = repo.split('|')[-1]
            
        # Check if URL contains solana or sui (case insensitive)
        if 'solana' not in repo.lower() and 'sui' not in repo.lower():
            filtered_repos.append(repo)

    # Write filtered repos to output file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.writelines(filtered_repos)

    print(f"Filtered out {len(repos) - len(filtered_repos)} repositories containing 'solana' or 'sui'")
    print(f"Remaining repositories: {len(filtered_repos)}")

if __name__ == "__main__":
    input_file = 'repos.txt'
    output_file = 'repos_filtered.txt'
    
    try:
        filter_repos(input_file, output_file)
        print(f"Processed {input_file} -> {output_file}")
    except FileNotFoundError:
        print(f"File not found: {input_file}")
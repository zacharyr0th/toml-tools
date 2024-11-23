# Read the input file and convert repo names to full GitHub URLs
with open('output/aptos-core/aptos-labs_aptos-core_repos.txt', 'r', encoding='utf-8') as input_file:
    repos = input_file.readlines()

# Create full URLs and write to new file
with open('output/aptos-core/aptos-labs_aptos-core_repos_urls.txt', 'w', encoding='utf-8') as output_file:
    for repo in repos:
        repo = repo.strip()  # Remove whitespace/newlines
        if repo:  # Skip empty lines
            url = f"https://github.com/{repo}"
            output_file.write(url + '\n')

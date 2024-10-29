import re
import logging
from urllib.parse import urlparse, urlunparse

def clean_url(url: str) -> str:
    """Clean and normalize GitHub repository URLs."""
    # Remove trailing quotes and slashes
    url = url.strip('"').rstrip('/')
    
    # Remove trailing slashes and ensure https
    url = ensure_https(url)
    
    # Parse the URL
    parsed = urlparse(url)
    
    # Extract path components
    path_parts = parsed.path.strip('/').split('/')
    
    # Keep only the first two path components (username/repo)
    if len(path_parts) >= 2:
        clean_path = '/'.join(path_parts[:2])
    else:
        return ''  # Invalid URL
    
    # Reconstruct the URL
    cleaned = urlunparse(('https', 'github.com', f'/{clean_path}', '', '', ''))
    
    return cleaned

def ensure_https(url: str) -> str:
    """Ensure the URL starts with https://."""
    return f'https://{url}' if url and not url.startswith(('http://', 'https://')) else url

def is_valid_repo_url(url: str) -> bool:
    """Check if the URL is a valid GitHub repository URL."""
    pattern = r'^https://github\.com/[^/]+/[^/]+$'
    return bool(re.match(pattern, url))

def extract_urls(content: str) -> set[str]:
    """Extract and normalize GitHub repository URLs from the content."""
    # Modified pattern to capture URLs including trailing quotes
    url_pattern = r'(?:https?://)?github\.com/[^\s"]+(?:")?'
    urls = set(re.findall(url_pattern, content))
    return {clean_url(url) for url in urls if is_valid_repo_url(clean_url(url))}

def extract_account_name(url: str) -> str:
    """Extract the full URL for case-insensitive sorting."""
    return url.lower()

def generate_toml(urls: list[str]) -> str:
    """Generate TOML-formatted string from a list of URLs, sorted case-insensitively."""
    # Sort URLs case-insensitively by the entire URL
    sorted_urls = sorted(urls, key=extract_account_name)
    toml_content = ""
    for url in sorted_urls:
        # Remove any trailing quotes from the URL
        url = url.rstrip('"')
        toml_content += f'[[repo]]\nurl = "{url}"\n\n'
    return toml_content

def merge_repos():
    # Read the existing aptos.toml file
    with open('aptos.toml', 'r', encoding='utf-8') as f:
        existing_content = f.read()

    # Extract existing repos
    existing_repos = extract_urls(existing_content)

    # Read the new repos from new-repos.txt
    with open('new-repos.txt', 'r', encoding='utf-8') as f:
        new_content = f.read()

    # Extract new repos
    new_repos = extract_urls(new_content)

    # Merge repos
    all_repos = existing_repos.union(new_repos)

    # Remove empty strings (invalid URLs)
    all_repos = {url for url in all_repos if url}

    # Generate new repo section
    new_repo_section = generate_toml(list(all_repos))

    # Replace the existing repo section with the new one
    repo_section_pattern = r'# Repositories\n((?:\[\[repo\]\][\s\S]*?\n\n)*)'
    updated_content = re.sub(repo_section_pattern, f'# Repositories\n{new_repo_section}', existing_content)

    # Write the updated content to new-aptos.toml
    with open('new-aptos.toml', 'w', encoding='utf-8') as f:
        f.write(updated_content)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    
    merge_repos()
    logging.info("Merge complete. New repos have been added to new-aptos.toml.")
    
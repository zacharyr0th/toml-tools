"""Module for sorting and deduplicating repository sections in TOML files."""
import os
from datetime import datetime
import logging
import argparse
import sys
import re

def ensure_https(url: str) -> str:
    """Ensure the URL starts with https:// and remove trailing slashes."""
    url = url.rstrip('/')
    return f'https://{url}' if url and not url.startswith(('http://', 'https://')) else url

def is_valid_repo_url(url: str) -> bool:
    """Check if the URL is a valid GitHub repository URL."""
    pattern = r'^https://github\.com/[^/]+/[^/]+$'
    return bool(re.match(pattern, url))

def extract_urls(content: str) -> set[str]:
    """Extract and normalize GitHub repository URLs from the content."""
    url_pattern = r'(?:https?://)?github\.com/[^\s]+'
    urls = set(re.findall(url_pattern, content))
    return {ensure_https(url) for url in urls if is_valid_repo_url(ensure_https(url))}

def extract_account_name(url: str) -> str:
    """Extract the account name from a GitHub repository URL."""
    return url.split('/')[-2].lower()

def generate_toml(urls: list[str]) -> str:
    """Generate TOML-formatted string from a list of URLs, sorted by account name (case-insensitive)."""
    sorted_urls = sorted(urls, key=extract_account_name)
    toml_content = "# Repositories\n"
    for url in sorted_urls:
        toml_content += f'[[repo]]\nurl = "{url}"\n\n'
    return toml_content

def main() -> None:
    """Parse command-line arguments and organize the specified TOML file."""
    parser = argparse.ArgumentParser(
        description="Sort and deduplicate repository sections in a TOML file."
    )
    parser.add_argument("toml_file", help="Name of the TOML file (without extension)")
    args = parser.parse_args()

    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'output')
    os.makedirs(output_dir, exist_ok=True)

    current_date = datetime.now().strftime('%Y-%m-%d')
    file_name = f'organized-test-{current_date}.txt'
    organized_output_path = os.path.join(output_dir, file_name)

    toml_input_path = os.path.join('input', f"{args.toml_file}.toml")
    if not os.path.exists(toml_input_path):
        logging.error("File %s not found.", toml_input_path)
        sys.exit(1)

    with open(toml_input_path, 'r', encoding='utf-8') as f:
        content = f.read()

    urls = extract_urls(content)
    organized_output = generate_toml(list(urls))  # Convert set to list

    with open(organized_output_path, 'w', encoding='utf-8') as f:
        f.write(organized_output)

    logging.info("Organized TOML file saved as %s", organized_output_path)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    main()
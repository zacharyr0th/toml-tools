"""Module for sorting and deduplicating repository sections in TOML files."""
import re
import os
from datetime import datetime
import logging

def process_toml(input_file, output_file):
    """Sort and deduplicate repository sections in a TOML file based on URL."""
    # Read the file
    with open(input_file, 'r', encoding='utf-8') as file:
        content = file.read()

    # Extract all [[repo]] sections
    repo_sections = re.findall(r'(?:\n|^)\[\[repo\]\].*?(?=\n\[\[|\Z)', content, re.DOTALL)

    # Deduplicate and sort the sections based on the URL
    unique_sections = {}
    for section in repo_sections:
        url_match = re.search(r'url\s*=\s*"(.*?)"', section)
        if url_match:
            url = url_match.group(1).lower()
            unique_sections[url] = section.strip()

    sorted_sections = sorted(
        unique_sections.values(),
        key=lambda x: re.search(r'url\s*=\s*"(.*?)"', x).group(1).lower()
    )

    # Reconstruct the file content
    header = content.split('[[repo]]')[0].strip()
    sorted_content = f"{header}\n\n" + '\n\n'.join(sorted_sections)

    # Write the processed content to the output file
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(sorted_content)

# Set up logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

# Get current date in MM-DD-YY format
current_date = datetime.now().strftime("%m-%d-%y")

# Create 'output' folder if it doesn't exist
os.makedirs('output', exist_ok=True)

# Process all .toml files in the 'tomls' folder
for filename in os.listdir('tomls'):
    if filename.endswith('.toml'):
        input_path = os.path.join('tomls', filename)
        output_filename = f"{os.path.splitext(filename)[0]}-stats-{current_date}.txt"
        output_path = os.path.join('output', output_filename)
        process_toml(input_path, output_path)
        logging.info("Report generated: %s", output_path)
        logging.info("Generated stats for %s -> %s", filename, output_filename)

logging.info("Statistics have been generated and saved in the 'output' folder.")

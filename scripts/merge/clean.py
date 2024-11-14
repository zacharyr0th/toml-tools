import re

def clean_duplicates(file_path):
    # Set to store unique URLs (normalized)
    unique_urls = set()
    # List to store cleaned lines
    cleaned_lines = []
    # Flag to track if we're in a repo block
    in_repo_block = False
    current_block = []
    
    def normalize_url(url):
        # Remove trailing slashes
        url = url.rstrip('/')
        # Convert to lowercase for comparison
        return url.lower()
    
    def is_valid_block(block):
        # Check for required fields
        url_line = next((l for l in block if l.startswith('url = ')), None)
        if not url_line:
            return False
            
        # Extract URL and normalize
        url = url_line.split('=')[1].strip().strip('"\'')
        
        # Skip if URL contains unwanted patterns
        if any(x in url.lower() for x in ['/tree/', '/blob/']):
            return False
            
        # Skip if URL has extra path components beyond owner/repo
        path_parts = url.split('github.com/')[-1].split('/')
        if len(path_parts) > 2:
            return False
            
        return True
    
    # Read the file
    with open(file_path, 'r') as file:
        for line in file:
            if line.strip() == '[[repo]]':
                if in_repo_block:
                    # Process previous block
                    if is_valid_block(current_block):
                        url_line = next(l for l in current_block if l.startswith('url = '))
                        norm_url = normalize_url(url_line.strip())
                        if norm_url not in unique_urls:
                            unique_urls.add(norm_url)
                            cleaned_lines.extend(['[[repo]]'] + current_block)
                # Start new block
                in_repo_block = True
                current_block = []
            elif in_repo_block:
                current_block.append(line.strip())
            else:
                cleaned_lines.append(line.strip())
    
    # Process the last block if exists
    if current_block and is_valid_block(current_block):
        url_line = next(l for l in current_block if l.startswith('url = '))
        norm_url = normalize_url(url_line.strip())
        if norm_url not in unique_urls:
            unique_urls.add(norm_url)
            cleaned_lines.extend(['[[repo]]'] + current_block)
    
    # Write back to file
    with open(file_path, 'w') as file:
        for line in cleaned_lines:
            file.write(line + '\n')

    return len(unique_urls)

if __name__ == "__main__":
    file_path = "scripts/merge/new-aptos.toml"
    unique_count = clean_duplicates(file_path)
    print(f"Cleaned file. Found {unique_count} unique repositories.")

import os
import shutil
from pathlib import Path

def consolidate_llama_csvs():
    # Define paths - going up one directory to find the project root
    project_root = Path(__file__).parent.parent
    output_dir = project_root / 'output'
    consolidated_dir = output_dir / 'consolidated_llama_csvs'
    
    print(f"Looking for files in: {output_dir}")
    
    # Create consolidated directory if it doesn't exist
    consolidated_dir.mkdir(parents=True, exist_ok=True)
    
    # Counter for found files
    counter = 0
    
    # Walk through output directory
    for root, dirs, files in os.walk(output_dir):
        # Check if current directory contains 'defi-llama'
        if 'defi-llama' in root.lower():
            print(f"\nChecking directory: {root}")
            # Look for any file that starts with 'protocols-' and ends with '.csv'
            protocol_files = [f for f in files if f.startswith('protocols-') and f.endswith('.csv')]
            
            if protocol_files:
                # Get the most recent file
                latest_file = max(protocol_files)
                csv_path = Path(root) / latest_file
                print(f"Found: {csv_path}")
                
                # Get the chain name from the directory path
                chain_name = root.split('defi-llama-data')[0].split('/')[-1].replace('-', '_')
                dest_path = consolidated_dir / f'protocols_{chain_name}.csv'
                
                # Copy the file
                shutil.copy2(csv_path, dest_path)
                print(f"Copied to: {dest_path}")
                counter += 1

    if counter == 0:
        print("\nNo matching files were found!")
    else:
        print(f"\nSuccessfully copied {counter} files to {consolidated_dir}")

if __name__ == "__main__":
    try:
        consolidate_llama_csvs()
        print("Process completed successfully!")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

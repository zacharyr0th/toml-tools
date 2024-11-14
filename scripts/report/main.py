import sys
import os
import logging
from datetime import datetime
import argparse
# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from report.report_generator import generate_master_report

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Generate ecosystem comparison reports.')
    parser.add_argument('ecosystems', nargs='*', help='List of ecosystems to compare')
    parser.add_argument('--verbose', action='store_true', help='Include verbose output in report')
    return parser.parse_args()

def get_toml_files(ecosystems):
    """Convert ecosystem names to their corresponding TOML file paths."""
    # Get the absolute path to the project root directory
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    input_dir = os.path.join(project_root, "input")
    
    if not ecosystems:
        # Return all TOML files if no ecosystems specified
        return [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.endswith(".toml")]
    
    return [os.path.join(input_dir, f"{ecosystem}.toml") for ecosystem in ecosystems]

def main() -> None:
    """Generate a report comparing specific TOML files.
    
    Usage: python scripts/report/main.py [ecosystem1] [ecosystem2] ... [ecosystem6]
    Example: python scripts/report/main.py ethereum solana polkadot
    """
    args = parse_args()
    toml_files = get_toml_files(args.ecosystems)
    current_date = datetime.now().strftime("%m-%d-%y")
    
    # Determine filename based on number of ecosystems
    if not args.ecosystems:  # Case 1: No arguments
        output_filename = f"report{'-verbose' if args.verbose else ''}-{current_date}.md"
    elif len(args.ecosystems) == 1:  # Case 2: Single ecosystem
        output_filename = f"report-{args.ecosystems[0]}{'-verbose' if args.verbose else ''}-{current_date}.md"
    else:  # Case 3: Multiple ecosystems
        eco_names = "-".join(args.ecosystems)
        output_filename = f"comparison-{eco_names}{'-verbose' if args.verbose else ''}-{current_date}.md"
    
    output_path = os.path.join("output", output_filename)
    
    generate_master_report(toml_files, output_path, verbose=args.verbose)
    logging.info("Generated report -> %s", output_filename)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    main()

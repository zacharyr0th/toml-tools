import argparse
import logging
import os
from datetime import datetime
from .report_generator import generate_master_report
from .ecosystem_analyzer import analyze_ecosystem_patterns
from .categories import CategoryRegistry

def main():
    parser = argparse.ArgumentParser(description='Generate repository analysis report with keyword search.')
    parser.add_argument('ecosystems', nargs='*', help='Names of ecosystem TOML files to analyze. If none provided, all TOML files will be processed.')
    parser.add_argument('--verbose', action='store_true', help='Generate detailed pattern analysis')
    parser.add_argument('--keyword', '-k', type=str, help='Keyword to search for in repository names and URLs')
    parser.add_argument('--category', '-c', type=str, help='Filter by specific category (e.g., DeFi, NFT, Gaming)')
    parser.add_argument('--output', '-o', type=str, help='Custom output filename')
    args = parser.parse_args()

    current_date = datetime.now().strftime("%m-%d-%y")
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    input_dir = os.path.join(project_root, 'input')
    output_dir = os.path.join(project_root, 'output')
    
    os.makedirs(output_dir, exist_ok=True)

    if not os.path.exists(input_dir):
        logging.error("Input folder '%s' does not exist.", input_dir)
        logging.info("Current working directory: %s", os.getcwd())
        logging.info("Please make sure you're running the script from the correct directory.")
        return

    # Get TOML files based on arguments
    if args.ecosystems:
        # Process specified ecosystems
        toml_files = []
        for eco in args.ecosystems:
            file_path = os.path.join(input_dir, f"{eco}.toml")
            if os.path.exists(file_path):
                toml_files.append(file_path)
            else:
                logging.warning(f"Ecosystem file not found: {eco}.toml")
    else:
        # Process all TOML files in the input directory
        toml_files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) 
                     if f.endswith('.toml')]
        logging.info(f"No ecosystems specified, processing all {len(toml_files)} TOML files found in input directory")

    if not toml_files:
        logging.error("No .toml files found to process.")
        return

    # Create output filename
    if args.output:
        output_filename = args.output if args.output.endswith('.md') else f"{args.output}.md"
    else:
        components = []
        if args.ecosystems:
            components.append(f"comparison-{'-'.join(args.ecosystems)}")
        else:
            components.append("report-all")
        
        if args.keyword:
            components.append(f"keyword-{args.keyword}")
        if args.category:
            components.append(f"category-{args.category}")
        if args.verbose:
            components.append("verbose")
        
        components.append(current_date)
        output_filename = f"{'-'.join(components)}.md"
    
    output_path = os.path.join(output_dir, output_filename)
    
    # Generate report with search parameters
    generate_master_report(
        toml_files, 
        output_path, 
        verbose=args.verbose,
        keyword=args.keyword,
        category_filter=args.category
    )
    
    logging.info("Generated report -> %s", output_filename)
    logging.info("Report has been saved in the 'output' folder.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    main()

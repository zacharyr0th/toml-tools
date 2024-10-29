import sys
import os
import logging
from datetime import datetime
# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from report.report_generator import generate_master_report

def main() -> None:
    """Generate a single report for all TOML files in the input folder."""
    current_date = datetime.now().strftime("%m-%d-%y")
    os.makedirs('output', exist_ok=True)

    input_folder = 'input'
    
    if not os.path.exists(input_folder):
        logging.error("Input folder '%s' does not exist.", input_folder)
        logging.info("Current working directory: %s", os.getcwd())
        logging.info("Please make sure you're running the script from the correct directory.")
        sys.exit(1)

    try:
        toml_files = [os.path.join(input_folder, f) for f in os.listdir(input_folder) if f.endswith('.toml')]
    except OSError as e:
        logging.error("Error accessing the input folder: %s", e)
        sys.exit(1)

    if not toml_files:
        logging.error("No .toml files found in the input folder.")
        sys.exit(1)

    output_filename = f"report-{current_date}.md"
    output_path = os.path.join('output', output_filename)
    
    generate_master_report(toml_files, output_path)
    logging.info("Generated report for all TOML files -> %s", output_filename)

    logging.info("Report has been generated for all TOML files and saved in the 'output' folder.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    main()

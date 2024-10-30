import argparse
from .categories import generate_category_lists

def main():
    parser = argparse.ArgumentParser(description="Generate category-based repository lists")
    parser.add_argument("input_folder", help="Folder containing input TOML files")
    parser.add_argument("output_folder", help="Folder to store output category files")
    args = parser.parse_args()

    generate_category_lists(args.input_folder, args.output_folder)

if __name__ == "__main__":
    main()


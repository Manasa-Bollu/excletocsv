import pandas as pd
import os
import sys
from pathlib import Path
from typing import List

OUTPUT_DIR = Path("version_history")

def process_file(excel_file: Path):
    """
    Reads an Excel file, converts each sheet to a CSV file, and saves it
    to the output directory.
    """
    if not excel_file.is_file():
        print(f"File not found: {excel_file}")
        return

    print(f"Processing {excel_file}...")
    try:
        xl = pd.ExcelFile(excel_file)
        base_name = excel_file.stem  # Gets filename without extension
        
        for sheet_name in xl.sheet_names:
            df = xl.parse(sheet_name)

            # Replace newlines in object columns to prevent multi-line rows in CSV
            for col in df.select_dtypes(include=['object']):
                df[col] = df[col].astype(str).str.replace('\r\n', ' ', regex=False).str.replace('\n', ' ', regex=False)
            
            # Sanitize sheet_name for use in filename
            safe_sheet_name = "".join(c for c in sheet_name if c.isalnum() or c in (' ', '_')).rstrip()

            if len(xl.sheet_names) == 1:
                csv_filename = f"{base_name}.csv"
            else:
                csv_filename = f"{base_name}_{safe_sheet_name}.csv"
            
            csv_path = OUTPUT_DIR / csv_filename
            df.to_csv(csv_path, index=False)
            print(f"  -> Saved {csv_path}")
    except Exception as e:
        print(f"Error processing {excel_file}: {e}")

def main(files: List[str]):
    """Main function to process a list of Excel files."""
    OUTPUT_DIR.mkdir(exist_ok=True)

    if not files:
        print("No Excel files provided to the script. Exiting.")
        return

    for file_path in files:
        process_file(Path(file_path))

if __name__ == "__main__":
    main(sys.argv[1:])

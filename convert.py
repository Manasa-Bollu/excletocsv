import pandas as pd
import os
import sys

# 1. Define and create the output directory
output_dir = "version_history"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 2. Get files from command line arguments (passed by xargs)
excel_files = sys.argv[1:]

if not excel_files:
    print("No Excel files provided to the script!")
    sys.exit(0)

for excel_file in excel_files:
    if not os.path.exists(excel_file):
        print(f"File not found: {excel_file}")
        continue

    print(f"Processing {excel_file}...")
    xl = pd.ExcelFile(excel_file)
    base_name = os.path.basename(excel_file).replace(".xlsx", "")
    
    for sheet_name in xl.sheet_names:
        df = xl.parse(sheet_name)
        
        if len(xl.sheet_names) == 1:
            csv_filename = f"{base_name}.csv"
        else:
            csv_filename = f"{base_name}_{sheet_name}.csv"
        
        csv_path = os.path.join(output_dir, csv_filename)
        df.to_csv(csv_path, index=False)
        print(f"  -> Saved {csv_path}")
#!/bin/bash
set -euo pipefail

# 1. Get changed files (comparing current commit to previous)
changed_files=$(git diff --name-only HEAD^..HEAD)

echo "--- Changed Files List ---"
echo "$changed_files"
echo "--------------------------"

touch files_to_process.txt

for file in $changed_files; do
  # Check if it's an .xlsx file AND it actually exists in the current checkout
  if [[ $file == *.xlsx ]] && [[ -f "$file" ]]; then
      echo "Condition met for: $file"
      echo "$file" >> files_to_process.txt
  fi
done

if [ -s files_to_process.txt ]; then
    echo "Starting conversion for modified files..."
    # This sends only the specific files found to the python script
    xargs -a files_to_process.txt python3 convert.py
else
    echo "No valid .xlsx files found in this commit. Skipping."
fi
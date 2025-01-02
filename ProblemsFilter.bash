#!/bin/bash

# Directory containing the files
DIRECTORY="Files/Problems"

# Iterate through all files in the directory (only regular files)
for file in "$DIRECTORY"/*; do
    if [ -f "$file" ]; then
        # Check if the file does not contain the required lines
        if ! grep -q "EDGE_WEIGHT_TYPE : EUC_2D" "$file" || ! grep -q "TYPE : TSP" "$file"; then
            # Remove the file if it doesn't meet the criteria
            rm "$file"
        fi
    fi
done

echo "Files not matching the criteria have been removed from $DIRECTORY."
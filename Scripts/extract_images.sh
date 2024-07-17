#!/bin/bash

# Create the images directory if it doesn't exist
mkdir -p images

# Loop through all PDF files in the current directory
for pdf in *.pdf; do
    # Extract the date from the filename
    date=$(echo "$pdf" | grep -oP '\d{4}-\d{2}-\d{2}')
    
    if [ -z "$date" ]; then
        echo "Skipping $pdf: No date found in filename"
        continue
    fi
    
    # Initialize counter for this PDF
    counter=1
    
    # Use pdfimages to extract images, storing them in a temporary directory
    temp_dir=$(mktemp -d)
    pdfimages -all "$pdf" "$temp_dir/img"
    
    # Move and rename the extracted images
    for img in "$temp_dir"/*; do
        # Get the file extension
        ext="${img##*.}"
        
        # Move and rename the image
        mv "$img" "images/${date}_${counter}.${ext}"
        
        # Increment counter
        ((counter++))
    done
    
    # Remove the temporary directory
    rm -rf "$temp_dir"
    
    echo "Processed $pdf: Extracted $((counter-1)) images"
done

echo "Image extraction complete. All images are in the 'images' directory."

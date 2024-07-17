#!/bin/bash

# Create a new directory for the renamed files
mkdir -p renamed_files

# Copy all jpg files to the new directory
cp *.jpg renamed_files/

# Change to the new directory
cd renamed_files

# Remove the first two files (blank pages)
rm 1765-01-04_1.jpg 1765-01-04_2.jpg

# Initialize variables
issue_number=0
page_number=1
global_page_number=1

# Function to pad numbers with leading zeros
pad() {
    printf "%03d" $1
}

# Sort files by name (which will sort them chronologically)
for file in $(ls -1 1765-*.jpg | sort); do
    # Extract date from filename
    date=$(echo $file | grep -oP '\d{4}-\d{2}-\d{2}')
    
    # If it's a new date, increment issue number and reset page counter
    if [[ $date != $current_date ]]; then
        current_date=$date
        issue_number=$((issue_number + 1))
        page_number=1
        pages_in_issue=$(ls -1 $date*.jpg | wc -l)
    fi
    
    # Create new filename based on number of pages in the issue and the issue number
    if [ $issue_number -eq 27 ] || [ $pages_in_issue -le 4 ]; then
        new_name="1765-$(pad $issue_number)-$(pad $global_page_number).jpg"
        global_page_number=$((global_page_number + 1))
    else
        if [ $page_number -le 2 ] || [ $page_number -gt $((pages_in_issue - 2)) ]; then
            new_name="1765-$(pad $issue_number)-$(pad $global_page_number).jpg"
            global_page_number=$((global_page_number + 1))
        else
            new_name="1765-$(pad $issue_number)b-$(pad $((page_number - 2))).jpg"
        fi
    fi
    
    # Rename file
    mv "$file" "$new_name"
    
    # Increment page number
    page_number=$((page_number + 1))
done

echo "Files have been renamed in the 'renamed_files' directory."

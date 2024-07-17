#!/bin/bash

# Create a new directory for the renamed files
mkdir -p renamed_files

# Copy all jpg files to the new directory
cp *.jpg renamed_files/

# Change to the new directory
cd renamed_files

# Function to calculate days between two dates
days_between() {
    date1=$(date -d "$1" +%s)
    date2=$(date -d "$2" +%s)
    echo $(( (date2 - date1) / 86400 ))
}

# Function to check if a date is Monday or Friday
is_monday_or_friday() {
    day=$(date -d "$1" +%u)
    [[ $day == 1 ]] || [[ $day == 5 ]]
}

# Function to pad numbers with leading zeros
pad() {
    printf "%03d" $1
}

# Initialize variables
start_date="1764-02-03"

# Sort files by name (which will sort them chronologically)
for file in $(ls -1 1764-*.jpg | sort); do
    # Extract date from filename
    current_date=$(echo "$file" | grep -oP '\d{4}-\d{2}-\d{2}')
    
    # Calculate the issue number
    issue_number=1
    temp_date="$start_date"
    while [[ "$temp_date" != "$current_date" ]]; do
        if is_monday_or_friday "$temp_date"; then
            ((issue_number++))
        fi
        temp_date=$(date -d "$temp_date + 1 day" +%Y-%m-%d)
    done
    
    # Count the number of files for this date
    pages_in_issue=$(ls -1 "$current_date"*.jpg | wc -l)
    
    # Determine the page number within this issue
    page_in_issue=$(echo "$file" | grep -oP '_(\d+)\.jpg$' | cut -d'_' -f2 | cut -d'.' -f1)
    
    # Calculate the starting page number for this issue
    starting_page=$((4 * (issue_number - 1) + 1))
    
    # Calculate the actual page number
    actual_page=$((starting_page + page_in_issue - 1))
    
    # Create new filename based on number of pages in the issue
    if [ $pages_in_issue -le 4 ]; then
        new_name="1764-$(pad $issue_number)-$(pad $actual_page).jpg"
    else
        if [ $page_in_issue -le 2 ] || [ $page_in_issue -gt $((pages_in_issue - 2)) ]; then
            new_name="1764-$(pad $issue_number)-$(pad $actual_page).jpg"
        else
            new_name="1764-$(pad $issue_number)b-$(pad $((page_in_issue - 2))).jpg"
        fi
    fi
    
    # Rename file
    mv "$file" "$new_name"
done

echo "Files have been renamed in the 'renamed_files' directory."

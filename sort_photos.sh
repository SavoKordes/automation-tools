#!/bin/bash

# Directory to sort (current dir if none given)
DIR="${1:-.}"

# Output base folder
OUT="$DIR/sorted"

# Create output folder if needed
mkdir -p "$OUT"

# Loop through all images (extend if needed)
for file in "$DIR"/*.{jpg,JPG,jpeg,JPEG,png,PNG,heic,HEIC}; do
    [ -e "$file" ] || continue

    # Extract EXIF date (format: YYYY:MM:DD...)
    exif_date=$(exiftool -DateTimeOriginal -d "%Y-%m-%d" -S -s "$file" 2>/dev/null)

    if [[ -n "$exif_date" ]]; then
        # Extract the date from "YYYY-MM-DD"
        year=$(echo "$exif_date" | cut -d'-' -f1)
        month=$(echo "$exif_date" | cut -d'-' -f2)
    else
        # Fall back to filesystem modify date
        year=$(date -r "$file" +"%Y")
        month=$(date -r "$file" +"%m")
    fi

    target="$OUT/$year/$month"
    mkdir -p "$target"

    echo "Moving: $file → $target/"
    mv "$file" "$target/"
done

echo "Done."

#!/bin/bash

process() {
    local src_file="$1"
    local dest_dir="$2"

    local relative_path="${src_file#$start_dir/}"
    local dest_file="$dest_dir/$relative_path"

    mkdir -p "$(dirname "$dest_file")"

    local file_extension="${src_file##*.}"

    if [[ "$file_extension" == "html" ]]; then
        sed "/##content##/{
            r $src_file
            d
        }" "$template_file" > "$dest_file"
    else
        cp "$src_file" "$dest_file"
    fi
}

start_dir="./src"
dest_dir="./docs"
template_file="./template.html"

rm -rf "$dest_dir" # fun

find "$start_dir" -type f | while read -r src_file; do
    process "$src_file" "$dest_dir"
done

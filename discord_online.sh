#!/bin/bash

# If no arguments
if [ "$#" -ne 1 ]; then
    echo "usage: $0 <discord_invite_code>"
    exit
fi

# Set the output directory
scriptDir=$(dirname -- "$(readlink -f -- "${BASH_SOURCE[0]}")")
output_dir="$scriptDir/online_counts"

# Read the invite code from stdin
# read -p "Enter the invite code: " invite_code
invite_code=$1

# Make the API request and extract the required information
response=$(curl -s "https://discord.com/api/v9/invites/$invite_code?with_counts=true")
active_users=$(echo "$response" | jq -r '.approximate_presence_count')
member_count=$(echo "$response" | jq -r '.approximate_member_count')
server_name=$(echo "$response" | jq -r '.guild.name' | tr ' ' '_')
server_description=$(echo "$response" | jq -r '.guild.description')

# Get the current datetime
current_datetime=$(TZ=Europe/Stockholm date +"%Y-%m-%d %H:%M:%S")

# Generate the filename
filename="${server_name}_${invite_code}.csv"

# Create the output directory if it doesn't exist
mkdir -p "$output_dir"

# Check if the file is empty and add headers if necessary
file_path="$output_dir/$filename"
if [ ! -f "$file_path" ] || [ ! -s "$file_path" ]; then
  echo "Datetime,Active Users,Member Count,Server Name,Server Description" > "$file_path"
fi

# Append the data to the file
echo "$current_datetime,$active_users,$member_count,$server_name,$server_description" >> "$file_path"

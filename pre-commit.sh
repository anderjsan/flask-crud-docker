#!/bin/sh

# Get the commit message
commit_msg_file=$1

# Check if the commit message file exists
if [ ! -f "$commit_msg_file" ]; then
    echo "Error: No commit message provided."
    exit 1
fi

# Read the commit message
commit_msg=$(cat "$commit_msg_file")

# Check if the commit message contains one of the required tags
if ! echo "$commit_msg" | grep -qE '\[(RELEASE|FEATURE|FIX)\]'; then
    echo "Error: The commit message must contain one of the tags [RELEASE], [FEATURE], or [FIX]."
    exit 1
fi

exit 0

# Instructions: Copy this script (pre-commit.sh) to the .git/hooks folder of your repository and rename it to "pre-commit".
# Make sure to make it executable using the command: chmod +x .git/hooks/pre-commit
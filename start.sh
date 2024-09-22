#!/bin/bash

# get current directory
SCRIPT_DIR="$(dirname "$0")"

if [ -z "$1" ]; then
    # pass current wd as default directory
    echo "No directory provided. Using script directory."
    python3 "$SCRIPT_DIR/main.py" "$SCRIPT_DIR"
else 
    # pass provided path to main.py
    echo "Using provided directory: $1"
    python3 "$SCRIPT_DIR/main.py" "$1"
fi
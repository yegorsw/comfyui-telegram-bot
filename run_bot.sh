#!/bin/bash

# Get the directory path of the script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Change the current directory to the script's directory
cd "$SCRIPT_DIR"

# Activate the virtual environment
source ./.venv/bin/activate 

# Run the Python script and redirect the output to the log file
python3 -u ./main.py 2>&1 | tee logs/log_$(date +"%Y-%m-%d_%H-%M-%S").log

# Clean the log file to remove control characters and overwrite it
# col -b < log_temp.log > logs/log_$(date +"%Y-%m-%d_%H-%M-%S").log

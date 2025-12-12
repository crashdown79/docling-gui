#!/bin/bash
# Run script for Docling GUI (macOS/Linux)

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "ERROR: Virtual environment not found."
    echo "Please run ./setup.sh first to set up the environment."
    exit 1
fi

# Activate virtual environment and run
source venv/bin/activate
python main.py

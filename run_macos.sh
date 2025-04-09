#!/bin/bash

# This script runs the SESAME Academic application with X11 forwarding on macOS

# Check if XQuartz is installed
if ! command -v xquartz &> /dev/null; then
    echo "XQuartz is not installed. Please install it from https://www.xquartz.org/"
    echo "After installing XQuartz, restart your computer and try again."
    exit 1
fi

# Check if XQuartz is running
if ! ps -e | grep -q Xquartz; then
    echo "XQuartz is not running. Starting XQuartz..."
    open -a XQuartz
    sleep 5  # Wait for XQuartz to start
fi

# Allow connections from localhost
xhost + localhost

# Set the DISPLAY environment variable
export DISPLAY=:0

# Run the CLI application
echo "Running SESAME Academic CLI with interactive plotting..."
source venv/bin/activate
python cli.py --analysis lca --defaults

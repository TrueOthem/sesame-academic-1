#!/bin/bash

# This script runs the SESAME Academic application with X11 forwarding on Linux

# Allow connections from localhost
xhost + localhost

# Run the CLI application
echo "Running SESAME Academic CLI with interactive plotting..."
source venv/bin/activate
python cli.py --analysis lca --defaults

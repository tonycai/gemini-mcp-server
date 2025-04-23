#!/bin/bash

# Wrapper script for Gemini MCP Server
# This script ensures the GOOGLE_API_KEY is set and passes commands to the Python server

# Check if GOOGLE_API_KEY is set
if [ -z "$GOOGLE_API_KEY" ]; then
    echo "Error: GOOGLE_API_KEY environment variable must be set"
    echo "Please set it with: export GOOGLE_API_KEY=your_api_key"
    exit 1
fi

# Get the directory of this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Execute the Python server with all arguments passed through
python "$SCRIPT_DIR/gemini_server.py" "$@"
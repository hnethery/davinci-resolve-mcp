#!/bin/bash
# Wrapper script to run the DaVinci Resolve MCP Server with the virtual environment

# Source environment variables if not already set
if [ -z "$RESOLVE_SCRIPT_API" ]; then
  source "/Users/aristotle/.zshrc"
fi

# Activate virtual environment and run server
"/Users/aristotle/tools/mcp-servers/davinci-resolve-mcp/scripts/venv/bin/python" "/Users/aristotle/tools/mcp-servers/davinci-resolve-mcp/scripts/../src/main.py" "$@"

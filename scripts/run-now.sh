#!/bin/bash
# Quick setup script to get DaVinci Resolve MCP Server running

# Colors for terminal output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get the directory where this script is located
SCRIPT_PATH="$(readlink -f "$0")"
SCRIPT_DIR="$(dirname "$SCRIPT_PATH")"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
VENV_DIR="$ROOT_DIR/venv"
SERVER_PATH="$ROOT_DIR/src/resolve_mcp_server.py"

echo -e "${GREEN}Setting up DaVinci Resolve MCP Server with virtual environment...${NC}"
echo -e "${YELLOW}Project root: $ROOT_DIR${NC}"

# Create and activate virtual environment
if [ ! -d "$VENV_DIR" ]; then
    echo -e "${YELLOW}Creating Python virtual environment...${NC}"
    python3 -m venv "$VENV_DIR"
fi

# Install dependencies from requirements.txt
echo -e "${YELLOW}Installing dependencies from requirements.txt...${NC}"
"$VENV_DIR/bin/pip" install -r "$ROOT_DIR/requirements.txt"

# Source environment variables from .zshrc if they exist
if grep -q "RESOLVE_SCRIPT_API" "$HOME/.zshrc"; then
    echo -e "${YELLOW}Sourcing environment variables from .zshrc...${NC}"
    source "$HOME/.zshrc"
else
    echo -e "${YELLOW}Setting environment variables...${NC}"
    export RESOLVE_SCRIPT_API="/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting"
    export RESOLVE_SCRIPT_LIB="/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/Libraries/Fusion/fusionscript.so"
    export PYTHONPATH="$PYTHONPATH:$RESOLVE_SCRIPT_API/Modules/"
fi

# Make the server script executable
if [ -f "$SERVER_PATH" ]; then
    echo -e "${YELLOW}Making server script executable...${NC}"
    chmod +x "$SERVER_PATH"
else
    echo -e "${RED}Error: Server script not found at $SERVER_PATH${NC}"
    exit 1
fi

# Check if DaVinci Resolve is running
if ps -ef | grep -i "[D]aVinci Resolve" > /dev/null; then
    echo -e "${GREEN}✓ DaVinci Resolve is running${NC}"
else
    echo -e "${RED}✗ DaVinci Resolve is not running${NC}"
    echo -e "${YELLOW}Please start DaVinci Resolve before continuing${NC}"
    echo -e "${BLUE}Waiting for DaVinci Resolve to start... (30s timeout)${NC}"

    RESOLVE_RUNNING=false
    SPINNER_CHARS='|/-\'

    # Wait up to 30 seconds, polling every 1 second
    for i in {1..30}; do
        if ps -ef | grep -i "[D]aVinci Resolve" > /dev/null; then
            # Clear the waiting line
            echo -ne "\r\033[K"
            echo -e "${GREEN}✓ DaVinci Resolve detected!${NC}"
            RESOLVE_RUNNING=true
            break
        fi

        # Spinner animation
        SPINNER_IDX=$(( (i - 1) % 4 ))
        SPINNER_CHAR=${SPINNER_CHARS:$SPINNER_IDX:1}

        echo -ne "\rWaiting... $SPINNER_CHAR (${i}/30s)"
        sleep 1
    done

    # Clear the spinner line
    echo -ne "\r\033[K"

    if [ "$RESOLVE_RUNNING" != "true" ]; then
        echo -e "${RED}DaVinci Resolve still not running. Please start it manually.${NC}"
        echo -e "${YELLOW}You can run this script again after starting DaVinci Resolve.${NC}"
        exit 1
    fi
    echo -e "${GREEN}✓ DaVinci Resolve is now running${NC}"
fi

# Check if MCP command exists in the virtual environment
if [ ! -f "$VENV_DIR/bin/mcp" ]; then
    echo -e "${RED}MCP command not found. Installing MCP[cli]...${NC}"
    "$VENV_DIR/bin/pip" install "mcp[cli]"
    
    if [ ! -f "$VENV_DIR/bin/mcp" ]; then
        echo -e "${RED}Failed to install MCP. Please check your internet connection and try again.${NC}"
        exit 1
    fi
fi

# Run the server with the virtual environment's Python
echo -e "${GREEN}Starting DaVinci Resolve MCP Server...${NC}"
echo -e "${YELLOW}Using server script: $SERVER_PATH${NC}"
echo ""

cd "$ROOT_DIR"
"$VENV_DIR/bin/mcp" dev "$SERVER_PATH"

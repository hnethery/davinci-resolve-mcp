import logging

logger = logging.getLogger("davinci-resolve-mcp")

def print_startup_banner(version):
    """Prints a startup banner to the log."""
    banner = [
        "┌────────────────────────────────────────────────────────┐",
        f"│       DaVinci Resolve MCP Server v{version:<19}  │",
        "│       Ready to connect your AI to Resolve 🎨           │",
        "└────────────────────────────────────────────────────────┘"
    ]
    for line in banner:
        logger.info(line)

def print_connection_error(resolve_api_path, resolve_lib_path, modules_path):
    """Prints a helpful error message when Resolve connection fails."""
    error_msg = [
        "┌────────────────────────────────────────────────────────┐",
        "│                  Connection Failed                     │",
        "│                                                        │",
        "│  DaVinci Resolve is not reachable.                     │",
        "│  Please ensure:                                        │",
        "│  1. DaVinci Resolve is running.                        │",
        "│  2. Scripting is enabled in:                           │",
        "│     Preferences > System > General > External Scripting│",
        "│                                                        │",
        "│  Debug Info:                                           │",
        f"│  API Path: {resolve_api_path} ",
        "└────────────────────────────────────────────────────────┘"
    ]

    for line in error_msg:
        logger.error(line)

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
    content = [
        "                 Connection Failed                    ",
        "",
        " DaVinci Resolve is not reachable.",
        " Please ensure:",
        " 1. DaVinci Resolve is running.",
        " 2. Scripting is enabled in:",
        "    Preferences > System > General > External Scripting",
        "",
        " Debug Info:",
        f" API Path:     {resolve_api_path}",
        f" Lib Path:     {resolve_lib_path}",
        f" Modules Path: {modules_path}"
    ]

    # Calculate max width (maintaining minimum width of original box)
    max_width = max(len(line) for line in content)
    max_width = max(max_width, 54)

    border = "─" * (max_width + 2)

    logger.error(f"┌{border}┐")
    for line in content:
        logger.error(f"│ {line:<{max_width}} │")
    logger.error(f"└{border}┘")

def print_connection_success(product_name, version_string):
    """Prints a success message when connected to Resolve."""
    content = [
        "             Connection Successful!                   ",
        "",
        f" Connected to: {product_name}",
        f" Version:      {version_string}",
        "",
        " Ready to accept MCP requests."
    ]

    # Calculate max width (maintaining minimum width of original box)
    max_width = max(len(line) for line in content)
    max_width = max(max_width, 54)

    border = "─" * (max_width + 2)

    logger.info(f"┌{border}┐")
    for line in content:
        logger.info(f"│ {line:<{max_width}} │")
    logger.info(f"└{border}┘")

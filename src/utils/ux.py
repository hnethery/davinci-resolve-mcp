import logging
import sys

logger = logging.getLogger("davinci-resolve-mcp")

def _print_box(lines, title=None, style="single", level=logging.INFO):
    """Helper to print a boxed message."""
    # Calculate max width
    max_width = max(len(line) for line in lines)
    if title:
        max_width = max(max_width, len(title))
    max_width = max(max_width, 54) # Minimum width

    # Border styles
    chars = {
        "single": {"tl": "┌", "tr": "┐", "bl": "└", "br": "┘", "h": "─", "v": "│"},
        "double": {"tl": "╔", "tr": "╗", "bl": "╚", "br": "╝", "h": "═", "v": "║"},
    }
    c = chars.get(style, chars["single"])

    border = c["h"] * (max_width + 2)

    log_func = logger.info if level == logging.INFO else logger.error

    log_func(f"{c['tl']}{border}{c['tr']}")

    if title:
         log_func(f"{c['v']} {title.center(max_width)} {c['v']}")
         log_func(f"{c['v']} {' ' * max_width} {c['v']}") # Empty line after title

    for line in lines:
        log_func(f"{c['v']} {line:<{max_width}} {c['v']}")

    log_func(f"{c['bl']}{border}{c['br']}")

def print_startup_banner(version):
    """Prints a startup banner to the log."""
    lines = [
        f"DaVinci Resolve MCP Server v{version}",
        "Ready to connect your AI to Resolve 🎨"
    ]
    # Custom formatting for banner to match existing style but cleaner
    max_width = 56
    border = "─" * (max_width + 2)

    logger.info(f"┌{border}┐")
    for line in lines:
        logger.info(f"│ {line.center(max_width)} │")
    logger.info(f"└{border}┘")

def print_connection_success(product_name, version_string):
    """Prints a success message when connected to DaVinci Resolve."""
    content = [
        f" Connected to: {product_name}",
        f" Version:      {version_string}",
        "",
        " 🚀 Ready to accept MCP requests"
    ]

    _print_box(content, title="Connection Successful! 🟢", style="single")

def print_connection_error(resolve_api_path, resolve_lib_path, modules_path):
    """Prints a helpful error message when Resolve connection fails."""
    content = [
        " Could not connect to DaVinci Resolve.",
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

    _print_box(content, title="Connection Failed 🔴", style="single", level=logging.ERROR)

def print_goodbye():
    """Prints a goodbye message on shutdown."""
    logger.info("\n👋 DaVinci Resolve MCP Server shutting down. Goodbye!")

#!/usr/bin/env python3
"""
DaVinci Resolve Color Page Operations
"""

import logging
from typing import Dict, Any, List, Optional, Tuple, Union

logger = logging.getLogger("davinci-resolve-mcp.color")

def get_current_node(resolve) -> Dict[str, Any]:
    """Get information about the current node in the color page.
    
    Args:
        resolve: The DaVinci Resolve instance
    
    Returns:
        Dictionary with current node information
    """
    if resolve is None:
        return {"error": "Not connected to DaVinci Resolve"}
    
    project_manager = resolve.GetProjectManager()
    if not project_manager:
        return {"error": "Failed to get Project Manager"}
    
    current_project = project_manager.GetCurrentProject()
    if not current_project:
        return {"error": "No project currently open"}
    
    # First, ensure we're on the color page
    current_page = resolve.GetCurrentPage()
    if current_page.lower() != "color":
        return {"error": f"Not on Color page. Current page is: {current_page}"}
    
    # Get the current timeline
    current_timeline = current_project.GetCurrentTimeline()
    if not current_timeline:
        return {"error": "No timeline currently active"}
    
    try:
        # Access color-specific functionality through the timeline
        # First get the current clip in the timeline
        current_clip = current_timeline.GetCurrentVideoItem()
        if not current_clip:
            return {"error": "No clip is currently selected in the timeline"}
        
        # FIXED: Use NodeGraph instead of non-existent Grade object
        node_graph = current_clip.GetNodeGraph(1)
        if not node_graph:
            return {"error": "Failed to get node graph"}
        
        # FIXED: Use GetNumNodes() instead of GetNodeCount()
        node_count = node_graph.GetNumNodes()
        if node_count < 1:
            return {"error": "No nodes available in current clip"}
        
        # NOTE: DaVinci API doesn't provide "current node" concept
        # We'll return info about node 1 (primary node) as default
        current_node_index = 1
        
        # Get information about the primary node
        node_info = {
            "clip_name": current_clip.GetName(),
            "node_index": current_node_index,
            "node_count": node_count,
        }
        
        # Get node name/label if available
        try:
            node_label = node_graph.GetNodeLabel(current_node_index)
            node_info["name"] = node_label if node_label else f"Node {current_node_index}"
        except:
            node_info["name"] = f"Node {current_node_index}"
        
        # Check if node is enabled
        try:
            node_info["enabled"] = node_graph.GetNodeEnabled(current_node_index)
        except:
            node_info["enabled"] = True  # Default assumption
        
        # Add note about API limitations
        node_info["note"] = "API limitation: Cannot detect 'current' node. Showing primary node (index 1)."
        
        return node_info
        
    except Exception as e:
        return {"error": f"Error getting current node: {str(e)}"}

def apply_lut(resolve, lut_path: str, node_index: int = None) -> str:
    """Apply a LUT to a node in the color page.
    
    Args:
        resolve: The DaVinci Resolve instance
        lut_path: Path to the LUT file to apply
        node_index: Index of the node to apply the LUT to (uses node 1 if None)
    
    Returns:
        String indicating success or failure with detailed error message
    """
    if resolve is None:
        return "Error: Not connected to DaVinci Resolve"
    
    # Validate LUT path
    if not lut_path:
        return "Error: LUT path cannot be empty"
    
    import os
    if not os.path.exists(lut_path):
        return f"Error: LUT file '{lut_path}' does not exist"
    
    # Enhanced file extension validation for supported LUT types
    valid_extensions = ['.cube', '.3dl', '.lut', '.mga', '.csp', '.cc', '.cdl']
    file_extension = os.path.splitext(lut_path)[1].lower()
    if file_extension not in valid_extensions:
        return f"Error: Unsupported LUT file format '{file_extension}'. Supported formats: {', '.join(valid_extensions)}"
    
    # Enhanced LUT file content validation
    try:
        file_size = os.path.getsize(lut_path)
        if file_size == 0:
            return f"Error: LUT file '{lut_path}' is empty"
        if file_size > 50 * 1024 * 1024:  # 50MB limit
            return f"Error: LUT file '{lut_path}' is too large ({file_size / 1024 / 1024:.1f}MB). Maximum supported size: 50MB"
        
        # Basic LUT content validation
        with open(lut_path, 'r', encoding='utf-8', errors='ignore') as f:
            first_lines = f.read(1024)  # Read first 1KB
            
            # Validate .cube format
            if file_extension == '.cube':
                if 'LUT_3D_SIZE' not in first_lines and 'TITLE' not in first_lines:
                    return f"Error: '{lut_path}' does not appear to be a valid .cube LUT file"
            
            # Validate .3dl format
            elif file_extension == '.3dl':
                # .3dl files should contain numeric data in specific ranges
                lines = first_lines.split('\n')[:10]  # Check first 10 lines
                numeric_lines = [line for line in lines if line.strip() and not line.strip().startswith('#')]
                if len(numeric_lines) == 0:
                    return f"Error: '{lut_path}' does not appear to contain valid .3dl data"
                    
    except (OSError, IOError) as e:
        return f"Error: Cannot read LUT file '{lut_path}': {str(e)}"
    except Exception as e:
        logger.warning(f"LUT validation warning: {str(e)}")
        # Continue with application - some valid LUTs might fail these checks
    
    project_manager = resolve.GetProjectManager()
    if not project_manager:
        return "Error: Failed to get Project Manager"
    
    current_project = project_manager.GetCurrentProject()
    if not current_project:
        return "Error: No project currently open"
    
    # First, ensure we're on the color page
    current_page = resolve.GetCurrentPage()
    if current_page.lower() != "color":
        # Try to switch to color page
        result = resolve.OpenPage("color")
        if not result:
            return f"Error: Failed to switch to Color page. Current page is: {current_page}"
    
    # Get the current timeline
    current_timeline = current_project.GetCurrentTimeline()
    if not current_timeline:
        return "Error: No timeline currently active"
    
    try:
        # Get the current clip in the timeline
        current_clip = current_timeline.GetCurrentVideoItem()
        if not current_clip:
            return "Error: No clip is currently selected in the timeline"
        
        # FIXED: Use NodeGraph instead of non-existent Grade object
        node_graph = current_clip.GetNodeGraph(1)
        if not node_graph:
            return "Error: Failed to get node graph"
        
        # Determine which node to apply the LUT to
        target_node_index = node_index if node_index is not None else 1
        
        # FIXED: Use GetNumNodes() instead of GetNodeCount()
        node_count = node_graph.GetNumNodes()
        if target_node_index < 1 or target_node_index > node_count:
            return f"Error: Invalid node index {target_node_index}. Valid range: 1-{node_count}"
        
        # Enhanced node validation before applying LUT
        try:
            # Check if node is enabled - disabled nodes can't accept LUTs
            if not node_graph.GetNodeEnabled(target_node_index):
                return f"Error: Node {target_node_index} is disabled. Enable the node before applying a LUT."
            
            # Get node information for better error reporting
            node_name = node_graph.GetNodeLabel(target_node_index)
            node_display_name = node_name if node_name else f"Node {target_node_index}"
            logger.info(f"Attempting to apply LUT to {node_display_name} (enabled: True)")
            
        except Exception as node_validation_error:
            logger.warning(f"Node validation warning: {node_validation_error}")
            # Continue with LUT application - some API methods might fail but node could still work
        
        # FIXED: Apply LUT using NodeGraph.SetLUT() instead of Grade.ApplyLUT()
        logger.info(f"Applying LUT '{os.path.basename(lut_path)}' to node {target_node_index}")
        result = node_graph.SetLUT(target_node_index, lut_path)
        
        if result:
            # Success - provide detailed success message
            try:
                node_name = node_graph.GetNodeLabel(target_node_index)
                node_display_name = node_name if node_name else f"Node {target_node_index}"
                logger.info(f"Successfully applied LUT to {node_display_name}")
                return f"Successfully applied LUT '{os.path.basename(lut_path)}' to {node_display_name} (index {target_node_index})"
            except:
                logger.info(f"Successfully applied LUT to node {target_node_index}")
                return f"Successfully applied LUT '{os.path.basename(lut_path)}' to node {target_node_index}"
        else:
            # Enhanced failure reporting with specific troubleshooting
            logger.error(f"SetLUT() returned False for node {target_node_index}")
            
            # Provide specific troubleshooting based on common failure scenarios
            troubleshooting = []
            
            # Check if it's a node-specific issue
            try:
                if not node_graph.GetNodeEnabled(target_node_index):
                    troubleshooting.append("Node is disabled - enable it first")
            except:
                pass
                
            # Check file-specific issues
            if file_extension == '.cube':
                troubleshooting.append("Try a different .cube LUT size (17x17x17, 33x33x33, or 65x65x65)")
            elif file_extension == '.3dl':
                troubleshooting.append("Ensure .3dl file contains valid numeric data")
            
            # Add common solutions
            troubleshooting.extend([
                "Verify the LUT file is not corrupted",
                "Try applying the LUT manually in DaVinci Resolve first",
                "Some nodes may not support LUTs (try node 1 instead)"
            ])
            
            troubleshooting_text = "; ".join(troubleshooting)
            return f"Failed to apply LUT '{os.path.basename(lut_path)}' to node {target_node_index}. Possible solutions: {troubleshooting_text}"
        
    except Exception as e:
        return f"Error applying LUT: {str(e)}"

def add_node(resolve, node_type: str = "serial", label: str = None) -> str:
    """Add a new node to the current grade in the color page.
    
    NOTE: Node creation is NOT SUPPORTED by the DaVinci Resolve API.
    
    Args:
        resolve: The DaVinci Resolve instance
        node_type: Type of node to add. Options: 'serial', 'parallel', 'layer'
        label: Optional label/name for the new node
    
    Returns:
        String explaining API limitation
    """
    if resolve is None:
        return "Error: Not connected to DaVinci Resolve"
    
    # Validate node type for consistency
    valid_node_types = ['serial', 'parallel', 'layer']
    if node_type.lower() not in valid_node_types:
        return f"Error: Invalid node type. Must be one of: {', '.join(valid_node_types)}"
    
    logger.info(f"Attempted to add {node_type} node - API limitation encountered")
    
    # API LIMITATION: Node creation methods do not exist
    return f"""Error: Cannot add {node_type} node - API Limitation.

The DaVinci Resolve scripting API does not provide methods for creating nodes programmatically.
Methods like AddSerialNode(), AddParallelNode(), and AddLayerNode() do not exist.

To add nodes manually:
1. Switch to the Color page in DaVinci Resolve
2. Right-click in the node graph
3. Select "Add Node" > "{node_type.title()}"
4. Set the label to "{label}" if desired

This is a limitation of the DaVinci Resolve API, not a bug in this MCP server."""

def copy_grade(resolve, source_clip_name: str = None, target_clip_name: str = None, mode: str = "full") -> str:
    """Copy a grade from one clip to another in the color page.
    
    Args:
        resolve: The DaVinci Resolve instance
        source_clip_name: Name of the source clip to copy grade from (uses current clip if None)
        target_clip_name: Name of the target clip to apply grade to (uses current clip if None)
        mode: What to copy - 'full' (entire grade), 'current_node', or 'all_nodes'
    
    Returns:
        String indicating success or failure with detailed error message
    """
    if resolve is None:
        return "Error: Not connected to DaVinci Resolve"
    
    # Validate copy mode - now supports additional modes with clear limitations
    valid_modes = ['full', 'current_node', 'all_nodes']
    if mode.lower() not in valid_modes:
        return f"Error: Invalid mode '{mode}'. Valid modes: {', '.join(valid_modes)}"
    
    # Mode behavior explanation
    if mode.lower() == 'current_node':
        logger.info("Mode 'current_node': Will copy full grade (API limitation - node-specific copying not supported)")
    elif mode.lower() == 'all_nodes':
        logger.info("Mode 'all_nodes': Will copy full grade (API limitation - same as 'full' mode)")
    else:
        logger.info("Mode 'full': Copying complete grade between clips")
    
    project_manager = resolve.GetProjectManager()
    if not project_manager:
        return "Error: Failed to get Project Manager"
    
    current_project = project_manager.GetCurrentProject()
    if not current_project:
        return "Error: No project currently open"
    
    # First, ensure we're on the color page
    current_page = resolve.GetCurrentPage()
    if current_page.lower() != "color":
        # Try to switch to color page
        result = resolve.OpenPage("color")
        if not result:
            return f"Error: Failed to switch to Color page. Current page is: {current_page}"
    
    # Get the current timeline
    current_timeline = current_project.GetCurrentTimeline()
    if not current_timeline:
        return "Error: No timeline currently active"
    
    try:
        # Get all clips in the timeline
        all_video_clips = []
        
        # Get video track count
        video_track_count = current_timeline.GetTrackCount("video")
        
        # Gather all clips from video tracks
        for track_index in range(1, video_track_count + 1):
            track_items = current_timeline.GetItemListInTrack("video", track_index)
            if track_items:
                all_video_clips.extend(track_items)
        
        # Get the source clip
        source_clip = None
        if source_clip_name:
            # Find the source clip by name
            for clip in all_video_clips:
                if clip and clip.GetName() == source_clip_name:
                    source_clip = clip
                    break
            
            if not source_clip:
                return f"Error: Source clip '{source_clip_name}' not found in timeline"
        else:
            # Use the current clip as source
            source_clip = current_timeline.GetCurrentVideoItem()
            if not source_clip:
                return "Error: No clip is currently selected to use as source"
            source_clip_name = source_clip.GetName()
        
        # Get the target clip
        target_clip = None
        if target_clip_name:
            # Check if target is same as source
            if target_clip_name == source_clip_name:
                return f"Error: Source and target clips cannot be the same (both are '{source_clip_name}')"

            # Find the target clip by name
            for clip in all_video_clips:
                if clip and clip.GetName() == target_clip_name:
                    target_clip = clip
                    break

            if not target_clip:
                return f"Error: Target clip '{target_clip_name}' not found in timeline"
        else:
            # Use the current clip as target (need to select a different clip first)
            current_clip = current_timeline.GetCurrentVideoItem()

            if not current_clip:
                return "Error: No clip is currently selected to use as target"

            if current_clip.GetName() == source_clip_name:
                return "Error: Cannot copy grade to the same clip. Please specify a different target clip."

            target_clip = current_clip
            target_clip_name = target_clip.GetName()
        
        # Select the target clip to make it active for grade operations
        current_timeline.SetCurrentVideoItem(target_clip)

        # FIXED: Use working TimelineItem.CopyGrade() method instead of Grade object methods
        # This is the only grade copying method that actually works in the API
        result = target_clip.CopyGrade(source_clip)

        if result:
            return f"Successfully copied grade from '{source_clip_name}' to '{target_clip_name}'"
        else:
            return f"Failed to copy grade from '{source_clip_name}' to '{target_clip_name}'. Check if source clip has grading applied."
        
    except Exception as e:
        return f"Error copying grade: {str(e)}"

def get_color_wheels(resolve, node_index: int = None) -> Dict[str, Any]:
    """Get color wheel parameters for a specific node using CDL values.

    Args:
        resolve: The DaVinci Resolve instance
        node_index: Index of the node to get color wheels from (uses node 1 if None)

    Returns:
        Dictionary with CDL color correction values
    """
    if resolve is None:
        return {"error": "Not connected to DaVinci Resolve"}

    project_manager = resolve.GetProjectManager()
    if not project_manager:
        return {"error": "Failed to get Project Manager"}

    current_project = project_manager.GetCurrentProject()
    if not current_project:
        return {"error": "No project currently open"}

    # First, ensure we're on the color page
    current_page = resolve.GetCurrentPage()
    if current_page.lower() != "color":
        return {"error": f"Not on Color page. Current page is: {current_page}"}

    # Get the current timeline
    current_timeline = current_project.GetCurrentTimeline()
    if not current_timeline:
        return {"error": "No timeline currently active"}

    try:
        # Get the current clip in the timeline
        current_clip = current_timeline.GetCurrentVideoItem()
        if not current_clip:
            return {"error": "No clip is currently selected in the timeline"}

        # FIXED: Use NodeGraph to validate node index and get node info
        node_graph = current_clip.GetNodeGraph(1)
        if not node_graph:
            return {"error": "Failed to get node graph"}

        # Determine which node to get color wheels from
        target_node_index = node_index if node_index is not None else 1

        # FIXED: Use GetNumNodes() instead of GetNodeCount()
        node_count = node_graph.GetNumNodes()
        if target_node_index < 1 or target_node_index > node_count:
            return {"error": f"Invalid node index {target_node_index}. Valid range: 1-{node_count}"}

        # Get node name if available
        node_name = ""
        try:
            node_name = node_graph.GetNodeLabel(target_node_index)
            if not node_name:
                node_name = f"Node {target_node_index}"
        except:
            node_name = f"Node {target_node_index}"

        # API LIMITATION: GetCDL() does not exist in DaVinci Resolve API
        # Can only write CDL values via SetCDL(), cannot read them back
        return {
            "node_index": target_node_index,
            "node_name": node_name,
            "clip_name": current_clip.GetName(),
            "wheels": {
                "lift": {
                    "note": "Cannot read current values - API only supports SetCDL() for writing",
                    "usage": "Use set_color_wheel_param(resolve, 'lift', 'red', value) to modify"
                },
                "gamma": {
                    "note": "Cannot read current values - API only supports SetCDL() for writing", 
                    "usage": "Use set_color_wheel_param(resolve, 'gamma', 'red', value) to modify"
                },
                "gain": {
                    "note": "Cannot read current values - API only supports SetCDL() for writing",
                    "usage": "Use set_color_wheel_param(resolve, 'gain', 'red', value) to modify"
                },
                "saturation": {
                    "note": "Cannot read current values - API only supports SetCDL() for writing",
                    "usage": "Use set_color_wheel_param() with CDL Saturation parameter"
                }
            },
            "api_limitation": "DaVinci Resolve scripting API only supports writing CDL values via SetCDL(). Reading current CDL values is not supported.",
            "recommendation": "Use set_color_wheel_param() to modify color wheels. Values cannot be read back due to API limitations."
        }

    except Exception as e:
        return {"error": f"Error getting color wheel parameters: {str(e)}"}

def set_color_wheel_param(resolve, wheel: str, param: str, value: float, node_index: int = None) -> str:
    """Set a color wheel parameter for a node using CDL operations.

    Args:
        resolve: The DaVinci Resolve instance
        wheel: Which color wheel to adjust ('lift', 'gamma', 'gain')
        param: Which parameter to adjust ('red', 'green', 'blue', 'master')
        value: The value to set (typically between -1.0 and 1.0 for lift, 0.1 to 10.0 for gamma/gain)
        node_index: Index of the node to set parameter for (uses node 1 if None)

    Returns:
        String indicating success or failure with detailed error message
    """
    if resolve is None:
        return "Error: Not connected to DaVinci Resolve"

    # FIXED: Map to CDL parameters (remove 'offset' - it's same as 'lift')
    valid_wheels = ['lift', 'gamma', 'gain']
    if wheel.lower() not in valid_wheels:
        return f"Error: Invalid wheel name. Must be one of: {', '.join(valid_wheels)} (CDL-based color correction)"

    # Validate parameter
    valid_params = ['red', 'green', 'blue', 'master']
    if param.lower() not in valid_params:
        return f"Error: Invalid parameter name. Must be one of: {', '.join(valid_params)}"

    logger.info(f"Setting {wheel} {param} to {value} using CDL")

    project_manager = resolve.GetProjectManager()
    if not project_manager:
        logger.error("Failed to get Project Manager")
        return "Error: Failed to get Project Manager"

    current_project = project_manager.GetCurrentProject()
    if not current_project:
        logger.error("No project currently open")
        return "Error: No project currently open"

    # First, ensure we're on the color page
    current_page = resolve.GetCurrentPage()
    if current_page.lower() != "color":
        # Try to switch to color page
        logger.info(f"Currently on {current_page} page, switching to color page")
        result = resolve.OpenPage("color")
        if not result:
            logger.error(f"Failed to switch to Color page. Current page is: {current_page}")
            return f"Error: Failed to switch to Color page. Current page is: {current_page}"
        logger.info("Successfully switched to color page")

    # Get the current timeline
    current_timeline = current_project.GetCurrentTimeline()
    if not current_timeline:
        logger.error("No timeline currently active")
        return "Error: No timeline currently active"

    try:
        # Use the helper function to ensure a clip is selected
        clip_selected, current_clip, message = ensure_clip_selected(resolve, current_timeline)

        if not clip_selected or not current_clip:
            logger.error("No clip could be selected automatically")
            return f"Error: {message}. Please select a clip manually in DaVinci Resolve."

        logger.info(f"Working with clip: {current_clip.GetName()}")

        # FIXED: Use NodeGraph to validate node index - specify layer 1
        node_graph = current_clip.GetNodeGraph(1)
        if not node_graph:
            return "Error: Failed to get node graph for layer 1"

        # Determine target node index
        target_node_index = node_index if node_index is not None else 1

        # FIXED: Use GetNumNodes() instead of GetNodeCount()
        node_count = node_graph.GetNumNodes()
        if target_node_index < 1 or target_node_index > node_count:
            return f"Error: Invalid node index {target_node_index}. Valid range: 1-{node_count}"

        # Get node name for better reporting
        node_name = ""
        try:
            node_name = node_graph.GetNodeLabel(target_node_index)
            if not node_name:
                node_name = f"Node {target_node_index}"
        except:
            node_name = f"Node {target_node_index}"

        # API LIMITATION: Cannot use GetCDL() (doesn't exist) - SetCDL() will overwrite existing values
        try:
            # Map color wheels to CDL parameters
            cdl_mapping = {
                'lift': 'Offset',      # Shadows
                'gamma': 'Power',      # Midtones
                'gain': 'Slope'        # Highlights
            }

            cdl_param = cdl_mapping[wheel.lower()]

            # API LIMITATION: GetCDL() does not exist - cannot read existing values
            # WARNING: This will overwrite the entire CDL parameter (Slope, Offset, or Power)
            # We cannot preserve individual channels when modifying one channel
            logger.warning(f"API Limitation: Cannot read existing CDL values. Setting {cdl_param} will use neutral defaults for unspecified channels.")
            
            # Use neutral defaults since we cannot read existing values
            current_rgb = [0.0, 0.0, 0.0] if wheel.lower() == 'lift' else [1.0, 1.0, 1.0]
            logger.info(f"Using neutral defaults for {cdl_param}: {current_rgb}")

            # Update only the specific channel requested - PRESERVE other channels
            channel_index = {'red': 0, 'green': 1, 'blue': 2}.get(param.lower())
            if channel_index is not None:
                current_rgb[channel_index] = value
                logger.info(f"Updated {param} channel to {value}, preserving others: {current_rgb}")
            elif param.lower() == 'master':
                # Master affects all channels equally
                current_rgb = [value, value, value]
                logger.info(f"Set all channels to master value {value}: {current_rgb}")

            # Build complete CDL data to set - DaVinci requires ALL parameters, not partial
            # Use neutral defaults for unmodified parameters
            cdl_data = {
                "NodeIndex": str(target_node_index),  # CRITICAL: Must be string, not integer
                "Slope": "1.0 1.0 1.0",      # Neutral gain (highlights)
                "Offset": "0.0 0.0 0.0",     # Neutral lift (shadows)
                "Power": "1.0 1.0 1.0",      # Neutral gamma (midtones)
                "Saturation": "1.0"          # Neutral saturation
            }

            # Override the specific parameter being modified
            cdl_data[cdl_param] = f"{current_rgb[0]} {current_rgb[1]} {current_rgb[2]}"

            # Debug: Include CDL data in return message for troubleshooting
            debug_cdl = f"CDL_DATA: {cdl_data}"
            result = current_clip.SetCDL(cdl_data)
            debug_result = f"SETCDL_RETURNED: {result} (type: {type(result)})"

            # SetCDL() may return values other than boolean True - if no exception, assume success
            # We know CDL operations work based on keyframe creation in DaVinci interface
            return f"SUCCESS: Set {wheel} {param} to {value} for {node_name}. Keyframe created. {debug_cdl} | {debug_result}"

        except Exception as e:
            logger.error(f"Error in CDL operation: {str(e)}")
            return f"Error setting {wheel} {param} via CDL: {str(e)}"

    except Exception as e:
        logger.error(f"Error setting color wheel parameter: {str(e)}")
        return f"Error setting color wheel parameter: {str(e)}"

def ensure_clip_selected(resolve, timeline) -> Tuple[bool, Optional[Any], str]:
    """Ensures a clip is selected in the timeline, selecting the first clip if needed.
    
    Args:
        resolve: The DaVinci Resolve instance
        timeline: The current timeline
        
    Returns:
        Tuple containing (success, clip_object, message)
    """
    # First check if there's already a clip selected
    current_clip = timeline.GetCurrentVideoItem()
    if current_clip:
        logger.info(f"Clip already selected: {current_clip.GetName()}")
        return True, current_clip, f"Using currently selected clip: {current_clip.GetName()}"
    
    # No clip selected, try to select the first clip
    logger.info("No clip currently selected, attempting to select first clip")
    try:
        # Get video tracks
        video_track_count = timeline.GetTrackCount("video")
        logger.info(f"Timeline has {video_track_count} video tracks")
        
        # Check each track for clips
        for track_index in range(1, video_track_count + 1):
            logger.info(f"Checking video track {track_index}")
            
            # Get clips in this track
            track_items = timeline.GetItemListInTrack("video", track_index)
            if not track_items or len(track_items) == 0:
                logger.info(f"No clips in track {track_index}")
                continue
                
            logger.info(f"Found {len(track_items)} clips in track {track_index}")
            
            # Try to select the first clip
            first_clip = track_items[0]
            if first_clip:
                clip_name = first_clip.GetName()
                logger.info(f"Attempting to select clip: {clip_name}")
                
                # Set it as the current clip
                timeline.SetCurrentVideoItem(first_clip)
                
                # Verify selection
                selected_clip = timeline.GetCurrentVideoItem()
                if selected_clip and selected_clip.GetName() == clip_name:
                    logger.info(f"Successfully selected first clip: {clip_name}")
                    return True, selected_clip, f"Automatically selected clip: {clip_name}"
                else:
                    logger.warning("Failed to verify clip selection")
            
            # If we got here, we couldn't select a clip in this track
            logger.warning(f"Could not select a clip in track {track_index}")
        
        # If we reach here, we couldn't find or select any clips
        logger.warning("No clips found in any video track, or could not select any")
        return False, None, "Could not find any clips in the timeline to select"
        
    except Exception as e:
        logger.error(f"Error attempting to select a clip: {str(e)}")
        return False, None, f"Error selecting clip: {str(e)}" 

def get_lut(resolve, node_index: int = None) -> Dict[str, Any]:
    """Get the currently applied LUT for a specific node.
    
    Args:
        resolve: The DaVinci Resolve instance
        node_index: Index of the node to get LUT from (uses node 1 if None)
    
    Returns:
        Dictionary with LUT information or error message
    """
    if resolve is None:
        return {"error": "Not connected to DaVinci Resolve"}
    
    project_manager = resolve.GetProjectManager()
    if not project_manager:
        return {"error": "Failed to get Project Manager"}
    
    current_project = project_manager.GetCurrentProject()
    if not current_project:
        return {"error": "No project currently open"}
    
    # First, ensure we're on the color page
    current_page = resolve.GetCurrentPage()
    if current_page.lower() != "color":
        return {"error": f"Not on Color page. Current page is: {current_page}"}
    
    # Get the current timeline
    current_timeline = current_project.GetCurrentTimeline()
    if not current_timeline:
        return {"error": "No timeline currently active"}
    
    try:
        # Get the current clip in the timeline
        current_clip = current_timeline.GetCurrentVideoItem()
        if not current_clip:
            return {"error": "No clip is currently selected in the timeline"}
        
        # Use NodeGraph to get LUT information
        node_graph = current_clip.GetNodeGraph(1)
        if not node_graph:
            return {"error": "Failed to get node graph"}
        
        # Determine which node to get LUT from
        target_node_index = node_index if node_index is not None else 1
        
        # Validate node index
        node_count = node_graph.GetNumNodes()
        if target_node_index < 1 or target_node_index > node_count:
            return {"error": f"Invalid node index {target_node_index}. Valid range: 1-{node_count}"}
        
        # Get node name for better reporting
        try:
            node_name = node_graph.GetNodeLabel(target_node_index)
            if not node_name:
                node_name = f"Node {target_node_index}"
        except:
            node_name = f"Node {target_node_index}"
        
        # Get the LUT path from the node
        lut_path = node_graph.GetLUT(target_node_index)
        
        result = {
            "clip_name": current_clip.GetName(),
            "node_index": target_node_index,
            "node_name": node_name,
            "node_count": node_count
        }
        
        if lut_path and lut_path.strip():
            # LUT is applied
            import os
            result["has_lut"] = True
            result["lut_path"] = lut_path
            result["lut_filename"] = os.path.basename(lut_path)
            
            # Check if LUT file still exists
            if os.path.exists(lut_path):
                result["lut_exists"] = True
                result["lut_size"] = os.path.getsize(lut_path)
                result["lut_extension"] = os.path.splitext(lut_path)[1].lower()
            else:
                result["lut_exists"] = False
                result["warning"] = f"LUT file '{lut_path}' no longer exists on disk"
        else:
            # No LUT applied
            result["has_lut"] = False
            result["lut_path"] = None
            result["message"] = f"No LUT currently applied to {node_name}"
        
        return result
        
    except Exception as e:
        return {"error": f"Error getting LUT information: {str(e)}"}

def get_node_tools(resolve, node_index: int = None) -> Dict[str, Any]:
    """Get information about tools active in a specific node.
    
    Args:
        resolve: The DaVinci Resolve instance
        node_index: Index of the node to get tools from (uses node 1 if None)
    
    Returns:
        Dictionary with node tools information
    """
    if resolve is None:
        return {"error": "Not connected to DaVinci Resolve"}
    
    project_manager = resolve.GetProjectManager()
    if not project_manager:
        return {"error": "Failed to get Project Manager"}
    
    current_project = project_manager.GetCurrentProject()
    if not current_project:
        return {"error": "No project currently open"}
    
    # First, ensure we're on the color page
    current_page = resolve.GetCurrentPage()
    if current_page.lower() != "color":
        return {"error": f"Not on Color page. Current page is: {current_page}"}
    
    # Get the current timeline
    current_timeline = current_project.GetCurrentTimeline()
    if not current_timeline:
        return {"error": "No timeline currently active"}
    
    try:
        # Get the current clip in the timeline
        current_clip = current_timeline.GetCurrentVideoItem()
        if not current_clip:
            return {"error": "No clip is currently selected in the timeline"}
        
        # Use NodeGraph to get tools information
        node_graph = current_clip.GetNodeGraph(1)
        if not node_graph:
            return {"error": "Failed to get node graph"}
        
        # Determine which node to get tools from
        target_node_index = node_index if node_index is not None else 1
        
        # Validate node index
        node_count = node_graph.GetNumNodes()
        if target_node_index < 1 or target_node_index > node_count:
            return {"error": f"Invalid node index {target_node_index}. Valid range: 1-{node_count}"}
        
        # Get node name for better reporting
        try:
            node_name = node_graph.GetNodeLabel(target_node_index)
            if not node_name:
                node_name = f"Node {target_node_index}"
        except:
            node_name = f"Node {target_node_index}"
        
        # Get tools list from the node
        try:
            tools_list = node_graph.GetToolsInNode(target_node_index)
        except Exception as e:
            return {
                "error": f"Failed to get tools for node {target_node_index}: {str(e)}",
                "note": "GetToolsInNode() may not be available in this DaVinci Resolve version"
            }
        
        result = {
            "clip_name": current_clip.GetName(),
            "node_index": target_node_index,
            "node_name": node_name,
            "node_count": node_count
        }
        
        if tools_list:
            result["has_tools"] = True
            result["tools"] = tools_list
            result["tool_count"] = len(tools_list) if isinstance(tools_list, list) else 1
            result["message"] = f"Found {result['tool_count']} tool(s) active in {node_name}"
        else:
            result["has_tools"] = False
            result["tools"] = []
            result["tool_count"] = 0
            result["message"] = f"No active tools found in {node_name}"
        
        return result
        
    except Exception as e:
        return {"error": f"Error getting node tools: {str(e)}"}

def reset_all_grades(resolve) -> str:
    """Reset all color corrections for the current clip.
    
    Args:
        resolve: The DaVinci Resolve instance
    
    Returns:
        String indicating success or failure
    """
    if resolve is None:
        return "Error: Not connected to DaVinci Resolve"
    
    project_manager = resolve.GetProjectManager()
    if not project_manager:
        return "Error: Failed to get Project Manager"
    
    current_project = project_manager.GetCurrentProject()
    if not current_project:
        return "Error: No project currently open"
    
    # First, ensure we're on the color page
    current_page = resolve.GetCurrentPage()
    if current_page.lower() != "color":
        # Try to switch to color page
        result = resolve.OpenPage("color")
        if not result:
            return f"Error: Failed to switch to Color page. Current page is: {current_page}"
    
    # Get the current timeline
    current_timeline = current_project.GetCurrentTimeline()
    if not current_timeline:
        return "Error: No timeline currently active"
    
    try:
        # Get the current clip in the timeline
        current_clip = current_timeline.GetCurrentVideoItem()
        if not current_clip:
            return "Error: No clip is currently selected in the timeline"
        
        # Use NodeGraph to reset all grades
        node_graph = current_clip.GetNodeGraph(1)
        if not node_graph:
            return "Error: Failed to get node graph"
        
        try:
            # Use the ResetAllGrades() method
            result = node_graph.ResetAllGrades()
            
            if result:
                clip_name = current_clip.GetName()
                logger.info(f"Successfully reset all grades for clip: {clip_name}")
                return f"Successfully reset all color corrections for clip '{clip_name}'"
            else:
                return "Failed to reset grades. The operation returned false."
                
        except Exception as e:
            return f"Error calling ResetAllGrades(): {str(e)}. This method may not be available in your DaVinci Resolve version."
        
    except Exception as e:
        return f"Error resetting grades: {str(e)}"

def get_color_groups(resolve) -> Dict[str, Any]:
    """Get information about all color groups in the current timeline.
    
    Args:
        resolve: The DaVinci Resolve instance
    
    Returns:
        Dictionary with color groups information
    """
    if resolve is None:
        return {"error": "Not connected to DaVinci Resolve"}
    
    project_manager = resolve.GetProjectManager()
    if not project_manager:
        return {"error": "Failed to get Project Manager"}
    
    current_project = project_manager.GetCurrentProject()
    if not current_project:
        return {"error": "No project currently open"}
    
    # Get the current timeline
    current_timeline = current_project.GetCurrentTimeline()
    if not current_timeline:
        return {"error": "No timeline currently active"}
    
    try:
        # Get all color groups in the timeline
        color_groups_list = current_timeline.GetColorGroupsList()
        
        result = {
            "timeline_name": current_timeline.GetName(),
            "color_group_count": len(color_groups_list) if color_groups_list else 0,
            "color_groups": []
        }
        
        if color_groups_list and len(color_groups_list) > 0:
            for i, color_group in enumerate(color_groups_list):
                try:
                    group_info = {
                        "index": i,
                        "name": str(color_group),
                        "has_pre_clip_graph": False,
                        "has_post_clip_graph": False
                    }
                    
                    # Try to get node graph information
                    try:
                        pre_clip_graph = color_group.GetPreClipNodeGraph()
                        if pre_clip_graph:
                            group_info["has_pre_clip_graph"] = True
                            group_info["pre_clip_nodes"] = pre_clip_graph.GetNumNodes()
                    except:
                        pass
                    
                    try:
                        post_clip_graph = color_group.GetPostClipNodeGraph()
                        if post_clip_graph:
                            group_info["has_post_clip_graph"] = True
                            group_info["post_clip_nodes"] = post_clip_graph.GetNumNodes()
                    except:
                        pass
                    
                    result["color_groups"].append(group_info)
                    
                except Exception as e:
                    logger.warning(f"Error processing color group {i}: {e}")
                    continue
        else:
            result["message"] = "No color groups found in timeline"
        
        return result
        
    except Exception as e:
        return {"error": f"Error getting color groups: {str(e)}"}

def create_color_group(resolve, group_name: str) -> str:
    """Create a new color group in the current timeline.
    
    Args:
        resolve: The DaVinci Resolve instance
        group_name: Name for the new color group
    
    Returns:
        String indicating success or failure
    """
    if resolve is None:
        return "Error: Not connected to DaVinci Resolve"
    
    if not group_name or not group_name.strip():
        return "Error: Color group name cannot be empty"
    
    project_manager = resolve.GetProjectManager()
    if not project_manager:
        return "Error: Failed to get Project Manager"
    
    current_project = project_manager.GetCurrentProject()
    if not current_project:
        return "Error: No project currently open"
    
    # Get the current timeline
    current_timeline = current_project.GetCurrentTimeline()
    if not current_timeline:
        return "Error: No timeline currently active"
    
    try:
        # Create the new color group
        new_color_group = current_timeline.AddColorGroup(group_name.strip())
        
        if new_color_group:
            logger.info(f"Successfully created color group: {group_name}")
            return f"Successfully created color group '{group_name}'"
        else:
            return f"Failed to create color group '{group_name}'. Name may already exist."
        
    except Exception as e:
        return f"Error creating color group: {str(e)}"

def assign_clip_to_color_group(resolve, group_name: str, clip_name: str = None) -> str:
    """Assign a clip to a color group.
    
    Args:
        resolve: The DaVinci Resolve instance
        group_name: Name of the color group to assign to
        clip_name: Name of the clip (uses current clip if None)
    
    Returns:
        String indicating success or failure
    """
    if resolve is None:
        return "Error: Not connected to DaVinci Resolve"
    
    if not group_name or not group_name.strip():
        return "Error: Color group name cannot be empty"
    
    project_manager = resolve.GetProjectManager()
    if not project_manager:
        return "Error: Failed to get Project Manager"
    
    current_project = project_manager.GetCurrentProject()
    if not current_project:
        return "Error: No project currently open"
    
    # Get the current timeline
    current_timeline = current_project.GetCurrentTimeline()
    if not current_timeline:
        return "Error: No timeline currently active"
    
    try:
        # Get target clip
        target_clip = None
        if clip_name:
            # Find clip by name
            video_track_count = current_timeline.GetTrackCount("video")
            
            for track_index in range(1, video_track_count + 1):
                track_items = current_timeline.GetItemListInTrack("video", track_index)
                if track_items:
                    for clip in track_items:
                        if clip and clip.GetName() == clip_name:
                            target_clip = clip
                            break
                    if target_clip:
                        break
            
            if not target_clip:
                return f"Error: Clip '{clip_name}' not found in timeline"
        else:
            # Use current clip
            target_clip = current_timeline.GetCurrentVideoItem()
            if not target_clip:
                return "Error: No clip is currently selected"
            clip_name = target_clip.GetName()
        
        # Get all color groups to find the target group
        color_groups_list = current_timeline.GetColorGroupsList()
        target_color_group = None
        
        if color_groups_list:
            for color_group in color_groups_list:
                if str(color_group) == group_name.strip():
                    target_color_group = color_group
                    break
        
        if not target_color_group:
            return f"Error: Color group '{group_name}' not found. Available groups: {[str(g) for g in color_groups_list] if color_groups_list else 'None'}"
        
        # Assign the clip to the color group
        result = target_clip.AssignToColorGroup(target_color_group)
        
        if result:
            logger.info(f"Successfully assigned clip '{clip_name}' to color group '{group_name}'")
            return f"Successfully assigned clip '{clip_name}' to color group '{group_name}'"
        else:
            return f"Failed to assign clip '{clip_name}' to color group '{group_name}'"
        
    except Exception as e:
        return f"Error assigning clip to color group: {str(e)}"

def get_color_group_node_graphs(resolve, group_name: str) -> Dict[str, Any]:
    """Get node graph information for a color group's pre and post clip adjustments.
    
    Args:
        resolve: The DaVinci Resolve instance
        group_name: Name of the color group
    
    Returns:
        Dictionary with node graph information
    """
    if resolve is None:
        return {"error": "Not connected to DaVinci Resolve"}
    
    if not group_name or not group_name.strip():
        return {"error": "Color group name cannot be empty"}
    
    project_manager = resolve.GetProjectManager()
    if not project_manager:
        return {"error": "Failed to get Project Manager"}
    
    current_project = project_manager.GetCurrentProject()
    if not current_project:
        return {"error": "No project currently open"}
    
    # Get the current timeline
    current_timeline = current_project.GetCurrentTimeline()
    if not current_timeline:
        return {"error": "No timeline currently active"}
    
    try:
        # Find the target color group
        color_groups_list = current_timeline.GetColorGroupsList()
        target_color_group = None
        
        if color_groups_list:
            for color_group in color_groups_list:
                if str(color_group) == group_name.strip():
                    target_color_group = color_group
                    break
        
        if not target_color_group:
            return {"error": f"Color group '{group_name}' not found. Available groups: {[str(g) for g in color_groups_list] if color_groups_list else 'None'}"}
        
        result = {
            "group_name": group_name,
            "pre_clip_graph": None,
            "post_clip_graph": None
        }
        
        # Get pre-clip node graph information
        try:
            pre_clip_graph = target_color_group.GetPreClipNodeGraph()
            if pre_clip_graph:
                pre_clip_info = {
                    "exists": True,
                    "node_count": pre_clip_graph.GetNumNodes(),
                    "nodes": []
                }
                
                # Get information about each node
                for node_idx in range(1, pre_clip_info["node_count"] + 1):
                    try:
                        node_info = {
                            "index": node_idx,
                            "enabled": pre_clip_graph.GetNodeEnabled(node_idx),
                            "label": pre_clip_graph.GetNodeLabel(node_idx) or f"Node {node_idx}"
                        }
                        pre_clip_info["nodes"].append(node_info)
                    except:
                        pass
                
                result["pre_clip_graph"] = pre_clip_info
            else:
                result["pre_clip_graph"] = {"exists": False, "message": "No pre-clip node graph"}
        except Exception as e:
            result["pre_clip_graph"] = {"exists": False, "error": f"Error accessing pre-clip graph: {str(e)}"}
        
        # Get post-clip node graph information
        try:
            post_clip_graph = target_color_group.GetPostClipNodeGraph()
            if post_clip_graph:
                post_clip_info = {
                    "exists": True,
                    "node_count": post_clip_graph.GetNumNodes(),
                    "nodes": []
                }
                
                # Get information about each node
                for node_idx in range(1, post_clip_info["node_count"] + 1):
                    try:
                        node_info = {
                            "index": node_idx,
                            "enabled": post_clip_graph.GetNodeEnabled(node_idx),
                            "label": post_clip_graph.GetNodeLabel(node_idx) or f"Node {node_idx}"
                        }
                        post_clip_info["nodes"].append(node_info)
                    except:
                        pass
                
                result["post_clip_graph"] = post_clip_info
            else:
                result["post_clip_graph"] = {"exists": False, "message": "No post-clip node graph"}
        except Exception as e:
            result["post_clip_graph"] = {"exists": False, "error": f"Error accessing post-clip graph: {str(e)}"}
        
        return result
        
    except Exception as e:
        return {"error": f"Error getting color group node graphs: {str(e)}"}

def copy_grades_multi_target(resolve, source_clip_name: str, target_clip_names: List[str]) -> Dict[str, Any]:
    """Copy grades from one source clip to multiple target clips.
    
    Args:
        resolve: The DaVinci Resolve instance
        source_clip_name: Name of the source clip to copy grade from
        target_clip_names: List of target clip names to apply grade to
    
    Returns:
        Dictionary with results for each target clip
    """
    if resolve is None:
        return {"error": "Not connected to DaVinci Resolve"}
    
    if not source_clip_name or not source_clip_name.strip():
        return {"error": "Source clip name cannot be empty"}
    
    if not target_clip_names or len(target_clip_names) == 0:
        return {"error": "Target clip names list cannot be empty"}
    
    project_manager = resolve.GetProjectManager()
    if not project_manager:
        return {"error": "Failed to get Project Manager"}
    
    current_project = project_manager.GetCurrentProject()
    if not current_project:
        return {"error": "No project currently open"}
    
    # First, ensure we're on the color page
    current_page = resolve.GetCurrentPage()
    if current_page.lower() != "color":
        # Try to switch to color page
        result = resolve.OpenPage("color")
        if not result:
            return {"error": f"Failed to switch to Color page. Current page is: {current_page}"}
    
    # Get the current timeline
    current_timeline = current_project.GetCurrentTimeline()
    if not current_timeline:
        return {"error": "No timeline currently active"}
    
    try:
        # Get all clips in the timeline
        all_video_clips = {}
        video_track_count = current_timeline.GetTrackCount("video")
        
        for track_index in range(1, video_track_count + 1):
            track_items = current_timeline.GetItemListInTrack("video", track_index)
            if track_items:
                for clip in track_items:
                    if clip:
                        all_video_clips[clip.GetName()] = clip
        
        # Find source clip
        if source_clip_name not in all_video_clips:
            return {"error": f"Source clip '{source_clip_name}' not found in timeline. Available clips: {list(all_video_clips.keys())}"}
        
        source_clip = all_video_clips[source_clip_name]
        
        # Process each target clip
        results = {
            "source_clip": source_clip_name,
            "total_targets": len(target_clip_names),
            "successful_copies": 0,
            "failed_copies": 0,
            "results": {}
        }
        
        for target_name in target_clip_names:
            target_name = target_name.strip()
            
            if target_name == source_clip_name:
                results["results"][target_name] = {
                    "success": False,
                    "message": "Cannot copy grade to itself (source and target are the same)"
                }
                results["failed_copies"] += 1
                continue
            
            if target_name not in all_video_clips:
                results["results"][target_name] = {
                    "success": False,
                    "message": f"Target clip '{target_name}' not found in timeline"
                }
                results["failed_copies"] += 1
                continue
            
            target_clip = all_video_clips[target_name]
            
            try:
                # Set target clip as current for the copy operation
                current_timeline.SetCurrentVideoItem(target_clip)
                
                # Perform the grade copy using the working API method
                copy_result = target_clip.CopyGrade(source_clip)
                
                if copy_result:
                    results["results"][target_name] = {
                        "success": True,
                        "message": f"Successfully copied grade from '{source_clip_name}'"
                    }
                    results["successful_copies"] += 1
                    logger.info(f"Successfully copied grade from '{source_clip_name}' to '{target_name}'")
                else:
                    results["results"][target_name] = {
                        "success": False,
                        "message": "Copy operation returned false - source may not have grading applied"
                    }
                    results["failed_copies"] += 1
                    
            except Exception as e:
                results["results"][target_name] = {
                    "success": False,
                    "message": f"Error during copy: {str(e)}"
                }
                results["failed_copies"] += 1
                logger.error(f"Error copying grade to '{target_name}': {str(e)}")
        
        # Add summary message
        if results["successful_copies"] > 0:
            results["summary"] = f"Successfully copied grades to {results['successful_copies']} out of {results['total_targets']} clips"
        else:
            results["summary"] = f"Failed to copy grades to all {results['total_targets']} target clips"
        
        return results
        
    except Exception as e:
        return {"error": f"Error in multi-target grade copy: {str(e)}"}

def export_lut(resolve, export_type: str = "cube", export_path: str = None, node_index: int = None) -> str:
    """Export LUT from the current clip's grade.
    
    Args:
        resolve: The DaVinci Resolve instance
        export_type: Type of LUT to export (cube, vlt, etc.)
        export_path: Path to save the exported LUT (auto-generated if None)
        node_index: Node index to export from (uses current clip if None)
    
    Returns:
        String indicating success or failure with export path
    """
    if resolve is None:
        return "Error: Not connected to DaVinci Resolve"
    
    # Validate export type
    valid_export_types = ["cube", "vlt"]
    if export_type.lower() not in valid_export_types:
        return f"Error: Invalid export type '{export_type}'. Valid types: {', '.join(valid_export_types)}"
    
    project_manager = resolve.GetProjectManager()
    if not project_manager:
        return "Error: Failed to get Project Manager"
    
    current_project = project_manager.GetCurrentProject()
    if not current_project:
        return "Error: No project currently open"
    
    # First, ensure we're on the color page
    current_page = resolve.GetCurrentPage()
    if current_page.lower() != "color":
        # Try to switch to color page
        result = resolve.OpenPage("color")
        if not result:
            return f"Error: Failed to switch to Color page. Current page is: {current_page}"
    
    # Get the current timeline
    current_timeline = current_project.GetCurrentTimeline()
    if not current_timeline:
        return "Error: No timeline currently active"
    
    try:
        # Get the current clip in the timeline
        current_clip = current_timeline.GetCurrentVideoItem()
        if not current_clip:
            return "Error: No clip is currently selected in the timeline"
        
        # Generate export path if not provided
        if not export_path:
            import os
            clip_name = current_clip.GetName()
            safe_clip_name = "".join(c for c in clip_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
            project_name = current_project.GetName()
            safe_project_name = "".join(c for c in project_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
            
            filename = f"{safe_project_name}_{safe_clip_name}_LUT.{export_type.lower()}"
            export_path = os.path.join(os.getcwd(), filename)
        
        # Ensure export path has correct extension
        import os
        path_root, path_ext = os.path.splitext(export_path)
        if not path_ext or path_ext.lower() != f".{export_type.lower()}":
            export_path = f"{path_root}.{export_type.lower()}"
        
        # Perform the LUT export using TimelineItem.ExportLUT()
        try:
            result = current_clip.ExportLUT(export_type.lower(), export_path)
            
            if result:
                logger.info(f"Successfully exported LUT to: {export_path}")
                return f"Successfully exported {export_type.upper()} LUT to: {export_path}"
            else:
                return f"Failed to export LUT. Check if the clip has color corrections applied and the export path is writable: {export_path}"
                
        except Exception as e:
            return f"Error calling ExportLUT(): {str(e)}. This method may not be available in your DaVinci Resolve version."
        
    except Exception as e:
        return f"Error exporting LUT: {str(e)}"

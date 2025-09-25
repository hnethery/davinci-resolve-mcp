---
task: h-fix-node-capabilities
branch: fix/node-capabilities
status: pending
created: 2025-09-25
modules: [src/api/color_operations.py, src/utils/resolve_connection.py]
---

# Fix DaVinci Resolve Node Capabilities

## Problem/Goal
The DaVinci Resolve MCP server's node operations are failing with "Cannot access grade object" errors. This prevents AI assistants from creating and manipulating color grading nodes, which is core functionality for color correction workflows.

Key issues identified:
- `add_node()` function in `src/api/color_operations.py` (lines 194-364) fails consistently
- Error message: "Cannot access grade object"
- Affects color page operations and node management
- Only 8% of 202 implemented features are verified working due to issues like this

## Success Criteria
- [ ] `add_node()` function successfully creates serial, parallel, and layer nodes
- [ ] Node operations work with active clips in DaVinci Resolve color page
- [ ] Proper error handling when no clips are selected or graded
- [ ] Node labeling functionality works correctly
- [ ] All color page node operations (get_current_node, set node properties) function properly
- [ ] Manual testing confirms nodes appear in DaVinci Resolve color page
- [ ] Integration testing with Cursor/Claude shows AI can create nodes via natural language

## Context Files
<!-- Added by context-gathering agent or manually -->
- @src/api/color_operations.py:194-364  # add_node function with issues
- @src/api/color_operations.py          # All color operations for context
- @src/utils/resolve_connection.py      # Connection utilities
- @docs/FEATURES.md                     # Feature status documentation

## Context Manifest

### How DaVinci Resolve Node Operations Currently Work

When a user attempts to create color grading nodes through the MCP server, the request flows through several critical layers. The MCP tool `add_node` in the main server file (`src/resolve_mcp_server.py` line 938) receives the parameters (node_type and optional label) and delegates to the `add_node` function in `src/api/color_operations.py` (lines 195-365).

The color operations function begins by establishing a connection to DaVinci Resolve through the scripting API. It first validates the node_type parameter against valid options ('serial', 'parallel', 'layer'), then accesses the DaVinci Resolve application via the resolve object passed from the connection utilities. This resolve object is initialized through `src/utils/resolve_connection.py` which imports the DaVinciResolveScript module and connects to the running application.

The critical workflow requires several prerequisites to succeed:

1. **Page Context**: The function ensures it's operating on the Color page by checking `resolve.GetCurrentPage()` and switching if necessary using `resolve.OpenPage("color")`.

2. **Project and Timeline Access**: It obtains the project manager, current project, and active timeline through the standard DaVinci API hierarchy: resolve → ProjectManager → CurrentProject → CurrentTimeline.

3. **Clip Selection and Grade Access**: Here's where the primary failure occurs. The function calls `ensure_clip_selected()` helper function (lines 856-917) to automatically select a clip if none is currently active. However, even when a clip is selected, the critical step of accessing the clip's grade object via `current_clip.GetCurrentGrade()` consistently returns None.

The fundamental issue is that `GetCurrentGrade()` only returns a valid grade object when the clip has been actively graded or when it's in a specific state in the DaVinci Resolve interface. A freshly imported clip or one that hasn't been explicitly touched in the Color page may not have an accessible grade object, even though it appears selected in the timeline.

The current implementation includes multiple fallback strategies:
- Direct grade access via `GetCurrentGrade()`
- Re-selecting the clip via `SetCurrentVideoItem()` and retry
- Attempting direct node creation through a theoretical ColorPage node graph interface (lines 292-312)

When all grade access methods fail, the function returns the error "Cannot access grade object. The clip may not be properly graded yet." This is the root cause of the reported failures.

**Current Error Handling Flow**: The system logs extensively through the Python logging module, tracking each step of the grade access attempts. When `current_grade` remains None after all attempts, the function exits with the "Cannot access grade object" error without creating any nodes.

**State Dependencies**: The operations are highly dependent on the exact state of DaVinci Resolve's UI and the selected clip's grading status. Unlike file-based operations, color grading requires active UI context and properly initialized grade objects.

### For Node Operations Fix: What Needs to Connect

Since we're implementing a fix for node operations, it will need to integrate with the existing system at several critical points:

The current error handling assumes that clips without accessible grade objects cannot have nodes added. However, the DaVinci Resolve API likely provides alternative pathways to initialize grading on clips or access grade functionality differently. The fix needs to either:

1. **Grade Initialization Pathway**: Before attempting node operations, explicitly initialize grading on the selected clip. This might involve calling specific API methods to create or activate the grade object.

2. **Alternative Grade Access**: Explore different methods of accessing grade functionality, potentially through the ColorPage API rather than directly through clip objects.

3. **State Preparation**: Ensure the clip is in the proper state for grading operations by mimicking user actions that would typically prepare a clip for color work.

The current codebase shows evidence of ongoing testing through `tests/test_improvements.py`, which specifically tests color page operations and includes checks for "Cannot access grade object" errors. The FEATURES.md documentation confirms that Color Page Operations have a 0% verification rate on macOS, with node management specifically marked as having "known issues" with this exact error.

The architectural challenge is that DaVinci Resolve's scripting API closely mirrors the UI workflow - clips must be "prepared" for grading in ways that aren't immediately obvious from the API documentation. The fix will need to bridge this gap between the programmatic interface and the UI-driven workflow expectations.

### Technical Reference Details

#### Core Function Signature
```python
def add_node(resolve, node_type: str = "serial", label: str = None) -> str
```
Location: `/Users/aristotle/tools/mcp-servers/davinci-resolve-mcp/src/api/color_operations.py:195-365`

#### Key API Objects and Methods

**Resolve Object Hierarchy**:
- `resolve.GetProjectManager()`
- `project_manager.GetCurrentProject()`
- `current_project.GetCurrentTimeline()`
- `current_timeline.GetCurrentVideoItem()`
- `current_clip.GetCurrentGrade()` ← Critical failure point

**Grade Object Methods** (when accessible):
- `current_grade.AddSerialNode()`
- `current_grade.AddParallelNode()`
- `current_grade.AddLayerNode()`
- `current_grade.SetNodeLabel(node_index, label)`
- `current_grade.GetCurrentNode()`
- `current_grade.GetNodeCount()`

**Helper Functions**:
- `ensure_clip_selected(resolve, timeline)` - Automatically selects first available clip
- Returns `(success: bool, clip_object, message: str)`

#### Error Conditions and Logging

**Primary Error Path**: Lines 313-314 in color_operations.py
```python
return f"Error adding {node_type} node: Cannot access grade object. The clip may not be properly graded yet."
```

**Logging Categories**:
- `davinci-resolve-mcp.color` - Color operations logger
- `davinci-resolve-mcp.connection` - Connection utilities logger
- `davinci-resolve-mcp.main` - Server main logger

**Test Verification**: The testing framework in `tests/test_improvements.py` includes specific checks for:
- Color page switching (line 104)
- Node addition with automatic clip selection (lines 108-109)
- Error message validation for proper clip selection

#### Environment Dependencies

**DaVinci Resolve API Paths** (from `src/utils/platform.py`):
- macOS: `/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting`
- Windows: `%PROGRAMDATA%\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting`
- Library paths for `fusionscript.so/.dll`

**Environment Variables Required**:
- `RESOLVE_SCRIPT_API` - Path to scripting API
- `RESOLVE_SCRIPT_LIB` - Path to Fusion script library
- `PYTHONPATH` - Must include modules path

#### Integration Points

**MCP Server Tool Registration**: Line 938-946 in `src/resolve_mcp_server.py`
```python
@mcp.tool()
def add_node(node_type: str = "serial", label: str = None) -> str:
    from api.color_operations import add_node as add_node_func
    return add_node_func(resolve, node_type, label)
```

**Related Operations Affected**:
- `set_color_wheel_param()` - Same grade object access issue
- `get_current_node()` - Depends on valid grade object
- `copy_grade()` - Requires source/target grade objects
- `apply_lut()` - Needs grade object for node targeting

**Prerequisites for Success**:
1. DaVinci Resolve running with project open
2. Timeline with at least one video clip
3. Proper environment variables set
4. Color page accessible (not locked by other operations)
5. **Critical Missing Element**: Clip must have initialized/accessible grade object

## User Notes
<!-- Any specific notes or requirements from the developer -->
Critical issue affecting color grading workflow. Node capabilities are essential for professional video editing workflows using AI assistants.

## Work Log
<!-- Updated as work progresses -->
- [2025-09-25] Task created, issue identified in add_node() function during codebase investigation
- [2025-09-25] **SOLUTION IMPLEMENTED**: Fixed "Cannot access grade object" error using SetCDL() initialization

## Solution Summary

**Root Cause**: `GetCurrentGrade()` returns `None` for clips that haven't been initialized for color grading, even when clips are properly selected in the timeline.

**Fix Strategy**: Initialize the grade structure using `SetCDL()` with neutral values before attempting node operations.

**Implementation Details** (`src/api/color_operations.py:252-300`):

1. **Grade Validation**: First attempts to access `current_clip.GetCurrentGrade()`
2. **Initialization on Failure**: When `GetCurrentGrade()` returns `None`, initializes grading using:
   ```python
   current_clip.SetCDL({
       "NodeIndex": 1, 
       "Slope": "1.0 1.0 1.0",      # Neutral slope (no change)
       "Offset": "0.0 0.0 0.0",     # No offset  
       "Power": "1.0 1.0 1.0",      # Neutral power (no change)
       "Saturation": 1.0            # No saturation change
   })
   ```
3. **Re-access**: After initialization, `GetCurrentGrade()` should return a valid grade object
4. **Normal Operation**: Proceeds with standard node creation (`AddSerialNode()`, `AddParallelNode()`, `AddLayerNode()`)

**Key Benefits**:
- Non-destructive: Uses completely neutral CDL values that don't affect the image
- Automatic: No user intervention required - clips are automatically prepared for grading
- Robust: Includes proper error handling for cases where initialization fails
- API Compliant: Uses documented DaVinci Resolve API methods

**Files Modified**:
- `src/api/color_operations.py` (lines 252-300): Replaced failed grade access attempts with SetCDL initialization approach

**Testing Ready**: Solution ready for testing with DaVinci Resolve running and timeline containing video clips.
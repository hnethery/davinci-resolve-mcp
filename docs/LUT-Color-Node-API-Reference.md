# DaVinci Resolve LUT/Color/Node API Reference

*Extracted from official DaVinci Resolve scripting documentation*

## Core API Architecture

```python
resolve = dvr_script.scriptapp("Resolve")
project = resolve.GetProjectManager().GetCurrentProject()
timeline = project.GetCurrentTimeline()
timeline_item = timeline.GetCurrentVideoItem()

# Two ways to access node operations:
node_graph = timeline_item.GetNodeGraph()      # Primary method
# OR for specific layers:
node_graph = timeline_item.GetNodeGraph(layerIdx)  # 1 <= layerIdx <= nodeStackLayers
```

## 🎨 COLOR OPERATIONS

### CDL (Color Decision List) Operations
```python
# ✅ CONFIRMED WORKING - SetCDL()
timeline_item.SetCDL({
    "NodeIndex": "1",           # MUST be string, not integer!
    "Slope": "0.5 0.4 0.2",     # RGB highlights (gain)
    "Offset": "0.4 0.3 0.2",    # RGB shadows (lift)
    "Power": "0.6 0.7 0.8",     # RGB midtones (gamma)
    "Saturation": "0.65"        # Overall saturation
})
# Returns: Bool

# ❌ GetCDL() DOES NOT EXIST - Cannot read current CDL values
```

### Color Groups
```python
# Timeline color group management
color_groups = timeline.GetColorGroupsList()           # Returns: [ColorGroup...]
new_group = timeline.AddColorGroup(groupName)          # Returns: ColorGroup
timeline.DeleteColorGroup(colorGroup)                  # Returns: Bool

# Individual timeline item color group operations
current_group = timeline_item.GetColorGroup()          # Returns: ColorGroup or None
timeline_item.AssignToColorGroup(ColorGroup)           # Returns: Bool
timeline_item.RemoveFromColorGroup()                   # Returns: Bool

# ColorGroup node graph access (POWERFUL!)
color_group = timeline_item.GetColorGroup()
pre_clip_graph = color_group.GetPreClipNodeGraph()     # Returns: Graph
post_clip_graph = color_group.GetPostClipNodeGraph()   # Returns: Graph
```

## 🎬 NODE OPERATIONS

### Node Graph Management
```python
# Basic node information
node_count = node_graph.GetNumNodes()                  # Returns: int
node_label = node_graph.GetNodeLabel(nodeIndex)        # Returns: string
tools_list = node_graph.GetToolsInNode(nodeIndex)      # Returns: [toolsList] - MISSING FROM MCP!

# Node state control
node_graph.SetNodeEnabled(nodeIndex, isEnabled)        # Returns: Bool (1 <= nodeIndex <= GetNumNodes())
is_enabled = node_graph.GetNodeEnabled(nodeIndex)      # [Inferred from SetNodeEnabled usage]
```

### Node Cache Control
```python
# Cache management per node
node_graph.SetNodeCacheMode(nodeIndex, cache_value)    # Returns: Bool
current_cache = node_graph.GetNodeCacheMode(nodeIndex) # Returns: cache_value

# Cache values:
resolve.CACHE_AUTO_ENABLED = -1
resolve.CACHE_DISABLED = 0
resolve.CACHE_ENABLED = 1
```

### Advanced Grade Operations
```python
# Still file operations (.drx files)
node_graph.ApplyGradeFromDRX(path, gradeMode)          # Returns: Bool
# gradeMode: 0="No keyframes", 1="Source Timecode aligned", 2="Start Frames aligned"

# ARRI-specific operations
node_graph.ApplyArriCdlLut()                           # Returns: Bool

# Reset operations
node_graph.ResetAllGrades()                             # Returns: Bool - MISSING FROM MCP!
```

## 🎭 LUT OPERATIONS

### Dual LUT API Access
```python
# NodeGraph LUT operations (Primary)
node_graph.SetLUT(nodeIndex, lutPath)                  # Returns: Bool (✅ USING)
current_lut_path = node_graph.GetLUT(nodeIndex)        # Returns: String (❌ NOT USING!)

# TimelineItem LUT operations (Alternative)
timeline_item.SetLUT(nodeIndex, lutPath)               # Returns: Bool (❌ NOT USING!)
current_lut_path = timeline_item.GetLUT(nodeIndex)     # Returns: String (❌ NOT USING!)

# TimelineItem direct node access
node_count = timeline_item.GetNumNodes()               # Returns: int (❌ NOT USING!)
node_label = timeline_item.GetNodeLabel(nodeIndex)     # Returns: string (❌ NOT USING!)
```

### LUT Export
```python
# Export LUTs from timeline items
timeline_item.ExportLUT(exportType, path)              # Returns: Bool
# path should include intended filename
# Empty/incorrect extension gets appropriate extension (.cube/.vlt) appended
```

## 📋 COPY & GRADE OPERATIONS

### Grade Copying
```python
# Single target copy (✅ USING)
target_clip.CopyGrade(source_clip)                     # Returns: Bool

# Multiple target copy (❌ NOT USING!)
timeline_item.CopyGrades([tgtTimelineItems])           # Returns: Bool
# Copies current node stack layer grade to same layer for each target
```

## 🚨 CRITICAL API NOTES

### Version Requirements
- **From v16.2.0+**: nodeIndex parameters are 1-based, not 0-based
- Valid range: `1 <= nodeIndex <= total number of nodes`

### Parameter Format Requirements
- **CDL NodeIndex**: MUST be string `"1"`, not integer `1`
- **CDL RGB values**: Space-separated strings `"0.5 0.4 0.2"`
- **LUT paths**: Can be absolute or relative to custom/master LUT paths

### API Limitations
- **GetCDL()** does not exist - can only write CDL, cannot read
- **Node creation** not supported programmatically (AddSerialNode, etc. don't exist)
- **Current node selection** concept doesn't exist in API

## 🔧 MISSING FROM CURRENT MCP SERVER

### High Priority Additions:
1. **GetLUT()** - Read current LUT paths from nodes for validation
2. **GetToolsInNode()** - Inspect what tools are active in each node
3. **ResetAllGrades()** - Reset all color corrections
4. **ApplyGradeFromDRX()** - Import .drx still files
5. **TimelineItem LUT methods** - Alternative LUT access methods
6. **ColorGroup node graphs** - Access pre/post clip adjustments
7. **Multi-target CopyGrades()** - Copy grades to multiple clips at once

### Medium Priority:
1. **Node cache control** - SetNodeCacheMode/GetNodeCacheMode
2. **LUT export** - ExportLUT functionality
3. **Timeline item direct node access** - GetNumNodes/GetNodeLabel alternatives

## 📚 REFERENCE SOURCES
- DaVinci Resolve Scripting Documentation (Parts 1-4)
- Official Blackmagic Design API Reference
- Verified against DaVinci Resolve v18.1+ compatibility
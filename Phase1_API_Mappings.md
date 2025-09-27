# Phase 1 - API Equivalents Mapping

## Real DaVinci Resolve API vs. Non-Existent Grade Methods

### ❌ BROKEN PATTERN (What We Currently Use)
```python
# THIS DOESN'T WORK - GetCurrentGrade() returns None
current_grade = current_item.GetCurrentGrade()  # Returns None!
current_grade.SetLiftR(node_index, value)      # NoneType error
current_grade.ApplyLUT(node_index, lut_path)   # NoneType error
current_grade.GetCurrentNode()                 # NoneType error
```

### ✅ WORKING PATTERN (What We Should Use)

## 1. Primary Color Correction

### Current Broken Code:
```python
current_grade = current_item.GetCurrentGrade()
current_grade.SetLiftR(node_index, 0.1)
current_grade.SetGammaG(node_index, 0.95)
```

### Working Replacement:
```python
# Use CDL (Color Decision List) operations
result = current_item.SetCDL({
    "NodeIndex": 1,                     # Target node (1-based indexing)
    "Slope": "1.1 1.0 0.9",            # RGB gain/contrast (Gain wheel)
    "Offset": "0.05 0.0 -0.05",        # RGB lift/shadows (Lift wheel) 
    "Power": "1.0 1.0 1.0",            # RGB gamma/midtones (Gamma wheel)
    "Saturation": 1.1                   # Overall saturation
})

# Get current CDL values
cdl_values = current_item.GetCDL(node_index)
```

## 2. LUT Operations

### Current Broken Code:
```python
current_grade = current_item.GetCurrentGrade()
current_grade.ApplyLUT(node_index, lut_path)
```

### Working Replacements:
```python
# Option 1: Direct on TimelineItem
result = current_item.SetLUT(node_index, lut_path)

# Option 2: Via NodeGraph
node_graph = current_item.GetNodeGraph()
result = node_graph.SetLUT(node_index, lut_path)
```

## 3. Node Management

### Current Broken Code:
```python
current_grade = current_item.GetCurrentGrade()
node_count = current_grade.GetNodeCount()
current_node = current_grade.GetCurrentNode()
node_name = current_grade.GetNodeName(index)
```

### Working Replacement:
```python
# Access via NodeGraph
node_graph = current_item.GetNodeGraph()
node_count = node_graph.GetNumNodes()
node_label = node_graph.GetNodeLabel(index)
is_enabled = node_graph.GetNodeEnabled(index)

# Node control
node_graph.SetNodeEnabled(index, True/False)
```

## 4. Node Creation (NOT SUPPORTED)

### Current Broken Code:
```python
current_grade = current_item.GetCurrentGrade()
current_grade.AddSerialNode()
current_grade.AddParallelNode()
```

### Reality:
```python
# These methods DO NOT EXIST in the API
# Node creation must be done manually in DaVinci Resolve UI
# This is an API limitation, not a bug
```

## 5. Grade Operations

### Current Broken Code:
```python
source_grade = source_item.GetCurrentGrade()
target_grade = target_item.GetCurrentGrade()
result = target_grade.CopyFromNodeToNode(source_grade, 1, 1)
```

### Working Replacement:
```python
# Use built-in grade copying
result = target_item.CopyGrade(source_item)

# For advanced workflows
node_graph = target_item.GetNodeGraph()
node_graph.ApplyGradeFromDRX(grade_file_path)    # Import from file
node_graph.ApplyArriCdlLut()                     # ARRI workflows
```

## Complete API Method Mapping

| Broken Grade Method | Working Replacement | Notes |
|--------------------|-------------------|--------|
| `GetCurrentGrade()` | `GetNodeGraph()` | Grade object doesn't exist |
| `SetLiftR/G/B/Y()` | `SetCDL()` with Offset | Use CDL Offset for lift/shadows |
| `SetGammaR/G/B/Y()` | `SetCDL()` with Power | Use CDL Power for gamma/midtones |
| `SetGainR/G/B/Y()` | `SetCDL()` with Slope | Use CDL Slope for gain/highlights |
| `ApplyLUT()` | `SetLUT()` | Works on TimelineItem/NodeGraph |
| `GetCurrentNode()` | Not directly available | Use GetNodeLabel() iteration |
| `GetNodeCount()` | `GetNumNodes()` | Available on NodeGraph |
| `GetNodeName()` | `GetNodeLabel()` | Available on NodeGraph |
| `IsSerial/Parallel/Layer()` | Not available | Node type detection not supported |
| `AddSerialNode()` | **NOT SUPPORTED** | Must be done manually in UI |
| `DeleteNode()` | **NOT SUPPORTED** | Must be done manually in UI |
| `CopyFromNodeToNode()` | `CopyGrade()` | Full grade copy only |

## CDL Parameters Mapping

| Color Wheel | CDL Parameter | Value Range | Description |
|------------|---------------|-------------|-------------|
| **Lift** (Shadows) | `Offset` | "-1.0 -1.0 -1.0" to "1.0 1.0 1.0" | RGB lift/shadow adjustment |
| **Gamma** (Midtones) | `Power` | "0.1 0.1 0.1" to "10.0 10.0 10.0" | RGB gamma/midtone adjustment |  
| **Gain** (Highlights) | `Slope` | "0.1 0.1 0.1" to "10.0 10.0 10.0" | RGB gain/highlight adjustment |
| **Saturation** | `Saturation` | 0.0 to 2.0+ | Overall saturation multiplier |

## NodeGraph Object Methods (Confirmed Working)

```python
node_graph = current_item.GetNodeGraph()

# Node Information
node_graph.GetNumNodes()                    # Get node count
node_graph.GetNodeLabel(index)             # Get node name/label
node_graph.GetNodeEnabled(index)           # Check if node enabled

# Node Control  
node_graph.SetNodeEnabled(index, boolean)  # Enable/disable node
node_graph.SetLUT(index, lut_path)         # Apply LUT to specific node

# Grade Operations
node_graph.ResetAllGrades()                # Reset entire grade
node_graph.ApplyGradeFromDRX(file_path)   # Import grade from DRX file
node_graph.ApplyArriCdlLut()              # ARRI workflow operations
```

## Key Insights

1. **No Grade Object**: The `Grade` object concept doesn't exist in the real API
2. **CDL is King**: Primary color correction must use CDL operations
3. **NodeGraph for Advanced**: Node-level operations require NodeGraph access
4. **API Limitations**: Node creation/deletion not supported programmatically
5. **TimelineItem Direct**: Many operations work directly on TimelineItem
6. **1-Based Indexing**: NodeIndex parameters use 1-based indexing (not 0-based)

## Implementation Strategy

### Phase 2-3: Replace all Grade calls with:
1. **Color Wheels** → CDL operations (`SetCDL`, `GetCDL`)
2. **Node Info** → NodeGraph methods (`GetNumNodes`, `GetNodeLabel`)
3. **LUT Operations** → TimelineItem/NodeGraph LUT methods
4. **Grade Copy** → TimelineItem grade copy methods
5. **Node Creation** → Error messages explaining API limitation
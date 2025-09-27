# Phase 1 - Broken Functions Audit

## Complete List of Functions Calling GetCurrentGrade() and Other Non-existent Methods

### Core Issue
**Root Cause**: `current_clip.GetCurrentGrade()` returns `None` because the Grade object and its methods **DO NOT EXIST** in the real DaVinci Resolve API.

### Functions with GetCurrentGrade() Calls

#### 1. **get_current_node()** - `src/api/color_operations.py:49`
- **Primary Issue**: `current_grade = current_clip.GetCurrentGrade()` → Returns None
- **Broken Methods Called**:
  - `current_grade.GetCurrentNode()` (line 54)  
  - `current_grade.GetNodeCount()` (line 59)
  - `current_grade.IsSerial()` (line 66)
  - `current_grade.IsParallel()` (line 67)  
  - `current_grade.IsLayer()` (line 68)
  - `current_grade.GetNodeName()` (line 73)

#### 2. **apply_lut()** - `src/api/color_operations.py:162`
- **Primary Issue**: `current_grade = current_clip.GetCurrentGrade()` → Returns None
- **Broken Methods Called**:
  - `current_grade.GetCurrentNode()` (line 170)
  - `current_grade.GetNodeCount()` (line 175)
  - `current_grade.ApplyLUT()` (line 180)
  - `current_grade.GetNodeName()` (line 185)

#### 3. **add_node()** - `src/api/color_operations.py:281, 299, 314` 
- **Primary Issue**: Multiple `current_grade = current_clip.GetCurrentGrade()` calls → All return None
- **Broken Methods Called**:
  - All the methods from `get_current_node()` and `apply_lut()`
  - **NOTE**: Function already contains comments acknowledging that `AddSerialNode()`, `AddParallelNode()`, and `AddLayerNode()` don't exist

#### 4. **copy_grade()** - `src/api/color_operations.py:415, 448`
- **Primary Issue**: 
  - `source_grade = source_clip.GetCurrentGrade()` (line 415) → Returns None
  - `target_grade = target_clip.GetCurrentGrade()` (line 448) → Returns None
- **Broken Methods Called**:
  - `source_grade.GetCurrentNode()` (line 462)
  - `target_grade.GetCurrentNode()` (line 463)
  - `source_grade.GetNodeCount()` (line 475)
  - `target_grade.GetNodeCount()` (line 481)
  - `target_grade.DeleteNode()` (line 483)
  - `source_grade.IsSerial()` (line 488)
  - `source_grade.IsParallel()` (line 490)
  - `source_grade.IsLayer()` (line 492)
  - `target_grade.AddSerialNode()` (line 489)
  - `target_grade.AddParallelNode()` (line 491)
  - `target_grade.AddLayerNode()` (line 493)
  - `target_grade.GetCurrentNode()` (line 496)

#### 5. **get_color_wheels()** - `src/api/color_operations.py:548`
- **Primary Issue**: `current_grade = current_clip.GetCurrentGrade()` → Returns None
- **Broken Methods Called**:
  - `current_grade.GetCurrentNode()` (line 556)
  - `current_grade.GetNodeCount()` (line 561)
  - `current_grade.GetNodeName()` (line 568)
  - Dynamic method calls like `current_grade.GetLiftR()`, `GetGammaG()`, etc.

#### 6. **set_color_wheel_param()** - `src/api/color_operations.py:740, 761`
- **Primary Issue**: Multiple `current_grade = current_clip.GetCurrentGrade()` calls → All return None
- **Broken Methods Called**:
  - `current_grade.GetCurrentNode()` (line 779)
  - `current_grade.GetNodeCount()` (line 787)
  - `current_grade.GetNodeName()` (line 796)
  - Dynamic method calls like `current_grade.SetLiftR()`, `SetGammaG()`, etc.

### Summary of Non-Existent API Methods

| Method Category | Methods That Don't Exist |
|----------------|---------------------------|
| **Grade Access** | `GetCurrentGrade()` |
| **Node Info** | `GetCurrentNode()`, `GetNodeCount()`, `GetNodeName()` |
| **Node Types** | `IsSerial()`, `IsParallel()`, `IsLayer()` |
| **Node Creation** | `AddSerialNode()`, `AddParallelNode()`, `AddLayerNode()` |
| **Node Management** | `DeleteNode()` |
| **LUT Operations** | `ApplyLUT()` (on Grade object) |
| **Color Wheels** | `SetLiftR()`, `SetLiftG()`, `SetLiftB()`, `SetLiftY()` |
| | `SetGammaR()`, `SetGammaG()`, `SetGammaB()`, `SetGammaY()` |
| | `SetGainR()`, `SetGainG()`, `SetGainB()`, `SetGainY()` |
| | `SetOffsetR()`, `SetOffsetG()`, `SetOffsetB()`, `SetOffsetY()` |
| | `GetLiftR()`, `GetGammaG()`, etc. (all getter variants) |
| **Grade Copy** | `CopyFromNodeToNode()` |

### Functions That Are Completely Broken
**ALL 6 FUNCTIONS** listed above are completely non-functional due to the Grade object not existing.

### Impact Assessment
- **Primary Color Correction**: Completely broken
- **LUT Operations**: Broken on Grade level (but may work on TimelineItem level)
- **Node Management**: Completely broken
- **Color Workflows**: Completely broken
- **Grade Copying**: Completely broken

### Error Pattern
Every function follows this pattern:
1. `current_grade = current_clip.GetCurrentGrade()` → Returns `None`
2. `current_grade.SomeMethod()` → `'NoneType' object has no attribute 'SomeMethod'` → **AttributeError/TypeError**

**Result**: All color operations fail with NoneType errors.
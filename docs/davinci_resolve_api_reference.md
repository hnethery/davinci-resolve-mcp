# DaVinci Resolve API Reference

Complete reference of all available methods and properties in the DaVinci Resolve API, discovered through introspection.

## Resolve Object (23 methods)

### Layout Preset Management
- `DeleteLayoutPreset()` - PyFunctionCall
- `ExportLayoutPreset()` - PyFunctionCall
- `ImportLayoutPreset()` - PyFunctionCall
- `LoadLayoutPreset()` - PyFunctionCall
- `SaveLayoutPreset()` - PyFunctionCall
- `UpdateLayoutPreset()` - PyFunctionCall

### Render Preset Management
- `ExportRenderPreset()` - PyFunctionCall
- `ImportRenderPreset()` - PyFunctionCall

### Application Control
- `GetCurrentPage()` - PyFunctionCall
- `GetProductName()` - PyFunctionCall
- `GetVersion()` - PyFunctionCall
- `GetVersionString()` - PyFunctionCall
- `OpenPage()` - PyFunctionCall
- `Quit()` - PyFunctionCall
- `SetHighPriority()` - PyFunctionCall

### Project Access
- `GetProjectManager()` - PyFunctionCall

### Keyframe and Settings
- `GetKeyframeMode()` - PyFunctionCall
- `SetKeyframeMode()` - PyFunctionCall

### Utility
- `Fusion()` - PyFunctionCall
- `Print()` - PyFunctionCall

---

## ProjectManager Object (29 methods)

### Project Operations
- `CreateProject()` - PyFunctionCall
- `LoadProject()` - PyFunctionCall
- `SaveProject()` - PyFunctionCall
- `CloseProject()` - PyFunctionCall
- `DeleteProject()` - PyFunctionCall

### Cloud Project Operations
- `CreateCloudProject()` - PyFunctionCall
- `ImportCloudProject()` - PyFunctionCall
- `LoadCloudProject()` - PyFunctionCall
- `RestoreCloudProject()` - PyFunctionCall

### Project Management
- `ArchiveProject()` - PyFunctionCall
- `ExportProject()` - PyFunctionCall
- `ImportProject()` - PyFunctionCall
- `RestoreProject()` - PyFunctionCall

### Folder Operations
- `CreateFolder()` - PyFunctionCall
- `DeleteFolder()` - PyFunctionCall
- `OpenFolder()` - PyFunctionCall
- `GotoParentFolder()` - PyFunctionCall
- `GotoRootFolder()` - PyFunctionCall

### Database Operations
- `GetCurrentDatabase()` - PyFunctionCall
- `SetCurrentDatabase()` - PyFunctionCall
- `GetDatabaseList()` - PyFunctionCall

### Project Discovery
- `GetProjectListInCurrentFolder()` - PyFunctionCall
- `GetProjectsInCurrentFolder()` - PyFunctionCall
- `GetProjectLastModifiedTime()` - PyFunctionCall

### Utility
- `Print()` - PyFunctionCall

---

## Project Object (46 methods)

### Timeline Management
- `GetCurrentTimeline()` - PyFunctionCall
- `SetCurrentTimeline()` - PyFunctionCall
- `GetTimelineByIndex()` - PyFunctionCall
- `GetTimelineCount()` - PyFunctionCall

### Render Operations
- `StartRendering()` - PyFunctionCall
- `StopRendering()` - PyFunctionCall
- `IsRenderingInProgress()` - PyFunctionCall
- `GetRenderJobList()` - PyFunctionCall
- `GetRenderJobs()` - PyFunctionCall
- `GetRenderJobStatus()` - PyFunctionCall
- `AddRenderJob()` - PyFunctionCall
- `DeleteRenderJob()` - PyFunctionCall
- `DeleteAllRenderJobs()` - PyFunctionCall

### Render Settings
- `GetRenderFormats()` - PyFunctionCall
- `GetRenderCodecs()` - PyFunctionCall
- `GetRenderResolutions()` - PyFunctionCall
- `GetCurrentRenderFormatAndCodec()` - PyFunctionCall
- `SetCurrentRenderFormatAndCodec()` - PyFunctionCall
- `GetCurrentRenderMode()` - PyFunctionCall
- `SetCurrentRenderMode()` - PyFunctionCall
- `SetRenderSettings()` - PyFunctionCall

### Render Presets
- `GetRenderPresetList()` - PyFunctionCall
- `GetRenderPresets()` - PyFunctionCall
- `LoadRenderPreset()` - PyFunctionCall
- `SaveAsNewRenderPreset()` - PyFunctionCall
- `DeleteRenderPreset()` - PyFunctionCall
- `GetPresetList()` - PyFunctionCall
- `GetPresets()` - PyFunctionCall
- `SetPreset()` - PyFunctionCall
- `GetQuickExportRenderPresets()` - PyFunctionCall
- `RenderWithQuickExport()` - PyFunctionCall

### Color Management
- `GetColorGroupsList()` - PyFunctionCall
- `AddColorGroup()` - PyFunctionCall
- `DeleteColorGroup()` - PyFunctionCall

### Media Operations
- `GetMediaPool()` - PyFunctionCall
- `GetGallery()` - PyFunctionCall

### Project Settings
- `GetSetting()` - PyFunctionCall
- `SetSetting()` - PyFunctionCall
- `GetName()` - PyFunctionCall
- `SetName()` - PyFunctionCall
- `GetUniqueId()` - PyFunctionCall

### Utility
- `Print()` - PyFunctionCall
- `RefreshLUTList()` - PyFunctionCall
- `LoadBurnInPreset()` - PyFunctionCall

### Frame Operations
- `ExportCurrentFrameAsStill()` - PyFunctionCall
- `InsertAudioToCurrentTrackAtPlayhead()` - PyFunctionCall

---

## Timeline Object (58 methods)

### Timeline Operations
- `GetName()` - PyFunctionCall
- `SetName()` - PyFunctionCall
- `DuplicateTimeline()` - PyFunctionCall
- `GetStartFrame()` - PyFunctionCall
- `GetEndFrame()` - PyFunctionCall
- `GetUniqueId()` - PyFunctionCall

### Track Management
- `GetTrackCount()` - PyFunctionCall
- `GetTrackName()` - PyFunctionCall
- `SetTrackName()` - PyFunctionCall
- `GetTrackSubType()` - PyFunctionCall
- `AddTrack()` - PyFunctionCall
- `DeleteTrack()` - PyFunctionCall

### Track Control
- `GetIsTrackEnabled()` - PyFunctionCall
- `SetTrackEnable()` - PyFunctionCall
- `GetIsTrackLocked()` - PyFunctionCall
- `SetTrackLock()` - PyFunctionCall

### Item Operations
- `GetItemsInTrack()` - PyFunctionCall
- `GetItemListInTrack()` - PyFunctionCall
- `GetCurrentVideoItem()` - PyFunctionCall
- `GetMediaPoolItem()` - PyFunctionCall

### Playback Control
- `GetCurrentTimecode()` - PyFunctionCall
- `SetCurrentTimecode()` - PyFunctionCall
- `GetStartTimecode()` - PyFunctionCall
- `SetStartTimecode()` - PyFunctionCall

### Markers
- `AddMarker()` - PyFunctionCall
- `GetMarkers()` - PyFunctionCall
- `DeleteMarkerAtFrame()` - PyFunctionCall
- `DeleteMarkerByCustomData()` - PyFunctionCall
- `DeleteMarkersByColor()` - PyFunctionCall
- `GetMarkerByCustomData()` - PyFunctionCall
- `GetMarkerCustomData()` - PyFunctionCall
- `UpdateMarkerCustomData()` - PyFunctionCall

### Timeline Settings
- `GetSetting()` - PyFunctionCall
- `SetSetting()` - PyFunctionCall

### Analysis Operations
- `AnalyzeDolbyVision()` - PyFunctionCall
- `DetectSceneCuts()` - PyFunctionCall

### Utility
- `Print()` - PyFunctionCall
- `ClearMarkInOut()` - PyFunctionCall
- `GetMarkInOut()` - PyFunctionCall
- `SetMarkInOut()` - PyFunctionCall

### Node Graph Access
- `GetNodeGraph()` - PyFunctionCall

### Still Operations
- `GrabStill()` - PyFunctionCall
- `GrabAllStills()` - PyFunctionCall
- `GetCurrentClipThumbnailImage()` - PyFunctionCall

### Import/Export
- `Export()` - PyFunctionCall
- `ImportIntoTimeline()` - PyFunctionCall

### Stereo Operations
- `ConvertTimelineToStereo()` - PyFunctionCall

### Compound Clip Operations
- `CreateCompoundClip()` - PyFunctionCall

### Fusion Operations
- `CreateFusionClip()` - PyFunctionCall
- `InsertFusionCompositionIntoTimeline()` - PyFunctionCall
- `InsertFusionGeneratorIntoTimeline()` - PyFunctionCall
- `InsertFusionTitleIntoTimeline()` - PyFunctionCall

### Generator Operations
- `InsertGeneratorIntoTimeline()` - PyFunctionCall
- `InsertOFXGeneratorIntoTimeline()` - PyFunctionCall
- `InsertTitleIntoTimeline()` - PyFunctionCall

### Subtitle Operations
- `CreateSubtitlesFromAudio()` - PyFunctionCall

### Clip Operations
- `DeleteClips()` - PyFunctionCall
- `SetClipsLinked()` - PyFunctionCall

---

## TimelineItem/VideoItem Object (84 methods)

### Basic Properties
- `GetName()` - PyFunctionCall
- `GetStart()` - PyFunctionCall
- `GetEnd()` - PyFunctionCall
- `GetDuration()` - PyFunctionCall
- `GetUniqueId()` - PyFunctionCall

### Position and Offset
- `GetLeftOffset()` - PyFunctionCall
- `GetRightOffset()` - PyFunctionCall
- `GetSourceStartFrame()` - PyFunctionCall
- `GetSourceEndFrame()` - PyFunctionCall
- `GetSourceStartTime()` - PyFunctionCall
- `GetSourceEndTime()` - PyFunctionCall

### Media Operations
- `GetMediaPoolItem()` - PyFunctionCall
- `GetProperty()` - PyFunctionCall
- `SetProperty()` - PyFunctionCall

### Color Operations
- `GetNodeGraph()` - PyFunctionCall
- `GetLUT()` - PyFunctionCall
- `SetLUT()` - PyFunctionCall
- `SetCDL()` - PyFunctionCall
- `CopyGrades()` - PyFunctionCall

### Markers and Flags
- `AddMarker()` - PyFunctionCall
- `GetMarkers()` - PyFunctionCall
- `DeleteMarkerAtFrame()` - PyFunctionCall
- `DeleteMarkerByCustomData()` - PyFunctionCall
- `DeleteMarkersByColor()` - PyFunctionCall
- `GetMarkerByCustomData()` - PyFunctionCall
- `GetMarkerCustomData()` - PyFunctionCall
- `UpdateMarkerCustomData()` - PyFunctionCall
- `AddFlag()` - PyFunctionCall
- `GetFlagList()` - PyFunctionCall
- `GetFlags()` - PyFunctionCall
- `ClearFlags()` - PyFunctionCall

### Color Group Operations
- `AssignToColorGroup()` - PyFunctionCall
- `GetColorGroup()` - PyFunctionCall
- `RemoveFromColorGroup()` - PyFunctionCall

### Clip Properties
- `GetClipColor()` - PyFunctionCall
- `SetClipColor()` - PyFunctionCall
- `ClearClipColor()` - PyFunctionCall
- `GetClipEnabled()` - PyFunctionCall
- `SetClipEnabled()` - PyFunctionCall

### Version and Takes
- `AddVersion()` - PyFunctionCall
- `GetVersionNameList()` - PyFunctionCall
- `GetVersionNames()` - PyFunctionCall
- `GetCurrentVersion()` - PyFunctionCall
- `LoadVersionByName()` - PyFunctionCall
- `DeleteVersionByName()` - PyFunctionCall
- `RenameVersionByName()` - PyFunctionCall
- `AddTake()` - PyFunctionCall
- `GetTakesCount()` - PyFunctionCall
- `GetTakeByIndex()` - PyFunctionCall
- `GetSelectedTakeIndex()` - PyFunctionCall
- `SelectTakeByIndex()` - PyFunctionCall
- `DeleteTakeByIndex()` - PyFunctionCall
- `FinalizeTake()` - PyFunctionCall

### Fusion Composition
- `AddFusionComp()` - PyFunctionCall
- `GetFusionCompByIndex()` - PyFunctionCall
- `GetFusionCompByName()` - PyFunctionCall
- `GetFusionCompNameList()` - PyFunctionCall
- `GetFusionCompNames()` - PyFunctionCall
- `GetFusionCompCount()` - PyFunctionCall
- `LoadFusionCompByName()` - PyFunctionCall
- `DeleteFusionCompByName()` - PyFunctionCall
- `RenameFusionCompByName()` - PyFunctionCall
- `ExportFusionComp()` - PyFunctionCall
- `ImportFusionComp()` - PyFunctionCall

### Track Information
- `GetTrackTypeAndIndex()` - PyFunctionCall

### Linked Items
- `GetLinkedItems()` - PyFunctionCall

### Cache Operations
- `GetIsColorOutputCacheEnabled()` - PyFunctionCall
- `SetColorOutputCache()` - PyFunctionCall
- `GetIsFusionOutputCacheEnabled()` - PyFunctionCall
- `SetFusionOutputCache()` - PyFunctionCall

### Effects
- `Stabilize()` - PyFunctionCall
- `SmartReframe()` - PyFunctionCall
- `CreateMagicMask()` - PyFunctionCall
- `RegenerateMagicMask()` - PyFunctionCall

### Audio Operations
- `GetSourceAudioChannelMapping()` - PyFunctionCall

### Stereo Operations
- `GetStereoConvergenceValues()` - PyFunctionCall
- `GetStereoLeftFloatingWindowParams()` - PyFunctionCall
- `GetStereoRightFloatingWindowParams()` - PyFunctionCall

### Utility
- `Print()` - PyFunctionCall
- `LoadBurnInPreset()` - PyFunctionCall
- `ExportLUT()` - PyFunctionCall
- `UpdateSidecar()` - PyFunctionCall

### Node Operations
- `GetNumNodes()` - PyFunctionCall
- `GetNodeLabel()` - PyFunctionCall

---

## Node Graph Object (12 methods)

### Grade Operations
- `GetNumNodes()` - PyFunctionCall
- `GetNodeLabel()` - PyFunctionCall
- `SetNodeLabel()` - PyFunctionCall
- `SetNodeEnabled()` - PyFunctionCall

### LUT Operations
- `GetLUT()` - PyFunctionCall
- `SetLUT()` - PyFunctionCall
- `ApplyArriCdlLut()` - PyFunctionCall

### Grade Management
- `ApplyGradeFromDRX()` - PyFunctionCall
- `ResetAllGrades()` - PyFunctionCall

### Caching
- `GetNodeCacheMode()` - PyFunctionCall
- `SetNodeCacheMode()` - PyFunctionCall

### Tools
- `GetToolsInNode()` - PyFunctionCall

### Utility
- `Print()` - PyFunctionCall

---

## Summary

**Total API Methods**: 252
- Resolve: 23 methods
- ProjectManager: 29 methods
- Project: 46 methods
- Timeline: 58 methods
- TimelineItem/VideoItem: 84 methods
- Node Graph: 12 methods

## Key Notes

- **Node Graph Access**: Use `GetNodeGraph()` method (not `GetCurrentGrade()` which doesn't exist)
- **Color Operations**: All color grading operations are accessed through the Node Graph object
- **Project Structure**: Navigate from Resolve → ProjectManager → Project → Timeline → TimelineItem → NodeGraph

This reference provides the complete API surface for DaVinci Resolve scripting, useful for developing MCP servers, automation scripts, and integrations.

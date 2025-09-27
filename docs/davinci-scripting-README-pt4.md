Auto Caption Settings
----------------------
This section covers the supported settings for the method Timeline.CreateSubtitlesFromAudio({autoCaptionSettings})

The parameter setting is a dictionary containing the following keys:
* resolve.SUBTITLE_LANGUAGE: languageID (see below), [resolve.AUTO_CAPTION_AUTO by default]
* resolve.SUBTITLE_CAPTION_PRESET: presetType (see below), [resolve.AUTO_CAPTION_SUBTITLE_DEFAULT by default]
* resolve.SUBTITLE_CHARS_PER_LINE: Number between 1 and 60 inclusive [42 by default]
* resolve.SUBTITLE_LINE_BREAK: lineBreakType (see below), [resolve.AUTO_CAPTION_LINE_SINGLE by default]
* resolve.SUBTITLE_GAP: Number between 0 and 10 inclusive [0 by default]

Note that the default values for some keys may change based on values defined for other keys, as per the UI.
For example, if the following dictionary is supplied,
    { resolve.SUBTITLE_LANGUAGE = resolve.AUTO_CAPTION_KOREAN,
      resolve.SUBTITLE_CAPTION_PRESET = resolve.AUTO_CAPTION_NETFLIX }
the default value for resolve.SUBTITLE_CHARS_PER_LINE will be 16 instead of 42

languageIDs:
* resolve.AUTO_CAPTION_AUTO
* resolve.AUTO_CAPTION_DANISH
* resolve.AUTO_CAPTION_DUTCH
* resolve.AUTO_CAPTION_ENGLISH
* resolve.AUTO_CAPTION_FRENCH
* resolve.AUTO_CAPTION_GERMAN
* resolve.AUTO_CAPTION_ITALIAN
* resolve.AUTO_CAPTION_JAPANESE
* resolve.AUTO_CAPTION_KOREAN
* resolve.AUTO_CAPTION_MANDARIN_SIMPLIFIED
* resolve.AUTO_CAPTION_MANDARIN_TRADITIONAL
* resolve.AUTO_CAPTION_NORWEGIAN
* resolve.AUTO_CAPTION_PORTUGUESE
* resolve.AUTO_CAPTION_RUSSIAN
* resolve.AUTO_CAPTION_SPANISH
* resolve.AUTO_CAPTION_SWEDISH

presetTypes:
* resolve.AUTO_CAPTION_SUBTITLE_DEFAULT
* resolve.AUTO_CAPTION_TELETEXT
* resolve.AUTO_CAPTION_NETFLIX

lineBreakTypes:
* resolve.AUTO_CAPTION_LINE_SINGLE
* resolve.AUTO_CAPTION_LINE_DOUBLE

Looking up Render Settings
--------------------------
This section covers the supported settings for the method SetRenderSettings({settings})

The parameter setting is a dictionary containing the following keys:
    - "SelectAllFrames": Bool (when set True, the settings MarkIn and MarkOut are ignored)
    - "MarkIn": int
    - "MarkOut": int
    - "TargetDir": string
    - "CustomName": string
    - "UniqueFilenameStyle": 0 - Prefix, 1 - Suffix.
    - "ExportVideo": Bool
    - "ExportAudio": Bool
    - "FormatWidth": int
    - "FormatHeight": int
    - "FrameRate": float (examples: 23.976, 24)
    - "PixelAspectRatio": string (for SD resolution: "16_9" or "4_3") (other resolutions: "square" or "cinemascope")
    - "VideoQuality" possible values for current codec (if applicable):
    -    0 (int) - will set quality to automatic
    -    [1 -> MAX] (int) - will set input bit rate
    -    ["Least", "Low", "Medium", "High", "Best"] (String) - will set input quality level
    - "AudioCodec": string (example: "aac")
    - "AudioBitDepth": int
    - "AudioSampleRate": int
    - "ColorSpaceTag" : string (example: "Same as Project", "AstroDesign")
    - "GammaTag" : string (example: "Same as Project", "ACEScct")
    - "ExportAlpha": Bool
    - "EncodingProfile": string (example: "Main10"). Can only be set for H.264 and H.265.
    - "MultiPassEncode": Bool. Can only be set for H.264.
    - "AlphaMode": 0 - Premultiplied, 1 - Straight. Can only be set if "ExportAlpha" is true.
    - "NetworkOptimization": Bool. Only supported by QuickTime and MP4 formats.
    - "ClipStartFrame": int
    - "TimelineStartTimecode": string (example: "01:00:00:00")
    - "ReplaceExistingFilesInPlace": Bool

Looking up timeline export properties
-------------------------------------
This section covers the parameters for the argument Export(fileName, exportType, exportSubtype).

exportType can be one of the following constants:
    - resolve.EXPORT_AAF
    - resolve.EXPORT_DRT
    - resolve.EXPORT_EDL
    - resolve.EXPORT_FCP_7_XML
    - resolve.EXPORT_FCPXML_1_8
    - resolve.EXPORT_FCPXML_1_9
    - resolve.EXPORT_FCPXML_1_10
    - resolve.EXPORT_HDR_10_PROFILE_A
    - resolve.EXPORT_HDR_10_PROFILE_B
    - resolve.EXPORT_TEXT_CSV
    - resolve.EXPORT_TEXT_TAB
    - resolve.EXPORT_DOLBY_VISION_VER_2_9
    - resolve.EXPORT_DOLBY_VISION_VER_4_0
    - resolve.EXPORT_DOLBY_VISION_VER_5_1
    - resolve.EXPORT_OTIO
    - resolve.EXPORT_ALE
    - resolve.EXPORT_ALE_CDL
exportSubtype can be one of the following enums:
    - resolve.EXPORT_NONE
    - resolve.EXPORT_AAF_NEW
    - resolve.EXPORT_AAF_EXISTING
    - resolve.EXPORT_CDL
    - resolve.EXPORT_SDL
    - resolve.EXPORT_MISSING_CLIPS
Please note that exportSubType is a required parameter for resolve.EXPORT_AAF and resolve.EXPORT_EDL. For rest of the exportType, exportSubtype is ignored.
When exportType is resolve.EXPORT_AAF, valid exportSubtype values are resolve.EXPORT_AAF_NEW and resolve.EXPORT_AAF_EXISTING.
When exportType is resolve.EXPORT_EDL, valid exportSubtype values are resolve.EXPORT_CDL, resolve.EXPORT_SDL, resolve.EXPORT_MISSING_CLIPS and resolve.EXPORT_NONE.
Note: Replace 'resolve.' when using the constants above, if a different Resolve class instance name is used.

Unsupported exportType types
---------------------------------
Starting with DaVinci Resolve 18.1, the following export types are not supported:
    - resolve.EXPORT_FCPXML_1_3
    - resolve.EXPORT_FCPXML_1_4
    - resolve.EXPORT_FCPXML_1_5
    - resolve.EXPORT_FCPXML_1_6
    - resolve.EXPORT_FCPXML_1_7


Looking up Timeline item properties
-----------------------------------
This section covers additional notes for the function "TimelineItem:SetProperty" and "TimelineItem:GetProperty". These functions are used to get and set properties mentioned.

The supported keys with their accepted values are:
  "Pan" : floating point values from -4.0*width to 4.0*width
  "Tilt" : floating point values from -4.0*height to 4.0*height
  "ZoomX" : floating point values from 0.0 to 100.0
  "ZoomY" : floating point values from 0.0 to 100.0
  "ZoomGang" : a boolean value
  "RotationAngle" : floating point values from -360.0 to 360.0
  "AnchorPointX" : floating point values from -4.0*width to 4.0*width
  "AnchorPointY" : floating point values from -4.0*height to 4.0*height
  "Pitch" : floating point values from -1.5 to 1.5
  "Yaw" : floating point values from -1.5 to 1.5
  "FlipX" : boolean value for flipping horizontally
  "FlipY" : boolean value for flipping vertically
  "CropLeft" : floating point values from 0.0 to width
  "CropRight" : floating point values from 0.0 to width
  "CropTop" : floating point values from 0.0 to height
  "CropBottom" : floating point values from 0.0 to height
  "CropSoftness" : floating point values from -100.0 to 100.0
  "CropRetain" : boolean value for "Retain Image Position" checkbox
  "DynamicZoomEase" : A value from the following constants
     - DYNAMIC_ZOOM_EASE_LINEAR = 0
     - DYNAMIC_ZOOM_EASE_IN
     - DYNAMIC_ZOOM_EASE_OUT
     - DYNAMIC_ZOOM_EASE_IN_AND_OUT
  "CompositeMode" : A value from the following constants
     - COMPOSITE_NORMAL = 0
     - COMPOSITE_ADD
     - COMPOSITE_SUBTRACT
     - COMPOSITE_DIFF
     - COMPOSITE_MULTIPLY
     - COMPOSITE_SCREEN
     - COMPOSITE_OVERLAY
     - COMPOSITE_HARDLIGHT
     - COMPOSITE_SOFTLIGHT
     - COMPOSITE_DARKEN
     - COMPOSITE_LIGHTEN
     - COMPOSITE_COLOR_DODGE
     - COMPOSITE_COLOR_BURN
     - COMPOSITE_EXCLUSION
     - COMPOSITE_HUE
     - COMPOSITE_SATURATE
     - COMPOSITE_COLORIZE
     - COMPOSITE_LUMA_MASK
     - COMPOSITE_DIVIDE
     - COMPOSITE_LINEAR_DODGE
     - COMPOSITE_LINEAR_BURN
     - COMPOSITE_LINEAR_LIGHT
     - COMPOSITE_VIVID_LIGHT
     - COMPOSITE_PIN_LIGHT
     - COMPOSITE_HARD_MIX
     - COMPOSITE_LIGHTER_COLOR
     - COMPOSITE_DARKER_COLOR
     - COMPOSITE_FOREGROUND
     - COMPOSITE_ALPHA
     - COMPOSITE_INVERTED_ALPHA
     - COMPOSITE_LUM
     - COMPOSITE_INVERTED_LUM
  "Opacity" : floating point value from 0.0 to 100.0
  "Distortion" : floating point value from -1.0 to 1.0
  "RetimeProcess" : A value from the following constants
     - RETIME_USE_PROJECT = 0
     - RETIME_NEAREST
     - RETIME_FRAME_BLEND
     - RETIME_OPTICAL_FLOW
  "MotionEstimation" : A value from the following constants
     - MOTION_EST_USE_PROJECT = 0
     - MOTION_EST_STANDARD_FASTER
     - MOTION_EST_STANDARD_BETTER
     - MOTION_EST_ENHANCED_FASTER
     - MOTION_EST_ENHANCED_BETTER
     - MOTION_EST_SPEED_WARP_BETTER
     - MOTION_EST_SPEED_WARP_FASTER
  "Scaling" : A value from the following constants
     - SCALE_USE_PROJECT = 0
     - SCALE_CROP
     - SCALE_FIT
     - SCALE_FILL
     - SCALE_STRETCH
  "ResizeFilter" : A value from the following constants
     - RESIZE_FILTER_USE_PROJECT = 0
     - RESIZE_FILTER_SHARPER
     - RESIZE_FILTER_SMOOTHER
     - RESIZE_FILTER_BICUBIC
     - RESIZE_FILTER_BILINEAR
     - RESIZE_FILTER_BESSEL
     - RESIZE_FILTER_BOX
     - RESIZE_FILTER_CATMULL_ROM
     - RESIZE_FILTER_CUBIC
     - RESIZE_FILTER_GAUSSIAN
     - RESIZE_FILTER_LANCZOS
     - RESIZE_FILTER_MITCHELL
     - RESIZE_FILTER_NEAREST_NEIGHBOR
     - RESIZE_FILTER_QUADRATIC
     - RESIZE_FILTER_SINC
     - RESIZE_FILTER_LINEAR
Values beyond the range will be clipped
width and height are same as the UI max limits

The arguments can be passed as a key and value pair or they can be grouped together into a dictionary (for python) or table (for lua) and passed
as a single argument.

Getting the values for the keys that uses constants will return the number which is in the constant

ExportLUT notes
---------------
The following section covers additional notes for TimelineItem.ExportLUT(exportType, path).

Supported values for 'exportType' (enum) are:
    - resolve.EXPORT_LUT_17PTCUBE
    - resolve.EXPORT_LUT_33PTCUBE
    - resolve.EXPORT_LUT_65PTCUBE
    - resolve.EXPORT_LUT_PANASONICVLUT

Deprecated Resolve API Functions
--------------------------------
The following API functions are deprecated.

ProjectManager
  GetProjectsInCurrentFolder()                    --> {project names...} # Returns a dict of project names in current folder.
  GetFoldersInCurrentFolder()                     --> {folder names...}  # Returns a dict of folder names in current folder.

Project
  GetPresets()                                    --> {presets...}       # Returns a dict of presets and their information.
  GetRenderJobs()                                 --> {render jobs...}   # Returns a dict of render jobs and their information.
  GetRenderPresets()                              --> {presets...}       # Returns a dict of render presets and their information.

MediaStorage
  GetMountedVolumes()                             --> {paths...}         # Returns a dict of folder paths corresponding to mounted volumes displayed in Resolve’s Media Storage.
  GetSubFolders(folderPath)                       --> {paths...}         # Returns a dict of folder paths in the given absolute folder path.
  GetFiles(folderPath)                            --> {paths...}         # Returns a dict of media and file listings in the given absolute folder path. Note that media listings may be logically consolidated entries.
  AddItemsToMediaPool(item1, item2, ...)          --> {clips...}         # Adds specified file/folder paths from Media Storage into current Media Pool folder. Input is one or more file/folder paths. Returns a dict of the MediaPoolItems created.
  AddItemsToMediaPool([items...])                 --> {clips...}         # Adds specified file/folder paths from Media Storage into current Media Pool folder. Input is an array of file/folder paths. Returns a dict of the MediaPoolItems created.

Folder
  GetClips()                                      --> {clips...}         # Returns a dict of clips (items) within the folder.
  GetSubFolders()                                 --> {folders...}       # Returns a dict of subfolders in the folder.

MediaPoolItem
  GetFlags()                                      --> {colors...}        # Returns a dict of flag colors assigned to the item.

Timeline
  GetItemsInTrack(trackType, index)               --> {items...}         # Returns a dict of Timeline items on the video or audio track (based on trackType) at specified

TimelineItem
  GetFusionCompNames()                            --> {names...}         # Returns a dict of Fusion composition names associated with the timeline item.
  GetFlags()                                      --> {colors...}        # Returns a dict of flag colors assigned to the item.
  GetVersionNames(versionType)                    --> {names...}         # Returns a dict of version names by provided versionType: 0 - local, 1 - remote.
  GetNumNodes()                                   --> int                # Returns the number of nodes in the current graph for the timeline item
  SetLUT(nodeIndex, lutPath)                      --> Bool               # Sets LUT on the node mapping the node index provided, 1 <= nodeIndex <= total number of nodes.
                                                                         # The lutPath can be an absolute path, or a relative path (based off custom LUT paths or the master LUT path).
                                                                         # The operation is successful for valid lut paths that Resolve has already discovered (see Project.RefreshLUTList).
  GetLUT(nodeIndex)                               --> String             # Gets relative LUT path based on the node index provided, 1 <= nodeIndex <= total number of nodes.
  GetNodeLabel(nodeIndex)                         --> string             # Returns the label of the node at nodeIndex.

Unsupported Resolve API Functions
---------------------------------
The following API (functions and parameters) are no longer supported. Use job IDs instead of indices.

Project
  StartRendering(index1, index2, ...)             --> Bool               # Please use unique job ids (string) instead of indices.
  StartRendering([idxs...])                       --> Bool               # Please use unique job ids (string) instead of indices.
  DeleteRenderJobByIndex(idx)                     --> Bool               # Please use unique job ids (string) instead of indices.
  GetRenderJobStatus(idx)                         --> {status info}      # Please use unique job ids (string) instead of indices.
  GetSetting and SetSetting                       --> {}                 # settingName videoMonitorUseRec601For422SDI is now replaced with videoMonitorUseMatrixOverrideFor422SDI and videoMonitorMatrixOverrideFor422SDI.
                                                                         # settingName perfProxyMediaOn is now replaced with perfProxyMediaMode which takes values 0 - disabled, 1 - when available, 2 - when source not available.

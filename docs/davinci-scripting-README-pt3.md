GalleryStillAlbum
  GetStills()                                     --> [galleryStill]     # Returns the list of GalleryStill objects in the album.
  GetLabel(galleryStill)                          --> string             # Returns the label of the galleryStill.
  SetLabel(galleryStill, label)                   --> Bool               # Sets the new 'label' to GalleryStill object 'galleryStill'.
  ImportStills([filePaths])                       --> Bool               # Imports GalleryStill from each filePath in [filePaths] list. True if at least one still is imported successfully. False otherwise.
  ExportStills([galleryStill], folderPath, filePrefix, format) --> Bool  # Exports list of GalleryStill objects '[galleryStill]' to directory 'folderPath', with filename prefix 'filePrefix', using file format 'format' (supported formats: dpx, cin, tif, jpg, png, ppm, bmp, xpm, drx).
  DeleteStills([galleryStill])                    --> Bool               # Deletes specified list of GalleryStill objects '[galleryStill]'.

GalleryStill                                                             # This class does not provide any API functions but the object type is used by functions in other classes.

Graph
  GetNumNodes()                                   --> int                # Returns the number of nodes in the graph
  SetLUT(nodeIndex, lutPath)                      --> Bool               # Sets LUT on the node mapping the node index provided, 1 <= nodeIndex <= self.GetNumNodes().
                                                                         # The lutPath can be an absolute path, or a relative path (based off custom LUT paths or the master LUT path).
                                                                         # The operation is successful for valid lut paths that Resolve has already discovered (see Project.RefreshLUTList).
  GetLUT(nodeIndex)                               --> String             # Gets relative LUT path based on the node index provided, 1 <= nodeIndex <= total number of nodes.
  SetNodeCacheMode(nodeIndex, cache_value)        --> Bool               # Sets the cache mode type on the node mapping the node index provided. Refer to "Cache Mode" section below to find the possible values of cache_value.
  GetNodeCacheMode(nodeIndex)                     --> cache_value        # Returns the cache mode type on the node mapping the node index provided.
  GetNodeLabel(nodeIndex)                         --> string             # Returns the label of the node at nodeIndex.
  GetToolsInNode(nodeIndex)                       --> [toolsList]        # Returns toolsList (list of strings) of the tools used in the node indicated by given nodeIndex (int).
  SetNodeEnabled(nodeIndex, isEnabled)            --> Bool               # Sets the node at the given nodeIndex (int) to isEnabled (bool).
                                                                         # 1 <= nodeIndex <= self.GetNumNodes().
  ApplyGradeFromDRX(path, gradeMode)              --> Bool               # Loads a still from given file path (string) and applies grade to graph with gradeMode (int): 0 - “No keyframes”, 1 - “Source Timecode aligned”, 2 - “Start Frames aligned”.
  ApplyArriCdlLut()                               --> Bool               # Applies ARRI CDL and LUT. Returns True if successful, False otherwise.
  ResetAllGrades()                                --> Bool               # Returns True if all grades were reset successfully, False otherwise.

ColorGroup
  GetName()                                       --> String             # Returns the name (string) of the ColorGroup.
  SetName(groupName)                              --> Bool               # Renames ColorGroup to groupName (string).
  GetClipsInTimeline(Timeline=CurrTimeline)       --> [TimelineItem]     # Returns a list of TimelineItem that are in colorGroup in the given Timeline. Timeline is Current Timeline by default.
  GetPreClipNodeGraph()                           --> Graph              # Returns the ColorGroup Pre-clip graph.
  GetPostClipNodeGraph()                          --> Graph              # Returns the ColorGroup Post-clip graph.

List and Dict Data Structures
-----------------------------
Beside primitive data types, Resolve's Python API mainly uses list and dict data structures. Lists are denoted by [ ... ] and dicts are denoted by { ... } above.
As Lua does not support list and dict data structures, the Lua API implements "list" as a table with indices, e.g. { [1] = listValue1, [2] = listValue2, ... }.
Similarly the Lua API implements "dict" as a table with the dictionary key as first element, e.g. { [dictKey1] = dictValue1, [dictKey2] = dictValue2, ... }.

Keyframe Mode information
-------------------------
This section covers additional notes for the functions Resolve.GetKeyframeMode() and Resolve.SetKeyframeMode(keyframeMode).

'keyframeMode' can be one of the following enums:
    - resolve.KEYFRAME_MODE_ALL     == 0
    - resolve.KEYFRAME_MODE_COLOR   == 1
    - resolve.KEYFRAME_MODE_SIZING  == 2

Integer values returned by Resolve.GetKeyframeMode() will correspond to the enums above.

Cache Mode information
-------------------------
This section covers additional notes for the functions Graph:GetNodeCacheMode(nodeIndex) and Graph:SetNodeCacheMode(nodeIndex, cache_value).

cache_value is an enumerated integer with one of the following values:
    - resolve.CACHE_AUTO_ENABLED  = -1
    - resolve.CACHE_DISABLED      =  0
    - resolve.CACHE_ENABLED       =  1

Integer values returned by Graph:GetNodeCacheMode(nodeIndex) will correspond to the enums above.

Cloud Projects Settings
--------------------------------------
This section covers additional notes for the functions "ProjectManager:LoadCloudProject", "ProjectManager:CreateCloudProject", "ProjectManager:ImportCloudProject", and "ProjectManager:RestoreCloudProject"

All four functions "ProjectManager:CreateCloudProject", "ProjectManager:LoadCloudProject", "ProjectManager:ImportCloudProject", and "ProjectManager:RestoreCloudProject" take in a {cloudSettings} dict, that have the following keys:
* resolve.CLOUD_SETTING_PROJECT_NAME: String, ["" by default]
* resolve.CLOUD_SETTING_PROJECT_MEDIA_PATH: String, ["" by default]
* resolve.CLOUD_SETTING_IS_COLLAB: Bool, [False by default]
* resolve.CLOUD_SETTING_SYNC_MODE: syncMode (see below), [resolve.CLOUD_SYNC_PROXY_ONLY by default]
* resolve.CLOUD_SETTING_IS_CAMERA_ACCESS: Bool [False by default]

Note that "ProjectManager:LoadCloudProject" only honour the following keys: resolve.CLOUD_SETTING_PROJECT_NAME, resolve.CLOUD_SETTING_PROJECT_MEDIA_PATH and resolve.CLOUD_SETTING_SYNC_MODE.
Only 1st load on a given system will honour all 3 settings. Subsequent loads will honour only resolve.CLOUD_SETTING_PROJECT_NAME

Where syncMode is one of the following values:
* resolve.CLOUD_SYNC_NONE,
* resolve.CLOUD_SYNC_PROXY_ONLY,
* resolve.CLOUD_SYNC_PROXY_AND_ORIG

All four functions "ProjectManager:CreateCloudProject", "ProjectManager:LoadCloudProject", "ProjectManager:ImportCloudProject", and "ProjectManager:RestoreCloudProject" require resolve.PROJECT_MEDIA_PATH to be defined.
"ProjectManager:LoadCloudProject" and "ProjectManager:CreateCloudProject" also requires resolve.PROJECT_NAME to be defined.

Audio Sync Settings
---------------------
This section covers additional notes for the functions "MediaPool:AutoSyncAudio".

AutoSyncAudio takes in a {audioSyncSettings} dict, that has the following keys:
* resolve.AUDIO_SYNC_MODE:                  audioSyncMode (see below),  [resolve.AUDIO_SYNC_TIMECODE by default]
* resolve.AUDIO_SYNC_CHANNEL_NUMBER:        channelNumber (see below)   [1 by default]
* resolve.AUDIO_SYNC_RETAIN_EMBEDDED_AUDIO: Bool,                       [False by default]
* resolve.AUDIO_SYNC_RETAIN_VIDEO_METADATA: Bool,                       [False by default]

audioSyncMode can be one of the following:
* resolve.AUDIO_SYNC_WAVEFORM
* resolve.AUDIO_SYNC_TIMECODE

With AUDIO_SYNC_WAVEFORM mode, channelNumber is used to determine channel offset for comparison.
channelNumber can be one of the following:
* resolve.AUDIO_SYNC_CHANNEL_AUTOMATIC    = -1
* resolve.AUDIO_SYNC_CHANNEL_MIX          = -2
* an actual channel offset from input media for waveform comparison. 1 <= channel offset <= channelMax, where channelMax is the channel count of the audio clip in [MediaPoolItems] with the fewest channels.

Looking up Project and Clip properties
--------------------------------------
This section covers additional notes for the functions "Project:GetSetting", "Project:SetSetting", "Timeline:GetSetting", "Timeline:SetSetting", "MediaPoolItem:GetClipProperty" and
"MediaPoolItem:SetClipProperty". These functions are used to get and set properties otherwise available to the user through the Project Settings and the Clip Attributes dialogs.

The functions follow a key-value pair format, where each property is identified by a key (the settingName or propertyName parameter) and possesses a value (typically a text value). Keys and values are
designed to be easily correlated with parameter names and values in the Resolve UI. Explicitly enumerated values for some parameters are listed below.

Some properties may be read only - these include intrinsic clip properties like date created or sample rate, and properties that can be disabled in specific application contexts (e.g. custom colorspaces
in an ACES workflow, or output sizing parameters when behavior is set to match timeline)

Getting values:
Invoke "Project:GetSetting", "Timeline:GetSetting" or "MediaPoolItem:GetClipProperty" with the appropriate property key. To get a snapshot of all queryable properties (keys and values), you can call
"Project:GetSetting", "Timeline:GetSetting" or "MediaPoolItem:GetClipProperty" without parameters (or with a NoneType or a blank property key). Using specific keys to query individual properties will
be faster. Note that getting a property using an invalid key will return a trivial result.

Setting values:
Invoke "Project:SetSetting", "Timeline:SetSetting" or "MediaPoolItem:SetClipProperty" with the appropriate property key and a valid value. When setting a parameter, please check the return value to
ensure the success of the operation. You can troubleshoot the validity of keys and values by setting the desired result from the UI and checking property snapshots before and after the change.

The following Project properties have specifically enumerated values:
"superScale" - the property value is an enumerated integer between 0 and 4 with these meanings: 0=Auto, 1=no scaling, and 2, 3 and 4 represent the Super Scale multipliers 2x, 3x and 4x.
               for super scale multiplier '2x Enhanced', exactly 4 arguments must be passed as outlined below. If less than 4 arguments are passed, it will default to 2x.
Affects:
• x = Project:GetSetting('superScale') and Project:SetSetting('superScale', x)
• for '2x Enhanced' --> Project:SetSetting('superScale', 2, sharpnessValue, noiseReductionValue), where sharpnessValue is a float in the range [0.0, 1.0] and noiseReductionValue is a float in the range [0.0, 1.0]

"timelineFrameRate" - the property value is one of the frame rates available to the user in project settings under "Timeline frame rate" option. Drop Frame can be configured for supported frame rates
                      by appending the frame rate with "DF", e.g. "29.97 DF" will enable drop frame and "29.97" will disable drop frame
Affects:
• x = Project:GetSetting('timelineFrameRate') and Project:SetSetting('timelineFrameRate', x)

The following Clip properties have specifically enumerated values:
"Super Scale" - the property value is an enumerated integer between 1 and 4 with these meanings: 1=no scaling, and 2, 3 and 4 represent the Super Scale multipliers 2x, 3x and 4x.
                for super scale multiplier '2x Enhanced', exactly 4 arguments must be passed as outlined below. If less than 4 arguments are passed, it will default to 2x.
Affects:
• x = MediaPoolItem:GetClipProperty('Super Scale') and MediaPoolItem:SetClipProperty('Super Scale', x)
• for '2x Enhanced' --> MediaPoolItem:SetClipProperty('Super Scale', 2, sharpnessValue, noiseReductionValue), where sharpnessValue is a float in the range [0.0, 1.0] and noiseReductionValue is a float in the range [0.0, 1.0]

"Cloud Sync" = the property value is an enumerated integer that will correspond to one of the following enums:
* resolve.CLOUD_SYNC_DEFAULT                == -1
* resolve.CLOUD_SYNC_DOWNLOAD_IN_QUEUE      == 0
* resolve.CLOUD_SYNC_DOWNLOAD_IN_PROGRESS   == 1
* resolve.CLOUD_SYNC_DOWNLOAD_SUCCESS       == 2
* resolve.CLOUD_SYNC_DOWNLOAD_FAIL          == 3
* resolve.CLOUD_SYNC_DOWNLOAD_NOT_FOUND     == 4

* resolve.CLOUD_SYNC_UPLOAD_IN_QUEUE        == 5
* resolve.CLOUD_SYNC_UPLOAD_IN_PROGRESS     == 6
* resolve.CLOUD_SYNC_UPLOAD_SUCCESS         == 7
* resolve.CLOUD_SYNC_UPLOAD_FAIL            == 8
* resolve.CLOUD_SYNC_UPLOAD_NOT_FOUND       == 9

* resolve.CLOUD_SYNC_SUCCESS                == 10

Audio Mapping
---------------
This section covers the output for mpItem.GetAudioMapping() and timelineItem.GetSourceAudioChannelMapping()
Mapping format (json result) is similar for mpItem and timelineItem.

This section will follow an example of an mpItem that has audio from its embedded source, and from two other clips that are linked to it.
The audio clip attributes of this mpItem will show 3 tracks.

Assume that (A) the embedded track is of format/type 'stereo' (2 channels),
            (B) linked clip 1 track is of format/type '7.1' (8 channels),
            (C) linked clip 2 track is '5.1' (6 channels)
and assume that the format/type was not changed further.

mpItem.GetAudioMapping() returns a string of the form:
    {
      "embedded_audio_channels": 2,                 # Total number of embedded channels across all tracks
      "linked_audio": {                             # A list of only linked audio information
        "1": {                                      # Same as (B) above
          "channels": 8,
          "offset": -100,                           # Audio at media offset 0 plays file_start + 100th sample
          "path": FILE_PATH
        },
        "2": {                                      # Same as (C) above
          "channels": 6,
          "offset": 200,                            # Audio at media start plays 200 samples of digital black then file_start + 0th audio sample
          "path": FILE_PATH
        }
      },
      "track_mapping": {                            # Listing of all the tracks. Output here will match what is seen in the audio clip attributes menu on the UI.
        "1": {
          "channel_idx": [1, 3],                    # In this case, channel index '1' corresponds to first channel of (A), channel index '3' will correspond to the first channel of (B)
          "mute": true,                             # Mute 'true' indicates track is muted. Valid value is true/false.
          "type": "Stereo"                          # The length of the 'channel_idx' list will always correspond to the number of channels the format specified in 'type' will allow.
                                                    # In this case, 'Stereo' allows 2 channels and so the length of the 'channel_idx' list is 2.
        },
        "2": {
          "channel_idx": [3, 4, 5, 6, 7, 8, 9, 10], # Channel indices here are following the default for (B)
          "mute": true,
          "type": "7.1"
        },
        "3": {
          "channel_idx": [1, 1, 1, 1, 15, 16],      # The first four channels for this track correspond to the first channel of (A), and the final 2 follow the default for (C)
          "mute": false,
          "type": "5.1"
        }
      }
    }

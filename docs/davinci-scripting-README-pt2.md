Folder
  GetClipList()                                   --> [clips...]         # Returns a list of clips (items) within the folder.
  GetName()                                       --> string             # Returns the media folder name.
  GetSubFolderList()                              --> [folders...]       # Returns a list of subfolders in the folder.
  GetIsFolderStale()                              --> bool               # Returns true if folder is stale in collaboration mode, false otherwise
  GetUniqueId()                                   --> string             # Returns a unique ID for the media pool folder
  Export(filePath)                                --> bool               # Returns true if export of DRB folder to filePath is successful, false otherwise
  TranscribeAudio()                               --> Bool               # Transcribes audio of the MediaPoolItems within the folder and nested folders. Returns True if successful; False otherwise
  ClearTranscription()                            --> Bool               # Clears audio transcription of the MediaPoolItems within the folder and nested folders. Returns True if successful; False otherwise.

MediaPoolItem
  GetName()                                       --> string             # Returns the clip name.
  GetMetadata(metadataType=None)                  --> string|dict        # Returns the metadata value for the key 'metadataType'.
                                                                         # If no argument is specified, a dict of all set metadata properties is returned.
  SetMetadata(metadataType, metadataValue)        --> Bool               # Sets the given metadata to metadataValue (string). Returns True if successful.
  SetMetadata({metadata})                         --> Bool               # Sets the item metadata with specified 'metadata' dict. Returns True if successful.
  GetThirdPartyMetadata(metadataType=None)        --> string|dict        # Returns the third party metadata value for the key 'metadataType'.
                                                                         # If no argument is specified, a dict of all set third party metadata properties is returned.
  SetThirdPartyMetadata(metadataType, metadataValue) --> Bool            # Sets/Add the given third party metadata to metadataValue (string). Returns True if successful.
  SetThirdPartyMetadata({metadata})               --> Bool               # Sets/Add the item third party metadata with specified 'metadata' dict. Returns True if successful.
  GetMediaId()                                    --> string             # Returns the unique ID for the MediaPoolItem.
  AddMarker(frameId, color, name, note, duration, --> Bool               # Creates a new marker at given frameId position and with given marker information. 'customData' is optional and helps to attach user specific data to the marker.
            customData)
  GetMarkers()                                    --> {markers...}       # Returns a dict (frameId -> {information}) of all markers and dicts with their information.
                                                                         # Example of output format: {96.0: {'color': 'Green', 'duration': 1.0, 'note': '', 'name': 'Marker 1', 'customData': ''}, ...}
                                                                         # In the above example - there is one 'Green' marker at offset 96 (position of the marker)
  GetMarkerByCustomData(customData)               --> {markers...}       # Returns marker {information} for the first matching marker with specified customData.
  UpdateMarkerCustomData(frameId, customData)     --> Bool               # Updates customData (string) for the marker at given frameId position. CustomData is not exposed via UI and is useful for scripting developer to attach any user specific data to markers.
  GetMarkerCustomData(frameId)                    --> string             # Returns customData string for the marker at given frameId position.
  DeleteMarkersByColor(color)                     --> Bool               # Delete all markers of the specified color from the media pool item. "All" as argument deletes all color markers.
  DeleteMarkerAtFrame(frameNum)                   --> Bool               # Delete marker at frame number from the media pool item.
  DeleteMarkerByCustomData(customData)            --> Bool               # Delete first matching marker with specified customData.
  AddFlag(color)                                  --> Bool               # Adds a flag with given color (string).
  GetFlagList()                                   --> [colors...]        # Returns a list of flag colors assigned to the item.
  ClearFlags(color)                               --> Bool               # Clears the flag of the given color if one exists. An "All" argument is supported and clears all flags.
  GetClipColor()                                  --> string             # Returns the item color as a string.
  SetClipColor(colorName)                         --> Bool               # Sets the item color based on the colorName (string).
  ClearClipColor()                                --> Bool               # Clears the item color.
  GetClipProperty(propertyName=None)              --> string|dict        # Returns the property value for the key 'propertyName'.
                                                                         # If no argument is specified, a dict of all clip properties is returned. Check the section below for more information.
  SetClipProperty(propertyName, propertyValue)    --> Bool               # Sets the given property to propertyValue (string). Check the section below for more information.
  LinkProxyMedia(proxyMediaFilePath)              --> Bool               # Links proxy media located at path specified by arg 'proxyMediaFilePath' with the current clip. 'proxyMediaFilePath' should be absolute clip path.
  LinkFullResolutionMedia(fullResMediaPath)       --> Bool               # Links proxy media to full resolution media files specified via its path.
  UnlinkProxyMedia()                              --> Bool               # Unlinks any proxy media associated with clip.
  ReplaceClip(filePath)                           --> Bool               # Replaces the underlying asset and metadata of MediaPoolItem with the specified absolute clip path.
  ReplaceClipPreserveSubClip(filePath)            --> Bool               # Replaces the underlying asset and metadata of a video or audio clip with the specified absolute clip path, preserving original sub clip extents.
  GetUniqueId()                                   --> string             # Returns a unique ID for the media pool item
  TranscribeAudio()                               --> Bool               # Transcribes audio of the MediaPoolItem. Returns True if successful; False otherwise
  ClearTranscription()                            --> Bool               # Clears audio transcription of the MediaPoolItem. Returns True if successful; False otherwise.
  GetAudioMapping()                               --> json formatted string # Returns a string with MediaPoolItem's audio mapping information. Check 'Audio Mapping' section below for more information.
  GetMarkInOut()                                  --> {mark}             # Returns dict of in/out marks set (keys omitted if not set), example:
                                                                         # {'video': {'in': 0, 'out': 134}, 'audio': {'in': 0, 'out': 134}}
  SetMarkInOut(in, out, type="all")               --> Bool               # Sets mark in/out of type "video", "audio" or "all" (default).
  ClearMarkInOut(type="all")                      --> Bool               # Clears mark in/out of type "video", "audio" or "all" (default).
  MonitorGrowingFile()                            --> Bool               # Monitor a file as long as it keeps growing (stops if the file does not grow for some time).

Timeline
  GetName()                                       --> string             # Returns the timeline name.
  SetName(timelineName)                           --> Bool               # Sets the timeline name if timelineName (string) is unique. Returns True if successful.
  GetStartFrame()                                 --> int                # Returns the frame number at the start of timeline.
  GetEndFrame()                                   --> int                # Returns the frame number at the end of timeline.
  SetStartTimecode(timecode)                      --> Bool               # Set the start timecode of the timeline to the string 'timecode'. Returns true when the change is successful, false otherwise.
  GetStartTimecode()                              --> string             # Returns the start timecode for the timeline.
  GetTrackCount(trackType)                        --> int                # Returns the number of tracks for the given track type ("audio", "video" or "subtitle").
  AddTrack(trackType, subTrackType)               --> Bool               # Adds track of trackType ("video", "subtitle", "audio"). Optional argument subTrackType is used for "audio" trackType.
                                                                         # subTrackType can be one of {"mono", "stereo", lrc, lcr, lrcs, lcrs, quad, "5.0", "5.0film", "5.1", "5.1film", "7.0", "7.0film" ,"7.1", "7.1film", "adaptive1", ... , "adaptive36"}
                                                                         # subTrackType defaults to 'mono' if skipped and track type is ‘audio’.
  AddTrack(trackType, newTrackOptions)            --> Bool               # Adds track of trackType ("video", "subtitle", "audio"). Optional newTrackOptions = {'audioType': same as subTrackType above, 'index': 1 <= index <= GetTrackCount(trackType))
                                                                         # 'audiotype' defaults to 'mono' if arg skipped and track type is ‘audio’.
                                                                         # 'index' if skipped (or if value not in bounds) appends track.
  DeleteTrack(trackType, trackIndex)              --> Bool               # Deletes track of trackType ("video", "subtitle", "audio") and given trackIndex. 1 <= trackIndex <= GetTrackCount(trackType).
  GetTrackSubType(trackType, trackIndex)          --> string             # Returns an audio track's format.
                                                                         # the return value is one of {"mono", "stereo", lrc, lcr, lrcs, lcrs, quad, "5.0", "5.0film", "5.1", "5.1film", "7.0", "7.0film" ,"7.1", "7.1film", "adaptive1", ... , "adaptive36"}
                                                                         # and matches the parameters 'subTrackType' and 'audioType' in timeline.AddTrack.
                                                                         # returns a blank string for non audio tracks

  SetTrackEnable(trackType, trackIndex, Bool)     --> Bool               # Enables/Disables track with given trackType and trackIndex
                                                                         # trackType is one of {"audio", "video", "subtitle"}
                                                                         # 1 <= trackIndex <= GetTrackCount(trackType).
  GetIsTrackEnabled(trackType, trackIndex)        --> Bool               # Returns True if track with given trackType and trackIndex is enabled and False otherwise.
                                                                         # trackType is one of {"audio", "video", "subtitle"}
                                                                         # 1 <= trackIndex <= GetTrackCount(trackType).
  SetTrackLock(trackType, trackIndex, Bool)       --> Bool               # Locks/Unlocks track with given trackType and trackIndex
                                                                         # trackType is one of {"audio", "video", "subtitle"}
                                                                         # 1 <= trackIndex <= GetTrackCount(trackType).
  GetIsTrackLocked(trackType, trackIndex)         --> Bool               # Returns True if track with given trackType and trackIndex is locked and False otherwise.
                                                                         # trackType is one of {"audio", "video", "subtitle"}
                                                                         # 1 <= trackIndex <= GetTrackCount(trackType).
  DeleteClips([timelineItems], Bool)              --> Bool               # Deletes specified TimelineItems from the timeline, performing ripple delete if the second argument is True. Second argument is optional (The default for this is False)
  SetClipsLinked([timelineItems], Bool)           --> Bool               # Links or unlinks the specified TimelineItems depending on second argument.
  GetItemListInTrack(trackType, index)            --> [items...]         # Returns a list of timeline items on that track (based on trackType and index). 1 <= index <= GetTrackCount(trackType).
  AddMarker(frameId, color, name, note, duration, --> Bool               # Creates a new marker at given frameId position and with given marker information. 'customData' is optional and helps to attach user specific data to the marker.
            customData)
  GetMarkers()                                    --> {markers...}       # Returns a dict (frameId -> {information}) of all markers and dicts with their information.
                                                                         # Example: a value of {96.0: {'color': 'Green', 'duration': 1.0, 'note': '', 'name': 'Marker 1', 'customData': ''}, ...} indicates a single green marker at timeline offset 96
  GetMarkerByCustomData(customData)               --> {markers...}       # Returns marker {information} for the first matching marker with specified customData.
  UpdateMarkerCustomData(frameId, customData)     --> Bool               # Updates customData (string) for the marker at given frameId position. CustomData is not exposed via UI and is useful for scripting developer to attach any user specific data to markers.
  GetMarkerCustomData(frameId)                    --> string             # Returns customData string for the marker at given frameId position.
  DeleteMarkersByColor(color)                     --> Bool               # Deletes all timeline markers of the specified color. An "All" argument is supported and deletes all timeline markers.
  DeleteMarkerAtFrame(frameNum)                   --> Bool               # Deletes the timeline marker at the given frame number.
  DeleteMarkerByCustomData(customData)            --> Bool               # Delete first matching marker with specified customData.
  GetCurrentTimecode()                            --> string             # Returns a string timecode representation for the current playhead position, while on Cut, Edit, Color, Fairlight and Deliver pages.
  SetCurrentTimecode(timecode)                    --> Bool               # Sets current playhead position from input timecode for Cut, Edit, Color, Fairlight and Deliver pages.
  GetCurrentVideoItem()                           --> item               # Returns the current video timeline item.
  GetCurrentClipThumbnailImage()                  --> {thumbnailData}    # Returns a dict (keys "width", "height", "format" and "data") with data containing raw thumbnail image data (RGB 8-bit image data encoded in base64 format) for current media in the Color Page.
                                                                         # An example of how to retrieve and interpret thumbnails is provided in 6_get_current_media_thumbnail.py in the Examples folder.
  GetTrackName(trackType, trackIndex)             --> string             # Returns the track name for track indicated by trackType ("audio", "video" or "subtitle") and index. 1 <= trackIndex <= GetTrackCount(trackType).
  SetTrackName(trackType, trackIndex, name)       --> Bool               # Sets the track name (string) for track indicated by trackType ("audio", "video" or "subtitle") and index. 1 <= trackIndex <= GetTrackCount(trackType).
  DuplicateTimeline(timelineName)                 --> timeline           # Duplicates the timeline and returns the created timeline, with the (optional) timelineName, on success.
  CreateCompoundClip([timelineItems], {clipInfo}) --> timelineItem       # Creates a compound clip of input timeline items with an optional clipInfo map: {"startTimecode" : "00:00:00:00", "name" : "Compound Clip 1"}. It returns the created timeline item.
  CreateFusionClip([timelineItems])               --> timelineItem       # Creates a Fusion clip of input timeline items. It returns the created timeline item.
  ImportIntoTimeline(filePath, {importOptions})   --> Bool               # Imports timeline items from an AAF file and optional importOptions dict into the timeline, with support for the keys:
                                                                         # "autoImportSourceClipsIntoMediaPool": Bool, specifies if source clips should be imported into media pool, True by default
                                                                         # "ignoreFileExtensionsWhenMatching": Bool, specifies if file extensions should be ignored when matching, False by default
                                                                         # "linkToSourceCameraFiles": Bool, specifies if link to source camera files should be enabled, False by default
                                                                         # "useSizingInfo": Bool, specifies if sizing information should be used, False by default
                                                                         # "importMultiChannelAudioTracksAsLinkedGroups": Bool, specifies if multi-channel audio tracks should be imported as linked groups, False by default
                                                                         # "insertAdditionalTracks": Bool, specifies if additional tracks should be inserted, True by default
                                                                         # "insertWithOffset": string, specifies insert with offset value in timecode format - defaults to "00:00:00:00", applicable if "insertAdditionalTracks" is False
                                                                         # "sourceClipsPath": string, specifies a filesystem path to search for source clips if the media is inaccessible in their original path and if "ignoreFileExtensionsWhenMatching" is True
                                                                         # "sourceClipsFolders": string, list of Media Pool folder objects to search for source clips if the media is not present in current folder

  Export(fileName, exportType, exportSubtype)     --> Bool               # Exports timeline to 'fileName' as per input exportType & exportSubtype format.
                                                                         # Refer to section "Looking up timeline export properties" for information on the parameters.
  GetSetting(settingName)                         --> string             # Returns value of timeline setting (indicated by settingName : string). Check the section below for more information.
  SetSetting(settingName, settingValue)           --> Bool               # Sets timeline setting (indicated by settingName : string) to the value (settingValue : string). Check the section below for more information.
  InsertGeneratorIntoTimeline(generatorName)      --> TimelineItem       # Inserts a generator (indicated by generatorName : string) into the timeline.
  InsertFusionGeneratorIntoTimeline(generatorName) --> TimelineItem      # Inserts a Fusion generator (indicated by generatorName : string) into the timeline.
  InsertFusionCompositionIntoTimeline()           --> TimelineItem       # Inserts a Fusion composition into the timeline.
  InsertOFXGeneratorIntoTimeline(generatorName)   --> TimelineItem       # Inserts an OFX generator (indicated by generatorName : string) into the timeline.
  InsertTitleIntoTimeline(titleName)              --> TimelineItem       # Inserts a title (indicated by titleName : string) into the timeline.
  InsertFusionTitleIntoTimeline(titleName)        --> TimelineItem       # Inserts a Fusion title (indicated by titleName : string) into the timeline.
  GrabStill()                                     --> galleryStill       # Grabs still from the current video clip. Returns a GalleryStill object.
  GrabAllStills(stillFrameSource)                 --> [galleryStill]     # Grabs stills from all the clips of the timeline at 'stillFrameSource' (1 - First frame, 2 - Middle frame). Returns the list of GalleryStill objects.
  GetUniqueId()                                   --> string             # Returns a unique ID for the timeline
  CreateSubtitlesFromAudio({autoCaptionSettings}) --> Bool               # Creates subtitles from audio for the timeline.
                                                                         # Takes in optional dictionary {autoCaptionSettings}. Check 'Auto Caption Settings' subsection below for more information.
                                                                         # Returns True on success, False otherwise.
  DetectSceneCuts()                               --> Bool               # Detects and makes scene cuts along the timeline. Returns True if successful, False otherwise.
  ConvertTimelineToStereo()                       --> Bool               # Converts timeline to stereo. Returns True if successful; False otherwise.
  GetNodeGraph()                                  --> Graph              # Returns the timeline's node graph object.
  AnalyzeDolbyVision([timelineItems]=[],          --> Bool               # Analyzes Dolby Vision on clips present on the timeline. Returns True if analysis start is successful; False otherwise.
                     analysisType=NONE)                                  # if [timelineItems] is empty, analysis performed on all items. Else, analysis performed on [timelineItems] only.
                                                                         # set analysisType to resolve.DLB_BLEND_SHOTS for blend setting
  GetMediaPoolItem()                              --> MediaPoolItem      # Returns the media pool item corresponding to the timeline
  GetMarkInOut()                                  --> {mark}             # Returns dict of in/out marks set (keys omitted if not set), example:
                                                                         # {'video': {'in': 0, 'out': 134}, 'audio': {'in': 0, 'out': 134}}
  SetMarkInOut(in, out, type="all")               --> Bool               # Sets mark in/out of type "video", "audio" or "all" (default).
  ClearMarkInOut(type="all")                      --> Bool               # Clears mark in/out of type "video", "audio" or "all" (default).

TimelineItem
  GetName()                                       --> string             # Returns the item name.
  GetDuration(subframe_precision)                 --> int/float          # Returns the item duration. Returns fractional frames if subframe_precision is True
  GetEnd(subframe_precision)                      --> int/float          # Returns the end frame position on the timeline. Returns fractional frames if subframe_precision is True
  GetSourceEndFrame()                             --> int                # Returns the end frame position of the media pool clip in the timeline clip.
  GetSourceEndTime()                              --> float              # Returns the end time position of the media pool clip in the timeline clip.
  GetFusionCompCount()                            --> int                # Returns number of Fusion compositions associated with the timeline item.
  GetFusionCompByIndex(compIndex)                 --> fusionComp         # Returns the Fusion composition object based on given index. 1 <= compIndex <= timelineItem.GetFusionCompCount()
  GetFusionCompNameList()                         --> [names...]         # Returns a list of Fusion composition names associated with the timeline item.
  GetFusionCompByName(compName)                   --> fusionComp         # Returns the Fusion composition object based on given name.
  GetLeftOffset(subframe_precision)               --> int/float          # Returns the maximum extension by frame for clip from left side. Returns fractional frames if subframe_precision is True
  GetRightOffset(subframe_precision)              --> int/float          # Returns the maximum extension by frame for clip from right side. Returns fractional frames if subframe_precision is True
  GetStart(subframe_precision)                    --> int/float          # Returns the start frame position on the timeline. Returns fractional frames if subframe_precision is True
  GetSourceStartFrame()                           --> int                # Returns the start frame position of the media pool clip in the timeline clip.
  GetSourceStartTime()                            --> float              # Returns the start time position of the media pool clip in the timeline clip.
  SetProperty(propertyKey, propertyValue)         --> Bool               # Sets the value of property "propertyKey" to value "propertyValue"
                                                                         # Refer to "Looking up Timeline item properties" for more information
  GetProperty(propertyKey)                        --> int/[key:value]    # returns the value of the specified key
                                                                         # if no key is specified, the method returns a dictionary(python) or table(lua) for all supported keys
  AddMarker(frameId, color, name, note, duration, --> Bool               # Creates a new marker at given frameId position and with given marker information. 'customData' is optional and helps to attach user specific data to the marker.
            customData)
  GetMarkers()                                    --> {markers...}       # Returns a dict (frameId -> {information}) of all markers and dicts with their information.
                                                                         # Example: a value of {96.0: {'color': 'Green', 'duration': 1.0, 'note': '', 'name': 'Marker 1', 'customData': ''}, ...} indicates a single green marker at clip offset 96
  GetMarkerByCustomData(customData)               --> {markers...}       # Returns marker {information} for the first matching marker with specified customData.
  UpdateMarkerCustomData(frameId, customData)     --> Bool               # Updates customData (string) for the marker at given frameId position. CustomData is not exposed via UI and is useful for scripting developer to attach any user specific data to markers.
  GetMarkerCustomData(frameId)                    --> string             # Returns customData string for the marker at given frameId position.
  DeleteMarkersByColor(color)                     --> Bool               # Delete all markers of the specified color from the timeline item. "All" as argument deletes all color markers.
  DeleteMarkerAtFrame(frameNum)                   --> Bool               # Delete marker at frame number from the timeline item.
  DeleteMarkerByCustomData(customData)            --> Bool               # Delete first matching marker with specified customData.
  AddFlag(color)                                  --> Bool               # Adds a flag with given color (string).
  GetFlagList()                                   --> [colors...]        # Returns a list of flag colors assigned to the item.
  ClearFlags(color)                               --> Bool               # Clear flags of the specified color. An "All" argument is supported to clear all flags.
  GetClipColor()                                  --> string             # Returns the item color as a string.
  SetClipColor(colorName)                         --> Bool               # Sets the item color based on the colorName (string).
  ClearClipColor()                                --> Bool               # Clears the item color.
  AddFusionComp()                                 --> fusionComp         # Adds a new Fusion composition associated with the timeline item.
  ImportFusionComp(path)                          --> fusionComp         # Imports a Fusion composition from given file path by creating and adding a new composition for the item.
  ExportFusionComp(path, compIndex)               --> Bool               # Exports the Fusion composition based on given index to the path provided.
  DeleteFusionCompByName(compName)                --> Bool               # Deletes the named Fusion composition.
  LoadFusionCompByName(compName)                  --> fusionComp         # Loads the named Fusion composition as the active composition.
  RenameFusionCompByName(oldName, newName)        --> Bool               # Renames the Fusion composition identified by oldName.
  AddVersion(versionName, versionType)            --> Bool               # Adds a new color version for a video clip based on versionType (0 - local, 1 - remote).
  GetCurrentVersion()                             --> {versionName...}   # Returns the current version of the video clip. The returned value will have the keys versionName and versionType(0 - local, 1 - remote).
  DeleteVersionByName(versionName, versionType)   --> Bool               # Deletes a color version by name and versionType (0 - local, 1 - remote).
  LoadVersionByName(versionName, versionType)     --> Bool               # Loads a named color version as the active version. versionType: 0 - local, 1 - remote.
  RenameVersionByName(oldName, newName, versionType)--> Bool             # Renames the color version identified by oldName and versionType (0 - local, 1 - remote).
  GetVersionNameList(versionType)                 --> [names...]         # Returns a list of all color versions for the given versionType (0 - local, 1 - remote).
  GetMediaPoolItem()                              --> MediaPoolItem      # Returns the media pool item corresponding to the timeline item if one exists.
  GetStereoConvergenceValues()                    --> {keyframes...}     # Returns a dict (offset -> value) of keyframe offsets and respective convergence values.
  GetStereoLeftFloatingWindowParams()             --> {keyframes...}     # For the LEFT eye -> returns a dict (offset -> dict) of keyframe offsets and respective floating window params. Value at particular offset includes the left, right, top and bottom floating window values.
  GetStereoRightFloatingWindowParams()            --> {keyframes...}     # For the RIGHT eye -> returns a dict (offset -> dict) of keyframe offsets and respective floating window params. Value at particular offset includes the left, right, top and bottom floating window values.
  SetCDL([CDL map])                               --> Bool               # Keys of map are: "NodeIndex", "Slope", "Offset", "Power", "Saturation", where 1 <= NodeIndex <= total number of nodes.
                                                                         # Example python code - SetCDL({"NodeIndex" : "1", "Slope" : "0.5 0.4 0.2", "Offset" : "0.4 0.3 0.2", "Power" : "0.6 0.7 0.8", "Saturation" : "0.65"})
  AddTake(mediaPoolItem, startFrame, endFrame)    --> Bool               # Adds mediaPoolItem as a new take. Initializes a take selector for the timeline item if needed. By default, the full clip extents is added. startFrame (int) and endFrame (int) are optional arguments used to specify the extents.
  GetSelectedTakeIndex()                          --> int                # Returns the index of the currently selected take, or 0 if the clip is not a take selector.
  GetTakesCount()                                 --> int                # Returns the number of takes in take selector, or 0 if the clip is not a take selector.
  GetTakeByIndex(idx)                             --> {takeInfo...}      # Returns a dict (keys "startFrame", "endFrame" and "mediaPoolItem") with take info for specified index.
  DeleteTakeByIndex(idx)                          --> Bool               # Deletes a take by index, 1 <= idx <= number of takes.
  SelectTakeByIndex(idx)                          --> Bool               # Selects a take by index, 1 <= idx <= number of takes.
  FinalizeTake()                                  --> Bool               # Finalizes take selection.
  CopyGrades([tgtTimelineItems])                  --> Bool               # Copies the current node stack layer grade to the same layer for each item in tgtTimelineItems. Returns True if successful.
  SetClipEnabled(Bool)                            --> Bool               # Sets clip enabled based on argument.
  GetClipEnabled()                                --> Bool               # Gets clip enabled status.
  UpdateSidecar()                                 --> Bool               # Updates sidecar file for BRAW clips or RMD file for R3D clips.
  GetUniqueId()                                   --> string             # Returns a unique ID for the timeline item
  LoadBurnInPreset(presetName)                    --> Bool               # Loads user defined data burn in preset for clip when supplied presetName (string). Returns true if successful.
  CreateMagicMask(mode)                           --> Bool               # Returns True if magic mask was created successfully, False otherwise. mode can "F" (forward), "B" (backward), or "BI" (bidirection)
  RegenerateMagicMask()                           --> Bool               # Returns True if magic mask was regenerated successfully, False otherwise.
  Stabilize()                                     --> Bool               # Returns True if stabilization was successful, False otherwise
  SmartReframe()                                  --> Bool               # Performs Smart Reframe. Returns True if successful, False otherwise.
  GetNodeGraph(layerIdx)                          --> Graph              # Returns the clip's node graph object at layerIdx (int, optional). Returns the first layer if layerIdx is skipped. 1 <= layerIdx <= project.GetSetting("nodeStackLayers").
  GetColorGroup()                                 --> ColorGroup         # Returns the clip's color group if one exists.
  AssignToColorGroup(ColorGroup)                  --> Bool               # Returns True if TiItem to successfully assigned to given ColorGroup. ColorGroup must be an existing group in the current project.
  RemoveFromColorGroup()                          --> Bool               # Returns True if the TiItem is successfully removed from the ColorGroup it is in.
  ExportLUT(exportType, path)                     --> Bool               # Exports LUTs from tiItem referring to value passed in 'exportType' (enum) for LUT size. Refer to. 'ExportLUT notes' section for possible values.
                                                                         # Saves generated LUT in the provided 'path' (string). 'path' should include the intended file name.
                                                                         # If an empty or incorrect extension is provided, the appropriate extension (.cube/.vlt) will be appended at the end of the path.
  GetLinkedItems()                                --> [TimelineItems]    # Returns a list of linked timeline items.
  GetTrackTypeAndIndex()                          --> [trackType, trackIndex] # Returns a list of two values that correspond to the TimelineItem's trackType (string) and trackIndex (int) respectively.
                                                                           # trackType is one of {"audio", "video", "subtitle"}
                                                                           # 1 <= trackIndex <= Timeline.GetTrackCount(trackType)
  GetSourceAudioChannelMapping()                 --> json formatted string # Returns a string with TimelineItem's audio mapping information. Check 'Audio Mapping' section below for more information.
  GetIsColorOutputCacheEnabled()                  --> cache_value        # Returns if the cache corresponding to cache_type is enabled
  GetIsFusionOutputCacheEnabled()                 --> cache_value        # Returns if the cache corresponding to cache_type is enabled (or auto)
  SetColorOutputCache(cache_value)                --> Bool               # Sets caching to enabled or disabled. Equivalent to clip context menu action 'Render Cache Color Output'.
  SetFusionOutputCache(cache_value)               --> Bool               # Sets caching to auto, enabled or disabled. Equivalent to clip context menu action 'Render Cache Fusion Output'.

Gallery
  GetAlbumName(galleryStillAlbum)                 --> string              # Returns the name of the GalleryStillAlbum object 'galleryStillAlbum'.
  SetAlbumName(galleryStillAlbum, albumName)      --> Bool                # Sets the name of the GalleryStillAlbum object 'galleryStillAlbum' to 'albumName'.
  GetCurrentStillAlbum()                          --> galleryStillAlbum   # Returns current album as a GalleryStillAlbum object.
  SetCurrentStillAlbum(galleryStillAlbum)         --> Bool                # Sets current album to GalleryStillAlbum object 'galleryStillAlbum'.
  GetGalleryStillAlbums()                         --> [galleryStillAlbum] # Returns the gallery Still albums as a list of GalleryStillAlbum objects.
  GetGalleryPowerGradeAlbums()                    --> [galleryStillAlbum] # Returns the gallery PowerGrade albums as a list of GalleryStillAlbum objects.
  CreateGalleryStillAlbum()                       --> galleryStillAlbum   # Returns a newly created Still album (GalleryStillAlbum object), or None if not successful.
  CreateGalleryPowerGradeAlbum()                  --> galleryStillAlbum   # Returns a newly created PowerGrade album (GalleryStillAlbum object), or None if not successful.
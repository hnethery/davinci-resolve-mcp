Last Updated: 7 May 2025
------------------------
In this package, you will find a brief introduction to the Scripting API for DaVinci Resolve Studio. Apart from this README.txt file, this package contains folders containing the basic import
modules for scripting access (DaVinciResolve.py) and some representative examples.

From v16.2.0 onwards, the nodeIndex parameters accepted by SetLUT() and SetCDL() are 1-based instead of 0-based, i.e. 1 <= nodeIndex <= total number of nodes.

Overview
--------
As with Blackmagic Fusion scripts, user scripts written in Lua and Python programming languages are supported. By default, scripts can be invoked from the Console window in the Fusion page,
or via command line. This permission can be changed in Resolve Preferences, to be only from Console, or to be invoked from the local network. Please be aware of the security implications when
allowing scripting access from outside of the Resolve application.

Prerequisites
-------------
DaVinci Resolve scripting requires one of the following to be installed (for all users):

    Lua 5.1
    Python >= 3.6 64-bit
    Python 2.7 64-bit

Using a script
--------------
DaVinci Resolve needs to be running for a script to be invoked.

For a Resolve script to be executed from an external folder, the script needs to know of the API location.
You may need to set the these environment variables to allow for your Python installation to pick up the appropriate dependencies as shown below:

    Mac OS X:
    RESOLVE_SCRIPT_API="/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting"
    RESOLVE_SCRIPT_LIB="/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/Libraries/Fusion/fusionscript.so"
    PYTHONPATH="$PYTHONPATH:$RESOLVE_SCRIPT_API/Modules/"

    Windows:
    RESOLVE_SCRIPT_API="%PROGRAMDATA%\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting"
    RESOLVE_SCRIPT_LIB="C:\Program Files\Blackmagic Design\DaVinci Resolve\fusionscript.dll"
    PYTHONPATH="%PYTHONPATH%;%RESOLVE_SCRIPT_API%\Modules\"

    Linux:
    RESOLVE_SCRIPT_API="/opt/resolve/Developer/Scripting"
    RESOLVE_SCRIPT_LIB="/opt/resolve/libs/Fusion/fusionscript.so"
    PYTHONPATH="$PYTHONPATH:$RESOLVE_SCRIPT_API/Modules/"
    (Note: For standard ISO Linux installations, the path above may need to be modified to refer to /home/resolve instead of /opt/resolve)

As with Fusion scripts, Resolve scripts can also be invoked via the menu and the Console.

On startup, DaVinci Resolve scans the subfolders in the directories shown below and enumerates the scripts found in the Workspace application menu under Scripts.
Place your script under Utility to be listed in all pages, under Comp or Tool to be available in the Fusion page or under folders for individual pages (Edit, Color or Deliver). Scripts under Deliver are additionally listed under render jobs.
Placing your script here and invoking it from the menu is the easiest way to use scripts.
    Mac OS X:
      - All users: /Library/Application Support/Blackmagic Design/DaVinci Resolve/Fusion/Scripts
      - Specific user:  /Users/<UserName>/Library/Application Support/Blackmagic Design/DaVinci Resolve/Fusion/Scripts
    Windows:
      - All users: %PROGRAMDATA%\Blackmagic Design\DaVinci Resolve\Fusion\Scripts
      - Specific user: %APPDATA%\Roaming\Blackmagic Design\DaVinci Resolve\Support\Fusion\Scripts
    Linux:
      - All users: /opt/resolve/Fusion/Scripts  (or /home/resolve/Fusion/Scripts/ depending on installation)
      - Specific user: $HOME/.local/share/DaVinciResolve/Fusion/Scripts

The interactive Console window allows for an easy way to execute simple scripting commands, to query or modify properties, and to test scripts. The console accepts commands in Python 2.7, Python 3.6
and Lua and evaluates and executes them immediately. For more information on how to use the Console, please refer to the DaVinci Resolve User Manual.

This example Python script creates a simple project:

    #!/usr/bin/env python
    import DaVinciResolveScript as dvr_script
    resolve = dvr_script.scriptapp("Resolve")
    fusion = resolve.Fusion()
    projectManager = resolve.GetProjectManager()
    projectManager.CreateProject("Hello World")

The resolve object is the fundamental starting point for scripting via Resolve. As a native object, it can be inspected for further scriptable properties - using table iteration and "getmetatable"
in Lua and dir, help etc in Python (among other methods). A notable scriptable object above is fusion - it allows access to all existing Fusion scripting functionality.


Running DaVinci Resolve in headless mode
----------------------------------------
DaVinci Resolve can be launched in a headless mode without the user interface using the -nogui command line option. When DaVinci Resolve is launched using this option, the user interface is disabled.
However, the various scripting APIs will continue to work as expected.

DaVinci Resolve API
-------------------
Some commonly used API functions are described below (*). As with the resolve object, each object is inspectable for properties and functions.

Resolve
  Fusion()                                        --> Fusion             # Returns the Fusion object. Starting point for Fusion scripts.
  GetMediaStorage()                               --> MediaStorage       # Returns the media storage object to query and act on media locations.
  GetProjectManager()                             --> ProjectManager     # Returns the project manager object for currently open database.
  OpenPage(pageName)                              --> Bool               # Switches to indicated page in DaVinci Resolve. Input can be one of ("media", "cut", "edit", "fusion", "color", "fairlight", "deliver").
  GetCurrentPage()                                --> String             # Returns the page currently displayed in the main window. Returned value can be one of ("media", "cut", "edit", "fusion", "color", "fairlight", "deliver", None).
  GetProductName()                                --> string             # Returns product name.
  GetVersion()                                    --> [version fields]   # Returns list of product version fields in [major, minor, patch, build, suffix] format.
  GetVersionString()                              --> string             # Returns product version in "major.minor.patch[suffix].build" format.
  LoadLayoutPreset(presetName)                    --> Bool               # Loads UI layout from saved preset named 'presetName'.
  UpdateLayoutPreset(presetName)                  --> Bool               # Overwrites preset named 'presetName' with current UI layout.
  ExportLayoutPreset(presetName, presetFilePath)  --> Bool               # Exports preset named 'presetName' to path 'presetFilePath'.
  DeleteLayoutPreset(presetName)                  --> Bool               # Deletes preset named 'presetName'.
  SaveLayoutPreset(presetName)                    --> Bool               # Saves current UI layout as a preset named 'presetName'.
  ImportLayoutPreset(presetFilePath, presetName)  --> Bool               # Imports preset from path 'presetFilePath'. The optional argument 'presetName' specifies how the preset shall be named. If not specified, the preset is named based on the filename.
  Quit()                                          --> None               # Quits the Resolve App.
  ImportRenderPreset(presetPath)                  --> Bool               # Import a preset from presetPath (string) and set it as current preset for rendering.
  ExportRenderPreset(presetName, exportPath)      --> Bool               # Export a preset to a given path (string) if presetName(string) exists.
  ImportBurnInPreset(presetPath)                  --> Bool               # Import a data burn in preset from a given presetPath (string)
  ExportBurnInPreset(presetName, exportPath)      --> Bool               # Export a data burn in preset to a given path (string) if presetName (string) exists.
  GetKeyframeMode()                               --> keyframeMode       # Returns the currently set keyframe mode (int). Refer to section 'Keyframe Mode information' below for details.
  SetKeyframeMode(keyframeMode)                   --> Bool               # Returns True when 'keyframeMode'(enum) is successfully set. Refer to section 'Keyframe Mode information' below for details.

ProjectManager
  ArchiveProject(projectName,
                 filePath,
                 isArchiveSrcMedia=True,
                 isArchiveRenderCache=True,
                 isArchiveProxyMedia=False)       --> Bool               # Archives project to provided file path with the configuration as provided by the optional arguments
  CreateProject(projectName)                      --> Project            # Creates and returns a project if projectName (string) is unique, and None if it is not.
  DeleteProject(projectName)                      --> Bool               # Delete project in the current folder if not currently loaded
  LoadProject(projectName)                        --> Project            # Loads and returns the project with name = projectName (string) if there is a match found, and None if there is no matching Project.
  GetCurrentProject()                             --> Project            # Returns the currently loaded Resolve project.
  SaveProject()                                   --> Bool               # Saves the currently loaded project with its own name. Returns True if successful.
  CloseProject(project)                           --> Bool               # Closes the specified project without saving.
  CreateFolder(folderName)                        --> Bool               # Creates a folder if folderName (string) is unique.
  DeleteFolder(folderName)                        --> Bool               # Deletes the specified folder if it exists. Returns True in case of success.
  GetProjectListInCurrentFolder()                 --> [project names...] # Returns a list of project names in current folder.
  GetFolderListInCurrentFolder()                  --> [folder names...]  # Returns a list of folder names in current folder.
  GotoRootFolder()                                --> Bool               # Opens root folder in database.
  GotoParentFolder()                              --> Bool               # Opens parent folder of current folder in database if current folder has parent.
  GetCurrentFolder()                              --> string             # Returns the current folder name.
  OpenFolder(folderName)                          --> Bool               # Opens folder under given name.
  ImportProject(filePath, projectName=None)       --> Bool               # Imports a project from the file path provided with given project name, if any. Returns True if successful.
  ExportProject(projectName, filePath, withStillsAndLUTs=True) --> Bool  # Exports project to provided file path, including stills and LUTs if withStillsAndLUTs is True (enabled by default). Returns True in case of success.
  RestoreProject(filePath, projectName=None)      --> Bool               # Restores a project from the file path provided with given project name, if any. Returns True if successful.
  GetCurrentDatabase()                            --> {dbInfo}           # Returns a dictionary (with keys 'DbType', 'DbName' and optional 'IpAddress') corresponding to the current database connection
  GetDatabaseList()                               --> [{dbInfo}]         # Returns a list of dictionary items (with keys 'DbType', 'DbName' and optional 'IpAddress') corresponding to all the databases added to Resolve
  SetCurrentDatabase({dbInfo})                    --> Bool               # Switches current database connection to the database specified by the keys below, and closes any open project.
                                                                         # 'DbType': 'Disk' or 'PostgreSQL' (string)
                                                                         # 'DbName': database name (string)
                                                                         # 'IpAddress': IP address of the PostgreSQL server (string, optional key - defaults to '127.0.0.1')
  CreateCloudProject({cloudSettings})             --> Project            # Creates and returns a cloud project.
                                                                         # '{cloudSettings}': Check 'Cloud Projects Settings' subsection below for more information.
  LoadCloudProject({cloudSettings})               --> Project            # Loads and returns a cloud project with the following cloud settings if there is a match found, and None if there is no matching cloud project.
                                                                         # '{cloudSettings}': Check 'Cloud Projects Settings' subsection below for more information.
  ImportCloudProject(filePath, {cloudSettings})   --> Bool               # Returns True if import cloud project is successful; False otherwise
                                                                         # 'filePath': String; filePath of file to import
                                                                         # '{cloudSettings}': Check 'Cloud Projects Settings' subsection below for more information.
  RestoreCloudProject(folderPath, {cloudSettings}) --> Bool              # Returns True if restore cloud project is successful; False otherwise
                                                                         # 'folderPath': String; path of folder to restore
                                                                         # '{cloudSettings}': Check 'Cloud Projects Settings' subsection below for more information.

Project
  GetMediaPool()                                  --> MediaPool          # Returns the Media Pool object.
  GetTimelineCount()                              --> int                # Returns the number of timelines currently present in the project.
  GetTimelineByIndex(idx)                         --> Timeline           # Returns timeline at the given index, 1 <= idx <= project.GetTimelineCount()
  GetCurrentTimeline()                            --> Timeline           # Returns the currently loaded timeline.
  SetCurrentTimeline(timeline)                    --> Bool               # Sets given timeline as current timeline for the project. Returns True if successful.
  GetGallery()                                    --> Gallery            # Returns the Gallery object.
  GetName()                                       --> string             # Returns project name.
  SetName(projectName)                            --> Bool               # Sets project name if given projectName (string) is unique.
  GetPresetList()                                 --> [presets...]       # Returns a list of presets and their information.
  SetPreset(presetName)                           --> Bool               # Sets preset by given presetName (string) into project.
  AddRenderJob()                                  --> string             # Adds a render job based on current render settings to the render queue. Returns a unique job id (string) for the new render job.
  DeleteRenderJob(jobId)                          --> Bool               # Deletes render job for input job id (string).
  DeleteAllRenderJobs()                           --> Bool               # Deletes all render jobs in the queue.
  GetRenderJobList()                              --> [render jobs...]   # Returns a list of render jobs and their information.
  GetRenderPresetList()                           --> [presets...]       # Returns a list of render presets and their information.
  StartRendering(jobId1, jobId2, ...)             --> Bool               # Starts rendering jobs indicated by the input job ids.
  StartRendering([jobIds...], isInteractiveMode=False)    --> Bool       # Starts rendering jobs indicated by the input job ids.
                                                                         # The optional "isInteractiveMode", when set, enables error feedback in the UI during rendering.
  StartRendering(isInteractiveMode=False)                 --> Bool       # Starts rendering all queued render jobs.
                                                                         # The optional "isInteractiveMode", when set, enables error feedback in the UI during rendering.
  StopRendering()                                 --> None               # Stops any current render processes.
  IsRenderingInProgress()                         --> Bool               # Returns True if rendering is in progress.
  LoadRenderPreset(presetName)                    --> Bool               # Sets a preset as current preset for rendering if presetName (string) exists.
  SaveAsNewRenderPreset(presetName)               --> Bool               # Creates new render preset by given name if presetName(string) is unique.
  DeleteRenderPreset(presetName)                  --> Bool               # Delete render preset by provided name.
  SetRenderSettings({settings})                   --> Bool               # Sets given settings for rendering. Settings is a dict, with support for the keys:
                                                                         # Refer to "Looking up render settings" section for information for supported settings
  GetRenderJobStatus(jobId)                       --> {status info}      # Returns a dict with job status and completion percentage of the job by given jobId (string).
  GetQuickExportRenderPresets()                   --> [preset_name..]    # Returns a list of Quick Export render presets by name
  RenderWithQuickExport(preset_name, {param_dict})--> {status info}      # Starts a quick export render for the current active timeline. preset_name from GetQuickExportRenderPresets list. param_dict supports render settings keys "TargetDir", "CustomName", "VideoQuality", and "EnableUpload".
                                                                         # "EnableUpload" key enables direct upload for supported web presets.
                                                                         # Returns a dict with job status and time taken to render, or an error string if render has failed or not attempted
                                                                         # Refer to "Looking up Render Settings" section for information on the above supported settings
  GetSetting(settingName)                         --> string             # Returns value of project setting (indicated by settingName, string). Check the section below for more information.
  SetSetting(settingName, settingValue)           --> Bool               # Sets the project setting (indicated by settingName, string) to the value (settingValue, string). Check the section below for more information.
  GetRenderFormats()                              --> {render formats..} # Returns a dict (format -> file extension) of available render formats.
  GetRenderCodecs(renderFormat)                   --> {render codecs...} # Returns a dict (codec description -> codec name) of available codecs for given render format (string).
  GetCurrentRenderFormatAndCodec()                --> {format, codec}    # Returns a dict with currently selected format 'format' and render codec 'codec'.
  SetCurrentRenderFormatAndCodec(format, codec)   --> Bool               # Sets given render format (string) and render codec (string) as options for rendering.
  GetCurrentRenderMode()                          --> int                # Returns the render mode: 0 - Individual clips, 1 - Single clip.
  SetCurrentRenderMode(renderMode)                --> Bool               # Sets the render mode. Specify renderMode = 0 for Individual clips, 1 for Single clip.
  GetRenderResolutions(format, codec)             --> [{Resolution}]     # Returns list of resolutions applicable for the given render format (string) and render codec (string). Returns full list of resolutions if no argument is provided. Each element in the list is a dictionary with 2 keys "Width" and "Height".
  RefreshLUTList()                                --> Bool               # Refreshes LUT List
  GetUniqueId()                                   --> string             # Returns a unique ID for the project item
  InsertAudioToCurrentTrackAtPlayhead(mediaPath,  --> Bool               # Inserts the media specified by mediaPath (string) with startOffsetInSamples (int) and durationInSamples (int) at the playhead on a selected track on the Fairlight page. Returns True if successful, otherwise False.
          startOffsetInSamples, durationInSamples)
  LoadBurnInPreset(presetName)                    --> Bool               # Loads user defined data burn in preset for project when supplied presetName (string). Returns true if successful.
  ExportCurrentFrameAsStill(filePath)             --> Bool               # Exports current frame as still to supplied filePath. filePath must end in valid export file format. Returns True if successful, False otherwise.
  GetColorGroupsList()                            --> [ColorGroups...]   # Returns a list of all group objects in the timeline.
  AddColorGroup(groupName)                        --> ColorGroup         # Creates a new ColorGroup. groupName must be a unique string.
  DeleteColorGroup(colorGroup)                    --> Bool               # Deletes the given color group and sets clips to ungrouped.

MediaStorage
  GetMountedVolumeList()                          --> [paths...]         # Returns list of folder paths corresponding to mounted volumes displayed in Resolve’s Media Storage.
  GetSubFolderList(folderPath)                    --> [paths...]         # Returns list of folder paths in the given absolute folder path.
  GetFileList(folderPath)                         --> [paths...]         # Returns list of media and file listings in the given absolute folder path. Note that media listings may be logically consolidated entries.
  RevealInStorage(path)                           --> Bool               # Expands and displays given file/folder path in Resolve’s Media Storage.
  AddItemListToMediaPool(item1, item2, ...)       --> [clips...]         # Adds specified file/folder paths from Media Storage into current Media Pool folder. Input is one or more file/folder paths. Returns a list of the MediaPoolItems created.
  AddItemListToMediaPool([items...])              --> [clips...]         # Adds specified file/folder paths from Media Storage into current Media Pool folder. Input is an array of file/folder paths. Returns a list of the MediaPoolItems created.
  AddItemListToMediaPool([{itemInfo}, ...])       --> [clips...]         # Adds list of itemInfos specified as dict of "media", "startFrame" (int), "endFrame" (int) from Media Storage into current Media Pool folder. Returns a list of the MediaPoolItems created.
  AddClipMattesToMediaPool(MediaPoolItem, [paths], stereoEye) --> Bool   # Adds specified media files as mattes for the specified MediaPoolItem. StereoEye is an optional argument for specifying which eye to add the matte to for stereo clips ("left" or "right"). Returns True if successful.
  AddTimelineMattesToMediaPool([paths])           --> [MediaPoolItems]   # Adds specified media files as timeline mattes in current media pool folder. Returns a list of created MediaPoolItems.

MediaPool
  GetRootFolder()                                 --> Folder             # Returns root Folder of Media Pool
  AddSubFolder(folder, name)                      --> Folder             # Adds new subfolder under specified Folder object with the given name.
  RefreshFolders()                                --> Bool               # Updates the folders in collaboration mode
  CreateEmptyTimeline(name)                       --> Timeline           # Adds new timeline with given name.
  AppendToTimeline(clip1, clip2, ...)             --> [TimelineItem]     # Appends specified MediaPoolItem objects in the current timeline. Returns the list of appended timelineItems.
  AppendToTimeline([clips])                       --> [TimelineItem]     # Appends specified MediaPoolItem objects in the current timeline. Returns the list of appended timelineItems.
  AppendToTimeline([{clipInfo}, ...])             --> [TimelineItem]     # Appends list of clipInfos specified as dict of "mediaPoolItem", "startFrame" (float/int), "endFrame" (float/int), (optional) "mediaType" (int; 1 - Video only, 2 - Audio only), "trackIndex" (int) and "recordFrame" (float/int). Returns the list of appended timelineItems.
  CreateTimelineFromClips(name, clip1, clip2,...) --> Timeline           # Creates new timeline with specified name, and appends the specified MediaPoolItem objects.
  CreateTimelineFromClips(name, [clips])          --> Timeline           # Creates new timeline with specified name, and appends the specified MediaPoolItem objects.
  CreateTimelineFromClips(name, [{clipInfo}])     --> Timeline           # Creates new timeline with specified name, appending the list of clipInfos specified as a dict of "mediaPoolItem", "startFrame" (float/int), "endFrame" (float/int), "recordFrame" (float/int).
  ImportTimelineFromFile(filePath, {importOptions}) --> Timeline         # Creates timeline based on parameters within given file (AAF/EDL/XML/FCPXML/DRT/ADL/OTIO) and optional importOptions dict, with support for the keys:
                                                                         # "timelineName": string, specifies the name of the timeline to be created. Not valid for DRT import
                                                                         # "importSourceClips": Bool, specifies whether source clips should be imported, True by default. Not valid for DRT import
                                                                         # "sourceClipsPath": string, specifies a filesystem path to search for source clips if the media is inaccessible in their original path and if "importSourceClips" is True
                                                                         # "sourceClipsFolders": List of Media Pool folder objects to search for source clips if the media is not present in current folder and if "importSourceClips" is False. Not valid for DRT import
                                                                         # "interlaceProcessing": Bool, specifies whether to enable interlace processing on the imported timeline being created. valid only for AAF import
  DeleteTimelines([timeline])                     --> Bool               # Deletes specified timelines in the media pool.
  GetCurrentFolder()                              --> Folder             # Returns currently selected Folder.
  SetCurrentFolder(Folder)                        --> Bool               # Sets current folder by given Folder.
  DeleteClips([clips])                            --> Bool               # Deletes specified clips or timeline mattes in the media pool
  ImportFolderFromFile(filePath, sourceClipsPath="") --> Bool            # Returns true if import from given DRB filePath is successful, false otherwise
                                                                         # sourceClipsPath is a string that specifies a filesystem path to search for source clips if the media is inaccessible in their original path, empty by default
  DeleteFolders([subfolders])                     --> Bool               # Deletes specified subfolders in the media pool
  MoveClips([clips], targetFolder)                --> Bool               # Moves specified clips to target folder.
  MoveFolders([folders], targetFolder)            --> Bool               # Moves specified folders to target folder.
  GetClipMatteList(MediaPoolItem)                 --> [paths]            # Get mattes for specified MediaPoolItem, as a list of paths to the matte files.
  GetTimelineMatteList(Folder)                    --> [MediaPoolItems]   # Get mattes in specified Folder, as list of MediaPoolItems.
  DeleteClipMattes(MediaPoolItem, [paths])        --> Bool               # Delete mattes based on their file paths, for specified MediaPoolItem. Returns True on success.
  RelinkClips([MediaPoolItem], folderPath)        --> Bool               # Update the folder location of specified media pool clips with the specified folder path.
  UnlinkClips([MediaPoolItem])                    --> Bool               # Unlink specified media pool clips.
  ImportMedia([items...])                         --> [MediaPoolItems]   # Imports specified file/folder paths into current Media Pool folder. Input is an array of file/folder paths. Returns a list of the MediaPoolItems created.
  ImportMedia([{clipInfo}])                       --> [MediaPoolItems]   # Imports file path(s) into current Media Pool folder as specified in list of clipInfo dict. Returns a list of the MediaPoolItems created.
                                                                         # Each clipInfo gets imported as one MediaPoolItem unless 'Show Individual Frames' is turned on.
                                                                         # Example: ImportMedia([{"FilePath":"file_%03d.dpx", "StartIndex":1, "EndIndex":100}]) would import clip "file_[001-100].dpx".
  ExportMetadata(fileName, [clips])               --> Bool               # Exports metadata of specified clips to 'fileName' in CSV format.
                                                                         # If no clips are specified, all clips from media pool will be used.
  GetUniqueId()                                   --> string             # Returns a unique ID for the media pool
  CreateStereoClip(LeftMediaPoolItem,
                   RightMediaPoolItem)            --> MediaPoolItem      # Takes in two existing media pool items and creates a new 3D stereoscopic media pool entry replacing the input media in the media pool.
  AutoSyncAudio([MediaPoolItems], {audioSyncSettings}) --> Bool          # Syncs audio for specified [MediaPoolItems] (list). The list must contain a minimum of two MediaPoolItems - at least one video and one audio clip.
                                                                         # Returns True if successful. Refer to 'Audio Sync Settings' section for details.
  GetSelectedClips()                              --> [MediaPoolItems]   # Returns the current selected MediaPoolItems
  SetSelectedClip(MediaPoolItem)                  --> Bool               # Sets the selected MediaPoolItem to the given MediaPoolItem

Function Log(string)
	WScript.Echo string
End Function

Const FOF_SILENT					= &H0004  ' don't display progress UI (confirm prompts may be displayed still)
Const FOF_RENAMEONCOLLISION			= &H0008  ' automatically rename the source files to avoid the collisions
Const FOF_NOCONFIRMATION			= &H0010  ' don't display confirmation UI, assume "yes" for cases that can be bypassed, "no" for those that can not
Const FOF_ALLOWUNDO					= &H0040  ' enable undo including Recycle behavior for IFileOperation::Delete()
Const FOF_FILESONLY					= &H0080  ' only operate on the files (non folders), both files and folders are assumed without this
Const FOF_SIMPLEPROGRESS			= &H0100  ' means don't show names of files
Const FOF_NOCONFIRMMKDIR			= &H0200  ' don't dispplay confirmatino UI before making any needed directories, assume "Yes" in these cases
Const FOF_NOERRORUI					= &H0400  ' don't put up error UI, other UI may be displayed, progress, confirmations
Const FOF_NOCOPYSECURITYATTRIBS		= &H0800  ' dont copy file security attributes (ACLs)
Const FOF_NORECURSION				= &H1000  ' don't recurse into directories for operations that would recurse
Const FOF_NO_CONNECTED_ELEMENTS		= &H2000  ' don't operate on connected elements ("xxx_files" folders that go with .htm files)
Const FOF_WANTNUKEWARNING			= &H4000  ' during delete operation, warn if nuking instead of recycling (partially overrides FOF_NOCONFIRMATION)
'Const FOF_NO_UI						= FOF_SILENT + FOF_NOCONFIRMATION + FOF_NOERRORUI + FOF_NOCONFIRMMKDIR

'Get command-line arguments.
Set objArgs	= WScript.Arguments
inputZip	= objArgs(0)

If objArgs.Count < 2 then
	outFolder = "."
Else
	outFolder = objArgs(1)
End If

' get our FSO object
Log "Get FSO object"
Set objFSO = CreateObject("Scripting.FileSystemObject")

' src zip file is arg 0
Log "Got src zip: "
Log inputZip
Log "Getting src object"
SRC = objFSO.GetAbsolutePathName(inputZip)

' dest folder is arg 1 or "."
Log "Get dest folder (arg 1)"
DEST = objFSO.GetAbsolutePathName(outFolder)

' create dest folder if it does not exist
Log "create dest folder:"
Log DEST

If not objFSO.FolderExists(DEST) Then
	objFSO.CreateFolder(DEST)
	Log "Created new folder:"
	Log DEST
End If

If not Right(SRC, 4) = ".zip" Then
	WScript.Echo "source not a zip file: "
	WScript.Echo SRC
Else
	' get the shell application object used to do the unzip
	Log "Get Shell App"
	Set objShell	= CreateObject("Shell.Application")

	Log "Get objSrc"	
	Set objSrc		= objShell.Namespace(SRC)
	set colItems	= objSrc.Items

	Log "Get objDest"	
	Set objDest		= objShell.Namespace(DEST)
	
	Log "unzipping..."	
	intCount = objDest.Items.Count
	fof_NO_UI = FOF_SILENT + FOF_NOCONFIRMATION + FOF_NOERRORUI + FOF_NOCONFIRMMKDIR
	objDest.CopyHere colItems, fof_NO_UI

	Do Until objDest.Items.Count = intCount + colItems.Count
		WScript.Sleep 200
	Loop
End If

	
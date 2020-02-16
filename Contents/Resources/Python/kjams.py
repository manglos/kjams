# -*- coding: utf-8 -*- 
import kjams_lib, platform, sys, os

#=== platform
def print_paths():
	for file in sys.path:
	    print "%s - %s" % (file, os.path.exists(file))

#=== platform
def is_on_mac():
	return platform.system() == 'Darwin'

def is_on_windows():
	return not is_on_mac()

#=== charcodes
def FourCCToNumber(code):
	return (ord(code[0]) << 24) | (ord(code[1]) << 16) | (ord(code[2]) << 8) | ord(code[3])

def NumberToFourCC(number):
	return chr((number & 0xFF000000) >> 24) + chr((number & 0x00FF0000) >> 16) + chr((number & 0x0000FF00) >> 8) + chr(number & 0x000000FF)

#=== enums
def enum(*sequential, **named):
	enums = dict(zip(sequential, range(len(sequential))), **named)
	enums['reverse_mapping'] = dict((value, key) for key, value in enums.iteritems())
	return type('Enum', (), enums)

def enum_cmds():
	commands = enum(
		'kScriptCommand_NONE', 
		'kScriptCommand_PLAY_PAUSE', 
		'kScriptCommand_STOP', 
		'kScriptCommand_BACK_REWIND', 
		'kScriptCommand_NEXT', 
		'kScriptCommand_VOL_UP', 
		'kScriptCommand_VOL_DOWN', 
		'kScriptCommand_VOL_MUTE', 
		'kScriptCommand_PITCH_UP', 
		'kScriptCommand_PITCH_DOWN', 
		'kScriptCommand_PITCH_NORMAL', 
		'kScriptCommand_SAVE', 
		'kScriptCommand_TEMPO_UP', 
		'kScriptCommand_TEMPO_DOWN', 
		'kScriptCommand_TEMPO_NORMAL', 
		'kScriptCommand_FULL_SCREEN', 
		'kScriptCommand_CAM_POWER', 
		'kScriptCommand_CAM_SHOOT', 
		'kScriptCommand_CRASH', 
		'kScriptCommand_RESCAN_VENUE', 
		'kScriptCommand_SHOW_ROTATION', 
		'kScriptCommand_HIDE_SHOWSCREEN', 
		'kScriptCommand_IS_SHOWSCREEN_SHOWING', 
		'kScriptCommand_GET_SHOW_ROTATION_TIME_REMAIN', 
		'kScriptCommand_TOGGLE_TRANSPARENT', 
		'kScriptCommand_IS_TRANSPARENT', 
		'kScriptCommand_GET_VIDEO_DISPLAY_ID', 
		'kScriptCommand_GET_IND_SONG_ID', 
		'kScriptCommand_Prog_SetCurMax', 
		'kScriptCommand_Prog_SetStr',
		'kScriptCommand_Menu',
		'kScriptCommand_GetPref',
		'kScriptCommand_SetPref', 
		'kScriptCommand_Server', 
		'kScriptCommand_GetMeta',
		'kScriptCommand_SetMeta',
		'kScriptCommand_GetSelectedPlaylist', 
		'kScriptCommand_SetSelectedPlaylist', 
		'kScriptCommand_GetSelection', 
		'kScriptCommand_SetSelection', 
		'kScriptCommandStr_GetAppVersion', 
		'kScriptCommandStr_GetCurSongName',
		'kScriptCommandStr_GetCurSongPath',
		'kScriptCommandStr_GetCurSongCachePath',
		'kScriptCommandStr_GetNextSongName',
		'kScriptCommandStr_GetNextSongPath',
		'kScriptCommandStr_GetNextSongCachePath',
		'kScriptCommand_GET_PLAY_MODE',
		'kScriptCommand_GET_CUR_SONG_TIME',
		'kScriptCommand_ADD_TO_LIBRARY',
		'kScriptCommand_EXPORT',
		'kScriptCommand_GET_PLI_LIST',
		'kScriptCommand_PLI_TO_SONG_ID',
		'kScriptCommand_Unicode_Test',
		'kScriptCommand_3ButtonDialog',
		'kScriptCommand_TextDialog',
		'kScriptCommand_SetKeyShortcut',
		'kScriptCommand_GetVolume',
		'kScriptCommand_SetVolume',
		'kScriptCommand_Is_Exporting',
		'kScriptCommand_Debug_GetNumFonts',
		'kScriptCommand_Create_QR_Code',
		'kScriptCommand_Get_ServerAddress',
		'kScriptCommand_Get_ModDate'	# returns a CFAbsoluteTime
	)
	
	return commands

def enum_server():
	commands = enum(
		'CWS_Path_NONE', 
		'CWS_Path_PING', 
		'CWS_Path_LOGIN', 
		'CWS_Path_LOGOUT', 
		'CWS_Path_MAIN', 
		'CWS_Path_HELP', 
		'CWS_Path_NEW_SINGER', 
		'CWS_Path_SINGERS', 
		'CWS_Path_ROTATION', 
		'CWS_Path_KJ_ROTATION', 
		'CWS_Path_PLAYLISTS', 
		'CWS_Path_SONGS', 
		'CWS_Path_SEARCH', 
		'CWS_Path_DROP', 
		'CWS_Path_REORDER', 
		'CWS_Path_REMOVE', 
		'CWS_Path_PITCH', 
		'CWS_Path_TEMPO', 
		'CWS_Path_SCRIPT_MAIN', 
		'CWS_Path_INFO',
		'CWS_Path_NEW_PLAYLIST')
	return commands
	
def enum_sortby():
	commands = enum(
		'CWS_OrderBy_INDEX', 
		'CWS_OrderBy_NAME', 
		'CWS_OrderBy_ARTIST', 
		'CWS_OrderBy_ALBUM', 
		'CWS_OrderBy_PITCH')
	return commands

def enum_play_modes():
	commands = enum(
		'kPlayModeType_STOPPED', 
		'kPlayModeType_PLAYING', 
		'kPlayModeType_PAUSED')
	return commands

def enum_audio_device():
	commands = enum(
		'kAudioDevice_OUT_MIXED', 
		'kAudioDevice_IN_MIC1') 
	return commands

def enum_button_type():
	commands = enum(
		'kButtonType_NORMAL', 			# key shortcut is first letter of text
		'kButtonType_DEFAULT', 			# pressing return or enter will press this
		'kButtonType_CANCEL', 			# pressing esc or cmd-. will press this
		'kButtonType_DEFAULT_CANCEL')	# both
	return commands

#=======================================================
def do_cmd(cmdID, *args):
	args = (cmdID,) + args
	return kjams_lib.do_command(*args)

#=== volume
def get_volume():
	return do_cmd(enum_cmds().kScriptCommand_GetVolume, enum_audio_device().kAudioDevice_OUT_MIXED)

def set_volume(volS):
	return do_cmd(enum_cmds().kScriptCommand_SetVolume, enum_audio_device().kAudioDevice_OUT_MIXED, volS)

#=== menus
def menu(*args):
	do_cmd(enum_cmds().kScriptCommand_Menu, args)

'''
this would work too
def menu(menu, item, sub1Item = -1, sub2Item = -1, sub3Item = -1, sub4Item = -1):
	itemA = [menu, item, sub1Item, sub2Item, sub3Item, sub4Item]
	do_cmd(enum_cmds().kScriptCommand_Menu, args)
'''

def menu_set_shortcut(str):
	do_cmd(enum_cmds().kScriptCommand_SetKeyShortcut, str)

def menu_clear_shortcut(menuStr):
	shortCutCmd = '"' + menuStr + '" = "-";'
	menu_set_shortcut(shortCutCmd)

def menu_set_command_key(menuStr, key):
	if key == "":
		commandKey = ""		# remove shortcut
	elif is_on_mac():
		commandKey = 'a'	# apple key on mac
	else:
		commandKey = 'c'	# control key on windows
				
	shortCutCmd = '"' + menuStr + '" = "' + commandKey + '-' + key + '";'
	menu_set_shortcut(shortCutCmd)

#=== showscreens & messenger
def showscreen(screen_name):
	menu("Video", screen_name)
	
def showscreen_rotation():
	showscreen("Toggle Rotation ShowScreen")

def showscreen_message_set(msg):
	pref_set("Custom ShowScreen message", msg)

def showscreen_message(msg):
	showscreen_message_set(msg)
	showscreen("Display Recent ShowScreen Message")

def showscreen_drink_specials(msg):
	showscreen_message_set(msg)
	showscreen("Drink Specials")

def messenger_set_looping(loopB):
	pref_set("Loop Messenger", loopB)
	
def messenger_message_set(msg):
	pref_set("Custom messenger message", msg)

def messenger_message(msg):
	messenger_message_set(msg)
	menu("Video", "Display Recent Messenger Message")

def messenger_rotation():
	menu("Video", "Display Messenger Rotation")
	
#=== progress
def prog_set_str(str):
	do_cmd(enum_cmds().kScriptCommand_Prog_SetStr, str)

def prog_set(cur, max = -1):
	do_cmd(enum_cmds().kScriptCommand_Prog_SetCurMax, cur, max)

def pref_get(keyStr):
	return do_cmd(enum_cmds().kScriptCommand_GetPref, keyStr)

#=== prefs
def pref_set(keyStr, val):
	return do_cmd(enum_cmds().kScriptCommand_SetPref, keyStr, val)

#=== server
def server_get_pass():
	return pref_get("Server admin password")

def server_set_pass(password):
	return pref_set("Server admin password", password)

def server_cmd(servCmd, *args):
	args = (servCmd, server_get_pass()) + args
	return do_cmd(enum_cmds().kScriptCommand_Server, *args)

# get list of playlist items: a PLI is a song, a singer, or a playlist
# passing CWS_Path_PLAYLISTS 
# 	without a singer logged in gives you a list of playlists in the Sources list,
#	WITH singer logged in gives you that singer's list of playlists 
# CWS_Path_SONGS 
# 	without a playlist ID, you will get the playlist designated  as "Playlist is used for Server Search"
#	WITH a playlist ID gives you all the songs in that playlist
def server_get_plItem_list(serverCmd, pl_ID = -1):
	resultsDict = server_cmd(serverCmd, pl_ID)

	# there is only one item in this dict, an array of playlists
	arrayOfPlaylists = resultsDict['Playlists']

	# there is only one item in this array, a single playlist's dict
	playListDict = arrayOfPlaylists[0]
	
	nameStr = playListDict['Name']

	# get the list of items, which is the list of playlists in the Sources list
	# or is a list of PLI_IDs in the playlist itself
	itemArray = playListDict['Playlist Items']
	
	return nameStr, itemArray

#=== playlists
def get_playlist(pl_ID):
	return server_get_plItem_list(enum_server().CWS_Path_SONGS, pl_ID)
	
#=== dialogs
'''dialog_three_button args are:
dialog title (short string) (shown in large text)
dialog messgae or "" (can be a long string) (shown in small text)
left button text or ""
left button enum_button_type or 0
middle button text or ""
middle button enum_button_type or 0
right button text or ""
right button enum_button_type or 0
checkbox text or "" or don't pass anything
checkbox default value (boolean) or don't pass anything
return is array with these values:
	button pressed (1, 2 or 3)
	current mark value
	name of button pressed
'''
def	dialog_three_button(*args):
	return do_cmd(enum_cmds().kScriptCommand_3ButtonDialog, *args)

# returns True if user hit OK
def	dialog_ok_cancel(title):
	print 'about to show dialog'
	
	resultArray = dialog_three_button(
		title, "", 
		"Cancel", enum_button_type().kButtonType_CANCEL, 
		"", 0, 
		"OK", enum_button_type().kButtonType_DEFAULT)
	
	button = resultArray[0]
	if button == 3:
		okB = True
	else:
		okB = False
		
	return okB

def	dialog_message(str):
	dialog_three_button(str, "", "", 0, "", 0, "OK", enum_button_type().kButtonType_DEFAULT_CANCEL)

'''dialog_input args are:
dialog title (short string) (shown in large text)
dialog messgae or "" or nothing (can be a long string) (shown in small text)
default string to put into text edit area or "" or nothing
True or False indicating "Password", or nothing.  if True, user sees bullets on screen, not characters
'''
def dialog_input(*args):
	return do_cmd(enum_cmds().kScriptCommand_TextDialog, *args)
	
#-----------------------------------------------------
if __name__ == "__main__":
	print str(enum_cmds())

# -*- coding: utf-8 -*- 
import kjams, time

g_iTunesLib = 0

if kjams.is_on_mac():
	from Foundation import *
	from ScriptingBridge import *
else:
	from win32com.client.gencache import EnsureDispatch

def	iTunesLib():
	global g_iTunesLib
	
	if isinstance(g_iTunesLib, int):
		if kjams.is_on_mac():
			g_iTunesLib = SBApplication.applicationWithBundleIdentifier_("com.apple.iTunes")
		else:
			g_iTunesLib = EnsureDispatch("iTunes.Application")
			
	return g_iTunesLib

def initialize():
	global g_iTunesLib
	if kjams.is_on_windows():
		# on windows, the global var does not survive multiple invocations
		g_iTunesLib = 0
	iTunesLib()

def enum_play_states():
	commands = kjams.enum(
		'iTunesEPlSStopped', 
		'iTunesEPlSPlaying',
		'iTunesEPlSPaused',
		'iTunesEPlSFastForwarding',
		'iTunesEPlSRewinding')
	return commands

def lib_play_states():
	enum_states = enum_play_states()
	lib_states = {}
	lib_states[enum_states.iTunesEPlSStopped]			= 'kPSS'
	lib_states[enum_states.iTunesEPlSPlaying]			= 'kPSP'
	lib_states[enum_states.iTunesEPlSPaused]			= 'kPSp'
	lib_states[enum_states.iTunesEPlSFastForwarding]	= 'kPSF'
	lib_states[enum_states.iTunesEPlSRewinding]			= 'kPSR'
	return lib_states

# returns an enum_play_states (integer)
def play_state():
	enum_states = enum_play_states()

	return_state = 0

	if kjams.is_on_mac():
		lib_states = lib_play_states()
		play_state = iTunesLib().playerState()
		
		# there is no paused on windows, 
		# so call it stopped on mac to match windows
		if play_state == lib_states[enum_states.iTunesEPlSPaused]:
			play_state = lib_states[enum_states.iTunesEPlSStopped]

		cur_lib_state = kjams.NumberToFourCC(play_state)
		
		for enum_state in range(len(lib_states)):
			if cur_lib_state == lib_states[enum_state]:
				return_state = enum_state
				break
	else:
		play_state = iTunesLib().PlayerState
		
		# there is no paused state on windows, 
		# so skip over it from the enum
		if play_state >= enum_states.iTunesEPlSPaused:
			play_state = play_state + 1
		
		return_state = play_state

	return return_state
	
def get_volume():
	if kjams.is_on_mac():
		return iTunesLib().soundVolume()
	else:
		return iTunesLib().SoundVolume
	
def set_volume(vol):
	if kjams.is_on_mac():
		# note the trailing underscore
		iTunesLib().setSoundVolume_(vol)
	else:
		iTunesLib().SoundVolume = vol

def next():
	if kjams.is_on_mac():
		iTunesLib().nextTrack()
	else:
		iTunesLib().NextTrack()

def playpause():
	if kjams.is_on_mac():
		iTunesLib().playpause()
	else:
		iTunesLib().PlayPause()

def pause():
	if play_state() == enum_play_states().iTunesEPlSPlaying:
		playpause()

def play():
	if play_state() != enum_play_states().iTunesEPlSPlaying:
		playpause()

#-----------------------------------------------------
if __name__ == "__main__":
	pass

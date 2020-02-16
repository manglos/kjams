# -*- coding: utf-8 -*- 
import kjams, itunes, time

def crossfade():
	itunes.initialize();
	cmds = kjams.enum_cmds()

	fade_durationF = kjams.pref_get('Crossfade Duration (seconds)')

	# Number of steps in fade
	fadeSteps = 20
	
	# sets how long in seconds between each step in the fade 
	fadeDelay = fade_durationF / fadeSteps

	# Get current audio volume from kJams	
	kJamsMaxVolume = kjams.get_volume();

	# set iTune volume maximum.
	iTunesMaxVolume = itunes.get_volume()
	
	# sets how much in percentage the volume is decreased per step
	kJFadeStep = kJamsMaxVolume / fadeSteps
	iTFadeStep = iTunesMaxVolume / fadeSteps
	
	# this is the minimum volume setting 
	MinVolume = 0
	
	if itunes.play_state() == itunes.enum_play_states().iTunesEPlSPlaying:
		# set all volumes to cross fade starting values 
		kJamsVolume = MinVolume
		iTunesVolume = iTunesMaxVolume
		
		kjams.set_volume(MinVolume)
		kjams.do_cmd(cmds.kScriptCommand_PLAY_PAUSE)
		
		while not (iTunesVolume <= 0 and kJamsVolume >= kJamsMaxVolume):
			iTunesVolume = iTunesVolume - iTFadeStep
			kJamsVolume = kJamsVolume + kJFadeStep
			itunes.set_volume(iTunesVolume)
			kjams.set_volume(kJamsVolume)
			time.sleep(fadeDelay)
		
		itunes.pause()
		itunes.set_volume(iTunesMaxVolume)
		
	else:
		# set all volumes to cross fade starting values 
		iTunesVolume = MinVolume
		kJamsVolume = kJamsMaxVolume
		kjams.set_volume(kJamsMaxVolume)
		itunes.set_volume(MinVolume)

		itunes.play()
		
		while not (kJamsVolume <= 0 and iTunesVolume >= iTunesMaxVolume):
			iTunesVolume = iTunesVolume + iTFadeStep
			kJamsVolume = kJamsVolume - kJFadeStep
			itunes.set_volume(iTunesVolume)
			kjams.set_volume(kJamsVolume)
			time.sleep(fadeDelay)

		kjams.do_cmd(cmds.kScriptCommand_STOP)
		kjams.set_volume(kJamsMaxVolume)
		
# ---------------------------------------------------
if __name__ == "__main__":
	crossfade()

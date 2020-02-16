# -*- coding: utf-8 -*- 
import kjams, itunes, time

'''	
Please have iTunes and kJams running before launching this script and 
have a playlist selected in iTunes 
The simple logic of the script assumes that if iTunes is playing and this script is run, 
you want to cross fade over to kJams.. Alternately, if iTunes is not playing a track, 
it assumes you want to cross fade over to iTunes. 
when you are ready to cross fade to kJams, make sure your next song is 
highlighted/selected.  It will NOT automatically go to the next track in 
your kJams playlist.
Unlike the original version of this script, you do not need to set your max volume levels. 
Instead, it will poll iTunes and kJams for their current volumes, and then cross fade using 
those values. Even if these volumes are very different, it will fade them such that they 
reach their appropriate values at the same time. No more need for these values to be identical!
Although I have tested this code, I make no guarantees with this code, 
any disasters that occur are not my fault.  Use at your own risk!! 
'''

# who is playing now?
def enum_player():
	commands = kjams.enum(
		'kJams', 
		'iTunes')
	return commands

def auto_crossfader():
	itunes.initialize();
	cmds = kjams.enum_cmds()
	player = enum_player()

	fade_durationF = kjams.pref_get('Crossfade Duration (seconds)')

	# Number of steps in fade
	fadeSteps = 20
	
	# sets how long in seconds between each step in the fade 
	fadeDelay = fade_durationF / fadeSteps

	# Get current audio volume from kJams	
	kJamsMaxVolume = kjams.get_volume();

	# set iTunes volume maximum.
	iTunesMaxVolume = itunes.get_volume()
	
	# this is the minimum volume setting 
	MinVolume = 0

	# cur_player will be either 0 for kJams or 1 for iTunes
	cur_player = player.kJams
	prev_player = player.kJams

	while True:
		# is kJams playing?
		playMode = kjams.do_cmd(cmds.kScriptCommand_GET_PLAY_MODE)
		
		# Check to see if kJams is playing
		if playMode == kjams.enum_play_modes().kPlayModeType_PLAYING:
		
			# if kJams is playing, set current cur_player to kJams
			cur_player = player.kJams
			
			# If prev_player is not the same as the current state
			# i.e. if kJams is has just started playing, fade in kJams and fade out iTunes
			if prev_player == player.iTunes:
				currentVolume = kjams.get_volume()
				
				if currentVolume != MinVolume:
					kJamsMaxVolume = currentVolume
					
				# sets how much in percentage the volume is decreased per step
				kJFadeStep = kJamsMaxVolume / fadeSteps
				kJamsVolume = MinVolume
				
				# get current starting volume from iTunes
				iTunesVolume = itunes.get_volume()
				
				kjams.set_volume(MinVolume)
				
				while not (iTunesVolume <= MinVolume and kJamsVolume >= kJamsMaxVolume):
					iTunesVolume = iTunesVolume - iTFadeStep
					kJamsVolume = kJamsVolume + kJFadeStep
					
					if kJamsVolume > kJamsMaxVolume:
						kJamsVolume = kJamsMaxVolume
					
					itunes.set_volume(iTunesVolume)
					kjams.set_volume(kJamsVolume)
					time.sleep(fadeDelay)

				# if you do NOT want iTunes to pick up where it left off, un-comment the following line
				# itunes.next()
				itunes.pause()
		else:
			# if kJams is not playing, set current cur_player to iTunes
			cur_player = player.iTunes
			
			#if kJams has just now been paused, cross fade in iTunes
			if prev_player == player.kJams:
			
				currentVolume = itunes.get_volume()
				
				if currentVolume != MinVolume:
					iTunesMaxVolume = currentVolume
					
				iTFadeStep = iTunesMaxVolume / fadeSteps
				
				#Get current audio volume from kJams
				kJamsMaxVolume = kjams.get_volume()
				kJFadeStep = kJamsMaxVolume / fadeSteps
				kJamsVolume = kJamsMaxVolume
				
				#set all volumes to cross fade starting values 
				iTunesVolume = MinVolume
				itunes.set_volume(MinVolume)
				itunes.play()
				
				while not (iTunesVolume >= iTunesMaxVolume):
					iTunesVolume = iTunesVolume + iTFadeStep

					if iTunesVolume > iTunesMaxVolume:
						iTunesVolume = iTunesMaxVolume

					itunes.set_volume(iTunesVolume)
					time.sleep(fadeDelay)

				#Get current audio volume from iTunes
				iTunesMaxVolume = itunes.get_volume()
				iTFadeStep = iTunesMaxVolume / fadeSteps
				kjams.set_volume(MinVolume)
			
		prev_player = cur_player
		time.sleep(0.5)

		
# ---------------------------------------------------
if __name__ == "__main__":
	auto_crossfader()

# -*- coding: utf-8 -*- 
import kjams, itunes

def main():
	kjams.do_cmd(kjams.enum_cmds().kScriptCommand_CAM_SHOOT)

	enum_play_states = itunes.enum_play_states()
	cur_state = itunes.play_state()

	print "cur_state: " + str(cur_state)
	print "Play state: " + enum_play_states.reverse_mapping[cur_state]

	# or try this
	if False:
		if cur_state == enum_play_states.iTunesEPlSPaused:
			itunes.playpause()

	print "Volume: " + str(itunes.get_volume())
	
	itunes.set_volume(75)
	itunes.next()
	
	print "New Volume: " + str(itunes.get_volume())


#-----------------------------------------------------
if __name__ == "__main__":
	main()

# -*- coding: utf-8 -*- 
import kjams

def main():
	cmd = kjams.enum_cmds()

	# pl = play list
	pl_ID = kjams.do_cmd(cmd.kScriptCommand_GetSelectedPlaylist)
	
	# returns an array (list) of PLI_IDs
	pli_id_list = kjams.do_cmd(cmd.kScriptCommand_GET_PLI_LIST, pl_ID)
	
	# the following does NOT dothe same thing: 
	# nameStr, pli_id_list = server_get_plItem_list(enum_server().CWS_Path_SONGS, pl_ID)
	# the above line returns a list of dicts, each being a song, containing strings
	# with name, artist, album strings etc
	
	# selection is also a pli_id_list
	# cur_selection = kjams.do_cmd(cmd.kScriptCommand_GetSelection, pl_ID)
	
	# select first item in the play list	
	if len(pli_id_list) != 0:
		# pli = play list item
		pli_ID = pli_id_list[0]			# take first item 
		single_selection = [ pli_ID ]	# make a new list (array) with just that
		kjams.do_cmd(cmd.kScriptCommand_SetSelection, pl_ID, single_selection)
	
		# always stop before attempting to play the selected song, otherwise you 
		# might just resume a paused song in another playlist
		#kjams.do_cmd(cmd.kScriptCommand_STOP)
		#kjams.do_cmd(cmd.kScriptCommand_PLAY_PAUSE)

		# here's how to pick "Convert Selection To..."  
		# no mater what the encoder string is
		# note that indexes are a bit more fragile because they can  change
		# between releases (tho very unlikely, you should still check each new release)
		# be sure to select something first!
		'''
		kAdvancedMenu = 4
		kConvertSelectionItem = 10
		kjams.menu(kAdvancedMenu, kConvertSelectionItem)
		'''
		
		song_ID = kjams.do_cmd(cmd.kScriptCommand_PLI_TO_SONG_ID, pl_ID, pli_ID)
		songDict = kjams.do_cmd(cmd.kScriptCommand_GetMeta, song_ID)
		#print songDict	# <- will print strings as ASCII
		
		# see https://karaoke.kjams.com/wiki/Xattr for dictionary keys
		zipPathDict = songDict['Sfs2']
		zipPath = zipPathDict['path']
		print zipPath	# <- utf8 now, you're welcome

#-----------------------------------------------------
if __name__ == "__main__":
	main()

# -*- coding: utf-8 -*- 
import kjams

def main():

	# illegal
	if False:
		# note: you can NOT mix names and indexes, this is illegal:
		kjams.menu("Controls", 2)
	
	# menus and sub menus
	if True:
		# call menus by name.  note: use the localized names
		# kjams.menu("File", "New Preset Playlist", "Unique Songs")
		kjams.menu("Controls", "Sync-Slipping", "Global No Slip")

	# multi-language support
	if False:
		# "Global No Slip" in chinese (must be running kJams in Chinese for this to work!)
		# be sure to edit this file as UTF-8!
		kjams.menu("控件", "同步滑帧", "全局无滑帧")
	
	# menu item indexes
	if False:
		# menu item indexes start at zero (the apple menu)
		# indexes work with any localization
		# the "apple" menu counts on windows too, but it is empty.
		# that way, the same indexes work on both mac and windows, eg:
		kjams.menu(1, 1, 8)	# File->New Preset Playlist->Corrupted Zip Files

	# keyboard shortcuts	
	if False:
		# same exact syntax as the keyboard shortcuts file
		# https://karaoke.kjams.com/wiki/Custom_Keyboard_Shortcuts
		# note these are necessarily platform DEPENDENT, so you have to 
		# do things slightly differently depending on platform

		# see 	menu_set_command_key in kjams.py for an example of this
		kjams.menu_set_command_key("SubMenu/Python/test_menus.py", "\'")

#-----------------------------------------------------
if __name__ == "__main__":
	main()

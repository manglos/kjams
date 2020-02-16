# -*- coding: utf-8 -*- 
import kjams, time, sys

# kJams will auto-run this script on startup.
# to open/view a script, hold down the alt/opt key when you pick it from the Special menu

def main():
	print sys.path

	cmd = kjams.enum_cmds()

	print "startup script BEGIN" # print statements go to the kJams Log File
	# want to see the logs? do this line:
	# kjams.menu("Help", "Reveal Logs")

	resultStr = kjams.do_cmd(cmd.kScriptCommandStr_GetAppVersion)
	print 'App Version: ' + resultStr;

	# when you select a script from the menu, if you have the alt key/option down
	# then kjams will tell the OS to open the file, instead of run the script inside kJams.
	# the point is that you want to view or edit the script, rather than have python
	# inside kjams execute it.
	# On windows, opening a .py script will cause the OS to *run* it (and not even inside kjams)
	# so there is the option to reveal it instead so you can right click and pick "edit".
	kjams.pref_set("python: alt key causes reveal instead of open", kjams.is_on_windows())
	
	# turn this on if you don't want to see the test scripts
	if False:
		kjams.pref_set("python: hide test scripts", True)
	
	# let's give a key shortcut to the new itunes crossfader	
	kjams.menu_set_command_key("SubMenu/Python/itunes_crossfade.py", "\'")
		
	# if you want assurance that your script ran, have it make a sound
	# when it completes
	# kjams.do_cmd(cmd.kScriptCommand_CAM_SHOOT)

	print "startup script END"

#-----------------------------------------------------
if __name__ == "__main__":
	main()

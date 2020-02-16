# -*- coding: utf-8 -*- 
import kjams, time

def main():
	cmd = kjams.enum_cmds()

	while True:
		for x in range (0, 20):
			kjams.do_cmd(cmd.kScriptCommand_VOL_UP)
			# same thing: 
			# kjams.menu("Controls", "Volume Up")
			time.sleep(0.25)
		for x in range (0, 20):
			kjams.do_cmd(cmd.kScriptCommand_VOL_DOWN)
			# same thing:
			# kjams.menu("Controls", "Volume Down")
			time.sleep(0.25)

#-----------------------------------------------------
if __name__ == "__main__":
	main()

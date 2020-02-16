# -*- coding: utf-8 -*- 
import kjams

def log_success(msg, successB, str):
	if successB:
		print msg + " worked: " + str
	else:
		print msg + "failed: " + str

def do_test(orig_str):
	cmd_enum = kjams.enum_cmds()
	
	print "---------------"
	print "Original string: " + orig_str
	print "converting..."

	oldstr = orig_str;
	newstr = kjams.do_cmd(cmd_enum.kScriptCommand_Unicode_Test, oldstr)
	log_success("string", oldstr == newstr, newstr);
	
	oldstr = unicode(orig_str, "UTF-8")
	oldstr.encode("UTF-8")
	newstr = kjams.do_cmd(cmd_enum.kScriptCommand_Unicode_Test, oldstr)
	newstr = unicode(newstr, "UTF-8")
	log_success("unicode", oldstr == newstr, newstr);

	print "---------------"
	
def main():
	do_test("frøânçïé")
	do_test("控件")

#-----------------------------------------------------
if __name__ == "__main__":
	main()

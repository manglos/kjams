# -*- coding: utf-8 -*- 
import kjams

def main():
	urlStr = kjams.do_cmd(cmd.kScriptCommand_Get_ServerAddress)
	kjams.do_cmd(cmd.kScriptCommand_Create_QR_Code, "~/Desktop", "qr_server", urlStr)

#-----------------------------------------------------
if __name__ == "__main__":
	main()

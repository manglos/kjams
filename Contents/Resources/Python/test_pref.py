# -*- coding: utf-8 -*- 
import kjams

def main():
	cmd = kjams.enum_cmds()

	print "getting font size"
	fontSizeF = kjams.pref_get("Browser Font Size")
	
	print "got font size"
	
	print "font size = " + str(fontSizeF)

	streamPacks = kjams.pref_get("TriceraSoft Streaming Packs")
	print streamPacks
	
	triceraWind = kjams.pref_get("TriceraSoft Gift Pack Window Rectangle")
	print triceraWind
	
	checkDate = kjams.pref_get("date of last check: app")
	print checkDate

	maxResultsKey = "Maximum number of items in web search results list"
	resultsI = int(kjams.pref_get(maxResultsKey))
	print "web results size was = " + str(resultsI)
	
	kjams.pref_set(maxResultsKey, 500)
	print "web results now set to 500"
	
#-----------------------------------------------------
if __name__ == "__main__":
	main()

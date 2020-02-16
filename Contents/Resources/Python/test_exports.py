# -*- coding: utf-8 -*- 
import kjams, time, math

Option_Is_ON	= 0;
Option_Key		= 1;

def is_test():
	# set to True to just generate the file names
	# but not do any actual exporting
	return False

def legal_options(options_enum, options):
	legalB = True;
	
	if options[options_enum.HD][Option_Is_ON]:
		if options[options_enum.PAD][Option_Is_ON]:
			legalB = False;
	else:
		if options[options_enum.HQ][Option_Is_ON]:
			legalB = False;
	
	return legalB;

def main():
	# get the songID of our song
	norml_song_ID = 535762;		#	sunfly
	media_song_ID = 1106433;	#	producer

	kjams.pref_set("Messenger Rotation size", 3)

	outFolderStr	= "~/Desktop/export tests"
	encoderStr		= "QuickTime Movie"
	presetStr		= "Animation / Lossless"
	
	options_enum = kjams.enum(
		'MS',		#	no key,	MediaStream
		'SAM',		#			SAMple
		'TRA',		#			TRAnsparent
		'PAD',		#			PADding
		'SLI',		#	no key,	SLIpping
		'HQ',		#			HQX Upscale
		'HD',		#	no key,	HighDef
	);
	
	options = {};	#	this is a map (dict)
	for curOption in options_enum.reverse_mapping:
		options[curOption] = [ False, "" ]
	
	# those with keys
	options[options_enum.TRA]	[Option_Key] = "QT Export with transparency";
	options[options_enum.PAD]	[Option_Key] = "Pad QuickTime Export to 320 x 240";
	options[options_enum.HQ]	[Option_Key] = "Use hq4x upscaling (fast computers only)";
	options[options_enum.SAM]	[Option_Key] = "QT Export only 30 seconds";

	outName_key = "QuickTime Export Name";
	skipExisting_key = "QuickTime Export Skip Existing";
	
	kjams.pref_set(skipExisting_key, True);
	
	loopSize = int(math.pow(2, len(options)))
	kjams.prog_set(0, loopSize)

	for optionBits in range(0, loopSize):
	
		outName		= ""
		i_hdB		= False;
		i_slipB		= False;
		i_songID	= norml_song_ID;
		
		for curOption in range(0, len(options)):
			testBit = 1 << curOption;
			is_onB = (optionBits & testBit) != 0;
			options[curOption][Option_Is_ON] = is_onB;
			outName += options_enum.reverse_mapping[curOption]
			if is_onB:
				outName += '1'
			else:
				outName += '0'

			outName += '-'
			
			if is_onB and options[curOption][Option_Key] == "":
				if curOption == options_enum.HD:
					i_hdB = True;
				elif curOption == options_enum.SLI:
					i_slipB = True;
				elif curOption == options_enum.MS:
					i_songID = media_song_ID;

		# pop the last dash		
		outName = outName[:-1]
		
		while kjams.do_cmd(kjams.enum_cmds().kScriptCommand_Is_Exporting, i_songID):
			time.sleep(0.2)
		
		kjams.prog_set_str(outName)
		kjams.prog_set(optionBits)

		nameStr = "song"
		if i_songID == media_song_ID:
			nameStr = "media song"
		
		if not legal_options(options_enum, options):
			print "Skipping (invalid): " + outName
		else:
			print outName

			if not is_test():
				# set prefs
				for curOption in range(0, len(options)):
					optionKey = options[curOption][Option_Key];
					if optionKey != "":
						is_onB = options[curOption][Option_Is_ON];
						print 'setting "' + optionKey + '" to ' + str(is_onB)
						kjams.pref_set(optionKey, options[curOption][Option_Is_ON]);
			
				slip_durationT = 0;
				if i_slipB: 
					slip_durationT = 73.5;
						
				slipDict = { 'Slip': slip_durationT };

				print 'setting "slipping" to ' + str(slip_durationT)
				kjams.do_cmd(
					kjams.enum_cmds().kScriptCommand_SetMeta,
					i_songID, slipDict)
			
				print 'setting "' + outName_key + '" to ' + outName
				kjams.pref_set(outName_key, outName);
			
				definitionStr = "SD"
				if i_hdB:
					definitionStr = "HD"
					
				print 'encoder preset is "' + definitionStr + '"'
				
				curPresetStr = presetStr;
				if (i_hdB):
					curPresetStr += " HD"
			
				if True:
					kjams.do_cmd(
						kjams.enum_cmds().kScriptCommand_EXPORT,
						i_songID, encoderStr, curPresetStr, outFolderStr)
		#------------------------------------------------
		
	kjams.pref_set(outName_key,					"");
	kjams.pref_set(options[options_enum.TRA]	[Option_Key], False);
	kjams.pref_set(options[options_enum.PAD]	[Option_Key], False);
	kjams.pref_set(options[options_enum.HQ]		[Option_Key], True);
	kjams.pref_set(options[options_enum.SAM]	[Option_Key], False);

	slipDict = { 'Slip': 0 };
	
	kjams.do_cmd(
		kjams.enum_cmds().kScriptCommand_SetMeta,
		norml_song_ID, slipDict)
		
	kjams.do_cmd(
		kjams.enum_cmds().kScriptCommand_SetMeta,
		media_song_ID, slipDict)

#-----------------------------------------------------
if __name__ == "__main__":
	main()

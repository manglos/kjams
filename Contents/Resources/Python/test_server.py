# -*- coding: utf-8 -*- 
import kjams, time

def printLoginErr(errDict):
	print "Error getting singer \"" + errDict["singername"] + "\": " + errDict["error"]

def main():
	servCmd = kjams.enum_server()
	
	# must use server admin password
	# to manipulate kJams thru the HTTP server
	# for things NOT related to singers (eg: new playlist etc)
	# prevents malicious people from destroying your show out from under you
	# i recommend you change this password below, to something only you know
	kjams.server_set_pass("once more, with feeling!")

	infoDict = kjams.server_cmd(servCmd.CWS_Path_INFO)
	
	print "things yes!"
	print "kJams Info:\n" + str(infoDict)

	# get list of all singers
	singersDict = kjams.server_cmd(servCmd.CWS_Path_SINGERS)
	singersA = singersDict['Playlists']
	singersDict = singersA[0]
	singersA = singersDict['Playlist Items']
	
	# named playlists
	if True:
		print "Got Singers list:\n" + str(singersA)

		rotationDict = kjams.server_cmd(servCmd.CWS_Path_ROTATION)
		print "Got Rotation:\n" + str(rotationDict)

	venue_playlist_id = str(singersDict['Playlist ID'])
	
	# Sources (list of playlists)
	if False:
		# CWS_Path_PLAYLISTS without a singer logged in 
		# gives you a list of playlists in the Sources list
		nameStr, itemArray = kjams.server_get_plItem_list(servCmd.CWS_Path_PLAYLISTS)
		
		for sourcePlayList in itemArray:
			print 'Playlist: ' + sourcePlayList['Name'] + ', pl_ID: ' + str(sourcePlayList['Playlist ID'])

		# now you know the playlist ID of the Library (which happens to always be 1)
		# so you could get all the songs now with: 
		# kjams.server_get_plItem_list(servCmd.CWS_Path_SONGS, 1)
		# or
		# kjams.get_playlist(1)

	# entire database test
	if False:
		# CWS_Path_SONGS without a playlist ID, you will get the playlist designated 
		# as "Playlist is used for Server Search"
		nameStr, itemArray = kjams.server_get_plItem_list(servCmd.CWS_Path_SONGS)
		# WARNING: this dictionary can be VERY VERY Big!!
		# may take a while to load, may crash due to out of memory error
				
		# show the playlist name
		print "Server Search playlist name: " + nameStr
		# don't print the actual list, it can be huge
		# print 'Song list:\n" + str(itemArray)
		
		# get a song
		firstSongDict = itemArray[0]
		print "First song: " + str(firstSongDict)
		
		# get the song ID (global ID unique to song, never changes)
		# refers to the same song in all playlists.  use to get/set meta on the song
		songID = firstSongDict['soID']
		
		# "playlist item index" is the same as "playlist item ID"
		# this ID is the index within it's playlist.  you can have the same
		# song in a playlist more than once, but each within the playlist
		# will have a unique pli_ID.  note that this number can change
		# between runs
		# use for re-ordering songs
		pli_ID = firstSongDict['piIx']
	
	# singer create / login test
	if True:
		# create a new singer, or log them in if they exist
		singerName = "ScoobyDoo"
		singerPass = "a"
		resultDict = kjams.server_cmd(servCmd.CWS_Path_NEW_SINGER, singerName, singerPass)
		
		loggedInB = 'singer' in resultDict
		
		if not loggedInB:
			printLoginErr(resultDict)
			resultDict = kjams.server_cmd(servCmd.CWS_Path_LOGIN, singerName, singerPass)

			print "Got Singer dict: " + str(resultDict)

			loggedInB = 'singer' in resultDict
			
			if not loggedInB:
				printLoginErr(resultDict)
			else:
				singerID = str(resultDict['singer_id'])
				print "Singer logged in"
		
		if loggedInB:
			print "Got Singer dict: " + str(resultDict)

			singerID = str(resultDict['singer_id'])
			singerName = str(resultDict['singername'])
			
			print "Got Singer Name: " + singerName

			# the singer is now logged in
			nameStr, itemArray = kjams.server_get_plItem_list(servCmd.CWS_Path_PLAYLISTS)
			print "Got playlists for singer: " + nameStr
			
			tonightDict = itemArray[1]	# 0 = Library, 1 = tonight, 2 = history, 3 = faves
			print "Tonight list:\n" + str(tonightDict)
			
			# get list of songs in Tonight list
			tonight_pl_ID = tonightDict['Playlist ID']
			nameStr, itemArray = kjams.server_get_plItem_list(servCmd.CWS_Path_SONGS, tonight_pl_ID)
			# or kjams.get_playlist(tonight_pl_ID)
			print 'Song list for ' + nameStr + ':\n' + str(itemArray)
			
			# now lets drop two songs from our favorite band into the singer's list
			nameStr, itemArray = kjams.server_get_plItem_list(servCmd.CWS_Path_SEARCH, "u2")
			
			print "Results:\n" + str(itemArray)
			
			if len(itemArray) > 1:
				songDict = itemArray[0]
				songID = songDict['soID']
				kjams.server_cmd(servCmd.CWS_Path_DROP, tonight_pl_ID, songID)

				songDict = itemArray[1]
				songID = songDict['soID']
				kjams.server_cmd(servCmd.CWS_Path_DROP, tonight_pl_ID, songID)
				
				# now let's re-order the songs
				# take the second song (1) and make it be first (0)
				kjams.server_cmd(servCmd.CWS_Path_REORDER, tonight_pl_ID, 1, 0)
			
		if loggedInB:
			print "about to call logout"
			kjams.server_cmd(servCmd.CWS_Path_LOGOUT)
			print "logout called"
		
		print "about to delete singer"
		kjams.server_cmd(servCmd.CWS_Path_REMOVE, venue_playlist_id, singerID)
		print "deleted singer"
		
	
	# playlist test
	if True:
		resultDict = kjams.server_cmd(servCmd.CWS_Path_NEW_PLAYLIST, "Hefty Manly Playlist")
		
		successB = 'Playlist ID' in resultDict

		if successB:
			pl_ID = resultDict['Playlist ID']
			print "success!  Playlist ID: " + str(pl_ID)
		else:
			print "failure to launch:\n" + str(resultDict)
		
	
#-----------------------------------------------------
if __name__ == "__main__":
	main()

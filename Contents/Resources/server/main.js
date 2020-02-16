/*	kJams Project - main.js
	Description: Main screen functionality.
	(c) 2007 kJams and David M. Cotter	*/

var timer = null;
var lastPing = 0;
var allowBackspace = false;
var totalMessages=5;
//checks to see if the search field it in focus. If it is, allow the user to use the Delete/Backspace key. Otherwise, set flag to trap it.
var inSearch = {
   on: function() {allowBackspace = true;},
   off: function() {allowBackspace = false;}
}
//variable to control if message is shown
var allowUnload = false;
//register function with the event handler
window.onbeforeunload = confirmUnload;
blinkSpeed=500;
tagName="blinker";
blinkerFlag=1;
blinkElement=document.getElementsByName(tagName);
blinkText();


function blinkText() {
	if (blinkerFlag== 1) {
		blinkState="visible";
	}
	else {
		blinkState="hidden";
	}
	blinkerFlag ^=1;
	for(i=0;i<blinkElement.length;i++) {
		blinkElement[i].style.visibility=blinkState;
	}

	setTimeout("blinkText()", blinkSpeed);
}

function getRadioValue(radioName) {
var radios=document.getElementsByName(radioName);
    for (var i = 0; i < radios.length; i++) {       
        if (radios[i].checked) {
            return (radios[i].value);
            break;
        }
    }
}

function filter(){
	if (document.getElementById("searchfield").value){
		m_doSearch();
	}
}

function messageLoad() {
	// totalMessages= number of messages
	var nodes = document.getElementById('hints').childNodes;
	for (var i=0; i<nodes.length; i++) {
		nodes[i].style.display = 'none';
	}
	var x=Math.floor(Math.random()*totalMessages+1);
	document.getElementById('hints').style.display='block';
	document.getElementById('hint'+x).style.display='block';
}

function m_populatePlaylists() {
	//Remove anything that was already there
	divObj = document.getElementById("playlists");
	
	for (var i = 0; i < divObj.childNodes.length; i++) {
		divObj.removeChild(divObj.childNodes[i]);
	}
	
	list = new KJDropList();
	list.create(divObj);
	playlistsList = list;
	
	getPlaylists(url_playlists, m_playlistsLoaded);
}

function m_playlistsLoaded(list) {
	listCtrl = document.getElementById("playlists").childNodes[0].parent;
	
	for (var i = 0; i < list.length; i++) {
		if ((list[i]['name'] == "Library") || (list[i]['name'] == "History"))
			dropTarget = false;
		else
			dropTarget = true;
		
		listCtrl.addItem("p" + list[i]['id'], list[i]['name'], dropTarget, null, false);
		
		//Library and History items are not rearrangeable
		if ((list[i]['name'] == "Library") || (list[i]['name'] == "History"))
			document.getElementById("p" + list[i]['id']).rearrange = false;
		else
			document.getElementById("p" + list[i]['id']).rearrange = true;
		
		//Keep track of ids for 'Tonight' and 'Favorites'
		if (list[i]['name'] == "Tonight") {
			pTonightID = list[i]['id'];
		}
		
		if (list[i]['name'] == "Favorites") {
			pFavoritesID = list[i]['id'];
		}
		
		//Store the playlist name in the DOM object
		document.getElementById("p" + list[i]['id']).name = list[i]['name'];
	}
	listCtrl.color();
	listCtrl.evtClick = m_populateSongs;
	listCtrl.evtDropInto = m_playlistDrop;
}

function m_populateSongs(playlist) {
	playlist = playlist.substring(1);
	
	//Hide
	if (songsList) {
		songsList.hide();
		
		if (songsList.playlist != "1") {
			songsList.destroy();
		}
	}
	
	//Hide "No Playlist" message, show waiting message
	document.getElementById("message").style.display = 'none';
	document.getElementById("msg_dosearch").style.display = 'none';
	document.getElementById("msg_error").style.display = 'none';
	document.getElementById("waiting").style.display = '';
	
	//If the list is already loaded, simply display it
	if ((playlist == "1") && (songsLists[playlist] != undefined)) {
		songsList = songsLists[playlist];
		songsList.show();
		document.getElementById("waiting").style.display = 'none';
	}
	
	//If it's the library, request that user do a search first
	else if (playlist == "1") {
		document.getElementById("waiting").style.display = 'none';
		document.getElementById("msg_dosearch").style.display = '';
	}
	
	else {
		//Playlist DOM object
		playlistObj = document.getElementById("p" + playlist);
		
		//Which columns are needed?
		var columns = Array("#", "Song Name", "Artist", "Album");
		
		if (playlistObj.name == "Tonight") {
			columns.push("Pitch");
			columns.push("Add to");
		}
		
		else if (playlistObj.name == "Favorites") {
			columns.push("Add to");
		}
		
		else {
			columns.push("Add to");
			columns.push("Add to");
		}
		
		songsList = new KJList();
		songsList.rearrange = playlistObj.rearrange;
		songsList.playlist = playlist;
		songsList.playlistName = playlistObj.name;
		songsList.create(document.getElementById("songs"));
		songsList.setColumns(columns, 0);
		songsList.evtDrop = m_songRearrange;
		songsLists[playlist] = songsList;
		getSongs(url_songs, m_songsLoaded, "playlist=" + playlist);
		
		if (false) {
			songsList.evtColClick = null;
		}
		else {
			songsList.evtColClick = m_sortSongs;
		}
	}
	
	m_sessionCheckin();
}

function m_songsLoaded(list) {
	//Hide waiting message
	document.getElementById("waiting").style.display = 'none';
	document.getElementById("displaybox").style.display='none';
	document.getElementById("hints").style.display='none';
	
	
	//Rearrangeable?
	if (songsList.rearrange)
		var rearrange = true;
	else
		var rearrange = false;
	
	for (var i = 0; i < list.length; i++) {
		//Add to favorites
		var favsButton = document.createElement("INPUT");
		favsButton.type = "button"
		favsButton.name = songsList.playlist + "-" + list[i]['itemId'];
		favsButton.songId = list[i]['id'];
		favsButton.value = "Favorites";
		favsButton.onmousedown = m_addToFavorites;
		
		//Add to Tonight
		var tonightButton = document.createElement("INPUT");
		tonightButton.type = "button";
		tonightButton.name = songsList.playlist + "-" + list[i]['itemId'];
		tonightButton.songId = list[i]['id']; 
		tonightButton.value = "Tonight";
		tonightButton.onmousedown = m_addToTonight;
	
		//Columns
		var columns = Array(i, list[i]['name'], list[i]['artist']);
		
		if (typeof(list[i]['album']) == "object") {
			var dropDown = document.createElement("SELECT");
			dropDown.name = list[i]['id'];
			
			for (var j = 0; j < list[i]['album']['items'].length; j++) {
				var optionObj = document.createElement("OPTION");
				optionObj.value = list[i]['album']['items'][j];
				optionObj.innerHTML = optionObj.value;
				
				if (list[i]['album']['default'] == j) {
					optionObj.selected = true;
				}
				
				dropDown.appendChild(optionObj);
			}
			
			columns.push(dropDown);
		}
		
		else {
			columns.push(list[i]['album']);
		}
		
		if (songsList.playlistName == "Tonight") {
			//Drop-down
			var options = {"+6" : 6, "+5" : 5, "+4" : 4, "+3" : 3, "+2" : 2, "+1" : 1, "0" : 0, "-1" : -1, "-2" : -2, "-3" : -3, "-4" : -4, "-5" : -5, "-6" : -6}
			var dropDown = document.createElement("SELECT");
			dropDown.name = list[i]['itemId'];
			dropDown.songId = list[i]['id'];
			dropDown.onchange = m_changePitch;
			for (option in options) {
				var optionObj = document.createElement("OPTION");
				optionObj.value = options[option];
				optionObj.innerHTML = option;
				
				if(list[i]['pitch'] == options[option]) {
					optionObj.selected = true;
				}
				
				dropDown.appendChild(optionObj);
			}
			
			columns.push(dropDown);
			columns.push(favsButton);
		}
		
		else if (songsList.playlistName == "Favorites") {
			columns.push(tonightButton);
		}
		
		else {
			columns.push(tonightButton);
			columns.push(favsButton);
		}
	
		index = songsList.addItem(songsList.playlist + "-" + list[i]['itemId'], columns, rearrange, null, false);
		
		document.getElementById(songsList.getByIndex(index)).songName	= list[i]['name'];
		document.getElementById(songsList.getByIndex(index)).songId		= list[i]['id'];
		document.getElementById(songsList.getByIndex(index)).piIx		= list[i]['itemId'];
	}
	
	songsList.color();
	
	if (songsList.playlistName != "Tonight" && songsList.playlistName != "History") {
		songsList.evtColClick = m_sortSongs;
	}
	else {
		songsList.evtColClick = null;
	}
}

function m_songRearrange(list, song, index, oldIndex) {
	sendData(url_rearrange, "playlist=" + list.playlist + "&index=" + index + "&oldIndex=" + oldIndex);
	m_sessionCheckin();
}

function m_playlistDrop(song, index, nodeId) {
	playlists	= document.getElementById("playlists").childNodes[0].parent;
	item		= songsList.getByID(song);
	
	if (songsLists[playlists.getByIndex(index).substring(1)]) { songsLists[playlists.getByIndex(index).substring(1)].destroy(); }
	songsLists[playlists.getByIndex(index).substring(1)] = null;
	sendData(url_drop, "playlist=" + playlists.getByIndex(index).substring(1) + "&song=" + songsList.getByID(song).songId);
	
	m_setStatus("Added \"" + item.songName + "\" to \"" + m_getPlaylistName(playlists.getByIndex(index)) + "\" ...");
	m_sessionCheckin();
}

function m_addToTonight(event) {
	playlists = document.getElementById("playlists").childNodes[0].parent;
	m_playlistDrop(event.target.name, playlists.getIndex("p" + pTonightID), event.target.name);
}

function m_addToFavorites(event) {
	playlists = document.getElementById("playlists").childNodes[0].parent
	m_playlistDrop(event.target.name, playlists.getIndex("p" + pFavoritesID), event.target.name);
}

function m_sortSongs(list, column) {
	var filterVal=getRadioValue('filters');
	list.removeAll();
	list.setPrimaryCol(column);
	messageLoad();
	document.getElementById("displaybox").style.display='';	
	if (document.getElementById("searchfield").value) {
		search = "&search=" + filterVal + document.getElementById("searchfield").value;
	}
	
	getSongs(url_sort, m_songsLoaded, "playlist=" + list.playlist + "&orderby=" + column + search);
	m_sessionCheckin();
}

function m_changePitch(event) {
	sendData(url_pitch, "song=" + event.target.songId + "&pitch=" + event.target.value);
	m_sessionCheckin();
}

function m_doSearch() {
		var filterVal=getRadioValue('filters');
		messageLoad();
		document.getElementById("displaybox").style.display='';
		
		//Select "Library" in the side bar
		playlistsList.select(playlistsList.getByID(playlistsList.getByIndex(0)));
	
		//Remove old search list if it's there
		if (songsLists["1"]) {
			songsLists["1"].parentObj.removeChild(songsLists["1"].container);
			songsLists["1"].parentObj.removeChild(songsLists["1"].columnsObj);
		}
	
		//Hide currently loaded list
		if (songsList) {
			songsList.hide();
		}
	
		document.getElementById("msg_dosearch").style.display = 'none';
		document.getElementById("message").style.display = 'none';
		document.getElementById("msg_error").style.display = 'none';
		document.getElementById("waiting").style.display = 'none';

		var columns = Array("#", "Song Name", "Artist", "Album", "Add to", "Add to");
	
		songsList = new KJList();
		songsList.rearrange = false;
		songsList.playlist = "1";
		songsList.playlistName = "Library";
		songsList.create(document.getElementById("songs"));
		songsList.setColumns(columns, 1);
		songsLists["1"] = songsList;
		getSongs(url_search, m_songsLoaded, "search="+filterVal+document.getElementById("searchfield").value);
		m_sessionCheckin();
}

function searchKeyPressed(event) {
	if (event.keyCode == 13) {
		m_doSearch();
	}
}

function m_getSongName(id) {
	songObj = document.getElementById(id);
	return songObj.songName;
}

function m_getPlaylistName(id) {
	playlistObj = document.getElementById(id);
	return playlistObj.name;
}

function kj_data_error(id, desc) {
	songsLists[songsList.id] = null;
	songsList.hide();
	document.getElementById("waiting").style.display = 'none';
	document.getElementById("displaybox").style.display='none';
	document.getElementById("hints").style.display='none';
	document.getElementById("msg_error").innerHTML = "Error: " + desc
	document.getElementById("msg_error").style.display = '';
}

function m_setStatus(status, revert) {
	statusObj = document.getElementById("status");
	statusObj.innerHTML = "<span style='color:#FF0000'>" + status + "</span>";
	var newInnerHTML='statusObj.innerHTML = "<span style="color:#FF0000">" + status + "</span>"';
	blink();
	setTimeout("statusObj.innerHTML = newInnerHTML",1250);
}

function blink(){ 
blinkFlag = 1 
blinkCount = 1 
blinkTimer();
}

function blinkTimer(){ 
if(blinkFlag==1){
blinkSpeed=250
blinkNumber=10 // If this value is even, the text flashes then remains visible. If it is odd, it flashes, then disappears
blinkCount++; 
document.getElementById("status").style.visibility='visible'; 
}else {
blinkCount++; 
document.getElementById("status").style.visibility='hidden'; 
}
blinkFlag^=1;
if (blinkCount < blinkNumber) {setTimeout('blinkTimer()', blinkSpeed);} 
} 

function trapDelete() {
	//Checks to see if the key pressed is the Delete/Backspace key, and if so, stop it from getting to the browser.
   var keyID = (window.event) ? event.keyCode : e.keyCode;
   if (keyID==8 && !allowBackspace){
	  return false;
   }
   return true;
}

function m_keyPressed(event) {
	//This is not IE-compliant code.
	if (event.keyCode == 46 || event.keyCode == 8) {
		if (!songsList.selection) {
			return;
		}
	
		playlistName	= songsList.playlistName;

		if (playlistName != "Library" && playlistName != "History") {
			selection	= songsList.selection;
			item		= songsList.getByID(selection);
			
			songsList.select(null);
			sendData(url_remove, "playlist=" + songsList.playlist + "&piIx=" + item.piIx);
			m_setStatus("Removed \"" + item.songName + "\" ...");
			songsList.removeItem(selection);
		}
	}
}

function m_pingSession() {
	var elapsedTime = new Date().getTime()/1000.0 - lastPing;
	
	if (elapsedTime >= 5) {
		sendData(url_ping, "");
		m_sessionCheckin();
		lastPing = new Date().getTime()/1000.0;
	}
}

function m_sessionCheckin() {
	/* A true or false value is set by the server before delivering this script 
		depending on preference. */
	if (!{auto_logout}) {
		return;
	}
	
	if (timer == null) {
		timer = setInterval("m_sessionLogout()", {timeout} * 1000);
	}
	else {
		clearInterval(timer);
		timer = null;
		return m_sessionCheckin();
	}
}

function m_sessionLogout() {
	// Sets the flag to tell confirmUnload subroutine that it is OK to let the user leave this page (close the Window, etc.)
	allowUnload = true;
	window.location=url_login;
}

function confirmUnload(){
	// function triggered by any closing of the current document
	if(!allowUnload){
		 		window.open(document.location.href);
	}
} 

function stopEvent(){
if (!e) var e = window.event;
    e.cancelBubble = true;
    if (e.stopPropagation) e.stopPropagation();
}
			
/* function loaded() {
	document.addEventListener('touchmove', function(e){ e.preventDefault(); });
	myScroll = new iScroll('songs');
}
//document.addEventListener('DOMContentLoaded', loaded);
*/
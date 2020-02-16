# -*- coding: utf-8 -*- 
import kjams, time

def main():

	# loop a message
	kjams.messenger_set_looping(True)
	kjams.messenger_message("We are showing a bunch of Show Screens!  Isn't this superduper fun?")

	# Random Showscreen
	if True:
		kjams.showscreen("Applause")
		time.sleep(5)
		
	# Show Rotation
	if True:
		kjams.showscreen_rotation()
		time.sleep(5)
		
	# send a "Drink Specials" Message
	if True:
		kjams.showscreen_drink_specials("Free drinks for the next five minutes!")
		time.sleep(5)
		
	# use the default message screen
	if True:
		kjams.showscreen_message("Donate to the kJams cause! Dave is working hard!")
		time.sleep(5)
	
	# finish up
	kjams.messenger_set_looping(False)
	kjams.menu("Video", "Hide ShowScreen")
		
#-----------------------------------------------------
if __name__ == "__main__":
	main()

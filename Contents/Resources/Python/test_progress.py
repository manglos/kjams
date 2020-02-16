# -*- coding: utf-8 -*- 
import kjams, time

def main():
	kjams.prog_set_str("testing progress bar")
	time.sleep(0.25)

	kjams.prog_set(0, 100)
	time.sleep(0.25)
	
	for x in range (0, 100):
		kjams.prog_set(x)
		time.sleep(0.05)

	kjams.prog_set_str("done!")
	kjams.prog_set(0, 0)	# return to "indeterminate" progress bar
	time.sleep(1)

#-----------------------------------------------------
if __name__ == "__main__":
	main()

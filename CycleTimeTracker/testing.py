import datetime
import time
import statistics as stat
print(time.localtime())
print(time.localtime().tm_min)
import gpiozero as io

	
inputPressActive = io.Button(2)
cyclingButton = io.LED(21)
cyclingButton.blink(on_time=200,off_time=200)
pressed = False
cycleTimeStamp = time.time()
while True:
	#print(inputPressActive.is_pressed)
	if  inputPressActive.is_pressed and pressed == False:
		print("false")
		cycleTime = time.time()-cycleTimeStamp
		cycleTimeStamp= time.time()
		print (cycleTime)
		pressed = True
	if (not inputPressActive.is_pressed) and pressed == True:
		print ("True")

		pressed = False

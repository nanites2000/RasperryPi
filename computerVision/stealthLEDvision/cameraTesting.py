import os
from PIL import Image
import numpy as np
from pprint import pprint
from picamera import PiCamera
from time import sleep

from PIL import Image, ImageFont, ImageDraw, ImageEnhance


np.set_printoptions(threshold = np.nan)

camera = PiCamera() 
camera.resolution = (2592,1944)
camera.awb_mode = 'off'
camera.exposure_mode = 'off'
camera.drc_strength = 'off'
camera._set_awb_gains((1.8,1.8))

def drawRectangle(center,size):
	
	draw.line(((center[0]-size,center[1]-size),(center[0]+size,center[1]-size),(center[0]+size,center[1]+size),(center[0]-size,center[1]+size),(center[0]-size,center[1]-size)), width = 10, fill = "red")
	
	
def averageBrightRect(center,size):

	
	crop = pixels[center[1]-size:center[1]+size,center[0]-size:center[0]+size]
	
	#pprint(crop)
	brightness = np.sum(crop)/size/size/3/4
	LEDOn = 0
	print(brightness)
	if brightness > 2000000:
		LEDOn = 1
def saveCrop(center,size,index):
    crop= source_img.crop((center[0]-size,center[1]-size,center[0]+size,center[1]+size))
    crop.save('/home/pi/Pictures/crop%s.jpg'%index)

i=0
#os.system("fswebcam -r 2048x1536 --no-banner croppy.jpg")

#shaftpic = Image.opencamera.capture('/home/pi/Pictures/image%s.jpg'%i)
#shaftpic = Image.open('croppy.jpg')
#shaftpic = Image.open('/home/pi/Pictures/image%s.jpg'%i)
#('/home/pi/Pictures/Webcam/shaftpic1.jpg')
camera.capture('/home/pi/Pictures/image%s.jpg'%i)
#shaftpic = Image.open('croppy.jpg')
#shaftpic = Image.open('/home/pi/Pictures/image%s.jpg'%i)
source_img = Image.open('/home/pi/Pictures/image%s.jpg'%i).convert("RGB")
pixels = np.asarray(source_img)
draw = ImageDraw.Draw(source_img)
#coordList= [(400,950),(1110,475),(1500,800)]
coordList= []
with open("pointData.txt","r") as file:
        #print(file.readlines().split('\t'))
        for index,coord in enumerate(file.readlines()):
            apart= coord.split('\t')
            coordList.append([int(apart[0]),int(apart[1].strip())])
size = 20	
for index,coord in enumerate(coordList):
        averageBrightRect(coord,size)
        saveCrop(coord,size,index)
        drawRectangle(coord,size)
            
    #draw.rectangle(((80, 80), (120, 120)), outline ="red")
    #draw.text((20, 70), "something123", font=ImageFont.truetype("font_path123"))
source_img.save('/home/pi/Pictures/image%s'%i, "BMP")

'''	

	px = shaftpic.load()
	print(px[4,4])import Tkinter
from PIL import Image, ImageTk
from sys import argv

window = Tkinter.Tk(className="bla")

image = Image.open(argv[1] if len(argv) >=2 else "bla2.png")
canvas = Tkinter.Canvas(window, width=image.size[0], height=image.size[1])
canvas.pack()
image_tk = ImageTk.PhotoImage(image)
canvas.create_image(image.size[0]//2, image.size[1]//2, image=image_tk)

def callback(event):
    print "clicked at: ", event.x, event.y

canvas.bind("<Button-1>", callback)
Tkinter.mainloop()
	data = np.asarray(shaftpic)
	print(np.shape(data))

	breaks = 20
	xgap=int(1536/breaks)
	ygap= int(2048/breaks)
	summer = 0import Tkinter
from PIL import Image, ImageTk
from sys import argv

window = Tkinter.Tk(className="bla")

image = Image.open(argv[1] if len(argv) >=2 else "bla2.png")
canvas = Tkinter.Canvas(window, width=image.size[0], height=image.size[1])
canvas.pack()
image_tk = ImageTk.PhotoImage(image)
canvas.create_image(image.size[0]//2, image.size[1]//2, image=image_tk)

def callback(event):
    print "clicked at: ", event.x, event.y

canvas.bind("<Button-1>", callback)
Tkinter.mainloop()
	LEDArray = np.zeros([breaks,breaks])
	for x in range(1,breaks):
		for y in range(1,breaks):
			crop = data[(x-1)*xgap:x*xgap,(y-1)*ygap:y*ygap]
			brightness = np.sum(crop)
			LEDOn = 0
			if brightness > 2000000:
				LEDOn = 1
			LEDArray[x][y] = int(LEDOn)
			#print(LEDArray[x][y], x,y)
			print('x=',x, ' y= ', y, 'LEDOn = ', LEDOn, 'brightness = ', brightness/xgap/ygap)
			
		
			summer+=1
	pprint(np.int_(LEDArray), width = 60)

#croppedIm = shaftpic.crop((0,0,1500,600))
#croppedIm.save('cropped.png')'''

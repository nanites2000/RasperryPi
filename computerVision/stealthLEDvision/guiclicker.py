import tkinter
from PIL import Image, ImageTk
from sys import argv
from PIL import Image
from picamera import PiCamera
from time import sleep

from PIL import Image, ImageFont, ImageDraw, ImageEnhance
with open("pointData.txt","w") as file:
	print("erased")
camera = PiCamera()
camera.resolution = (2592,1944)
camera.awb_mode = 'off'
camera.exposure_mode = 'off'
camera.drc_strength = 'off'
camera._set_awb_gains((1.8,1.8))
#sleep(3)
window = tkinter.Tk(className="bla")
camera.capture('/home/pi/Pictures/image0.jpg')
#shaftpic = Image.open('croppy.jpg')
width = 1296
height = 972
sleep(3)
image = Image.open('/home/pi/Pictures/image0.jpg')
image = image.resize((width, height), Image.ANTIALIAS)    # best down-sizing filter

#image = Image.open(argv[1] if len(argv) >=2 else "bla2.png")
canvas = tkinter.Canvas(window, width=image.size[0], height=image.size[1])
canvas.pack()
image_tk = ImageTk.PhotoImage(image)
canvas.create_image(image.size[0]//2, image.size[1]//2, image=image_tk)

def callback(event):
	with open("pointData.txt","a") as file:
		print(event.x*2, event.y*2)
		file.write(str(event.x*2) + "\t" + str(event.y*2) + '\n')

canvas.bind("<Button-1>", callback)
tkinter.mainloop()

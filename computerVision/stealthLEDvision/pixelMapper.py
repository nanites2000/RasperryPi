
import pyautogui
while True:
	xy = pyautogui.position()
	print(pyautogui.screenshot().getpixel(xy))

from tkinter import *
from tkinter import ttk
from threading import Thread
import gpiozero as io
import time
from collections import deque
import statistics as stat
import datetime
import numpy as np

import sqlite3
try:
	connection = sqlite3.connect("cycleTime.db",check_same_thread = False)
	cursor = connection.cursor()
except:
	print("Database Filed to Connect")
	
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

inputPressActive = io.Button(7, hold_time = 7, bounce_time=2)
cyclingButton = io.DigitalOutputDevice(21)
cyclingButton.blink(on_time=.04,off_time=.04)
global previous
previous = False
global size
size = 10
global stack
stack = deque(maxlen = size)
global greenTime
global yellowTime
global redTime
greentime = 2.8
yellowTime = 3.6
redTime = 12
global downtime
downtime = 0

#set up the table to enter data into
sql_command = """
CREATE TABLE  IF NOT EXISTS AutoJarCycleTimes ( 
datetime text,
cycleTime REAL 
);"""
cursor.execute(sql_command)










class check_button(Thread):
	global previous

	#try:
	#	connection2 = sqlite3.connect("cycleTime.db")
	#	cursor2 = connection2.cursor()
	#except:
	#	print("Database2 Filed to Connect")
	

	def __init__(self, labelText):
		Thread.__init__(self)
		#self.labelText = labelText
		self.b = False
		#self.previous = False
		labelText1 = "off"
		print("initial")
		
	def movingAverage(self, newTime):
		global stack
		global redTime
		size =10
		
		
		if newTime < redTime:
			stack.append(newTime)
			meanTime = stat.mean(stack)
			averageCycleTime.set(round(meanTime,1))
		
			if meanTime < greentime:	
				if str(averageCycle['background']) != "green":
					averageCycle.configure(background = "green")		
			elif meanTime < yellowTime:
				if str(averageCycle['background']) != "yellow":
					averageCycle.configure(background = "yellow")
			elif meanTime < redTime:
				if str(averageCycle['background']) != "red":
					averageCycle.configure(background = "red")
			else: 
				if str(averageCycle['background']) != "purple":
					averageCycle.configure(background = "purple")
			

	def checkloop(self):
		global connection2
		global cursor2
		
		global previous
		global downtime
		debounceMax = .5
		debounce = 0
		count = 0
		cycleTime = 0
		cycleTimeStamp = time.time()
		downtime = 0
		cycleQueArray =[]
		cycleQue = deque(cycleQueArray)
		startTime = 6
		cycleGoal = 34 #in seconds
		
		def goalPlot():
			breaks = [[6,30],[8,15],[10,15],[12,30]]  #[starttime, length in mins]
			goalxarray= [startTime]
			goalyarray =[0]
			goalx = deque(goalxarray)
			goaly = deque(goalyarray)
			breakSum = 0 #minutes of break that have accumlated as day goes by.
			#breaksum keeps the predicted jars needed accurate.
			
			for i in breaks:
				goalx.append(i[0])
				goaly.append((i[0]-startTime-breakSum/60)*3600/cycleGoal)
				goalx.append(i[0]+i[1]/60)
				goaly.append((i[0]-startTime-breakSum/60)*3600/cycleGoal)
				breakSum += i[1]
			goalx.append(startTime+8)
			goaly.append((8-breakSum/60)*3600/cycleGoal) 	
			plt.plot(goalx,goaly, 'r')			
			
		
		
		while True:

			#print(inputPressActive.is_held)
			#print(debounce)
			#labelText1.set(GPIO.input(7))
			#if inputPressActive.is_pressed == 0 and debounce < debounceMax:
				#debounce+= 1
				#print(debounce)
				#if debounce >= debounceMax:
					#previous = 0
					#debounce = 0
			
			if inputPressActive.is_pressed and previous == 0:
				#if self.b == False :
					
					#print ("on")
					#self.b = True
					previous = 1
					count += 1
					#print(count)
					countValueString.set(count)
					currentCycleTime.set(round(cycleTime,1))
					cycleTimeStamp = time.time()
					debounce = 0
					self.movingAverage(cycleTime)#calculates the moving average of last values	
					if cycleTime > redTime:
						downtime+=cycleTime
						downtimeValueString.set(round(downtime/60, 1))
					#fond the average of all the daily values	
					if cycleTime < redTime:
						cycleQue.append(cycleTime)
						totalMean = stat.mean(cycleQue)
						overallAverageValueString.set(round(totalMean,1))
					#now put the values into the graph and replot
					now = datetime.datetime.now()
					timeGraph.append(now.hour + now.minute/60 + now.second/3600)
					jarsGraph.append(count)
					goalPlot()
					plt.plot(timeGraph,jarsGraph, 'k')#also'ro' works
					canvas.draw()
				
					#sql_command ="INSERT INTO AutoJarCycleTimes (time,cycleTime) VALUES (%s, %s);" %(now, cycleTime)
					#cursor2.execute(sql_command)
					timestring = now.strftime('%Y-%m-%d %X.%f')
					sql_command ="INSERT INTO AutoJarCycleTimes (datetime, cycleTime) VALUES ('%s', %s);" %(timestring,cycleTime)
					cursor.execute(sql_command) 
					connection.commit()
					
					#cursor.execute("SELECT AVG(cycleTime) FROM autojarcycletimes")
					#print("fetchall:")
					#result = cursor.fetchall()
					#for r in result:
					#	print(r)

					
					
			#this checks how long since last button press and 
			#changes the background if not already that color		
			cycleTime = time.time()-cycleTimeStamp
				
			if cycleTime < 2.8:	
				if str(currentCycle['background']) != "green":
					currentCycle.configure(background = "green")
					
			elif cycleTime < 3.6:
				if str(currentCycle['background']) != "yellow":
					currentCycle.configure(background = "yellow")
			elif cycleTime < 12.0:
				if str(currentCycle['background']) != "red":
					currentCycle.configure(background = "red")
			else: 
				if str(currentCycle['background']) != "purple":
					currentCycle.configure(background = "purple")
					
			if  inputPressActive.is_pressed == 0:
				debounce += 1
				
			if debounce > 2000 and inputPressActive.is_pressed == 0: #this is used for debounce
				previous = 0
					
				
				#else:
					#labelText1.set("off")
					#print ("off")
					#self.b = False
					#previous = 1
					#while inputPressActive.is_pressed == 1: pass

root = Tk()


mainframe = ttk.Frame(root, padding="30 30 0 30")
mainframe.columnconfigure((0,1,2,3,4,5,6,7,8,9,10), weight=1)
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

#mainframe.columnconfigure(0, weight=1)
#mainframe.columnconfigure(1, weight=2)
#mainframe.columnconfigure(2, weight=1)

mainframe.rowconfigure(0, weight=1)
mainframe.rowconfigure(1, weight=15)
mainframe.rowconfigure(2, weight=5)

currentCycleTime = StringVar()
currentCycle = ttk.Label(mainframe,textvariable=currentCycleTime,padding="400 0 400 0") 
currentCycle.config(font=('Helvetica',250,'bold'))
currentCycle.grid(row=0,column=1, sticky=(E,W))

averageCycleTime = StringVar()
averageCycle = ttk.Label(mainframe,textvariable=averageCycleTime,padding="400 0 400 0") 
averageCycle.config(font=('Helvetica',250,'bold'))
averageCycle.grid(row=1,column=1, sticky=(E,W))

buttonframe = ttk.Frame(mainframe, padding="30 0 30 30")
buttonframe.grid(column=1, row=2, columnspan = 5)

downtimeLabel = ttk.Label(buttonframe,text="Downtime",padding="10 10 10 10") 
downtimeLabel.config(font=('Helvetica',40,'bold'))
downtimeLabel.grid(row=0,column=0, sticky=(E,W))

downtimeValueString =StringVar()
downtimeValueString.set("0")
downtimeValue = ttk.Label(buttonframe,textvariable=downtimeValueString,padding="15 15 35 15") 
downtimeValue.config(font=('Helvetica',75,'bold'))
downtimeValue.grid(row=0,column=1, sticky=(E,W))

countLabel = ttk.Label(buttonframe,text="Count",padding="10 10 10 10") 
countLabel.config(font=('Helvetica',40,'bold'))
countLabel.grid(row=0,column=2, sticky=(E,W))

countValueString =StringVar()
countValueString.set("0")
countValue = ttk.Label(buttonframe,textvariable=countValueString,padding="15 15 35 15") 
countValue.config(font=('Helvetica',75,'bold'))
countValue.grid(row=0,column=3, sticky=(E,W))

overallAverageLabel = ttk.Label(buttonframe,text="Average",padding="10 10 10 10") 
overallAverageLabel.config(font=('Helvetica',40,'bold'))
overallAverageLabel.grid(row=0,column=4, sticky=(E,W))

overallAverageValueString =StringVar()
overallAverageValueString.set("0")
overallAverageValue = ttk.Label(buttonframe,textvariable=overallAverageValueString,padding="15 15 0 15") 
overallAverageValue.config(font=('Helvetica',75,'bold'))
overallAverageValue.grid(row=0,column=5, sticky=(E,W))

fig = plt.figure(1)
canvas = FigureCanvasTkAgg(fig, master=root)
plot_widget = canvas.get_tk_widget()
canvas.get_tk_widget().place(x=1100, y=300)
graph = fig.add_subplot(111)
graph.set_xlabel('Date')
now = datetime.datetime.now()
global timeGraph
global jarsGraph
a = []
b = []
timeGraph = deque(a)
jarsGraph = deque(b)
plt.plot(timeGraph,jarsGraph, 'k')
plt.xlabel('Time')
plt.ylabel('Jars')
plt.title('Production')


root.title("Cycle Time") 
root.geometry('1900x1200')


chk1 = check_button(currentCycleTime)
c1 = Thread(target=chk1.checkloop)
c1.start()
root.mainloop()

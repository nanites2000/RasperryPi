from tkinter import *
from tkinter import ttk
from threading import Thread
import gpiozero as io
import time
from collections import deque
import statistics as stat
import datetime
import numpy as np
import pyautogui
import sqlite3

#set up the database
try:
	connection = sqlite3.connect("cycleTime.db",check_same_thread = False)
	cursor = connection.cursor()
except:
	print("Database Filed to Connect")
	
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

inputPressActive = io.Button(2)
cyclingButton = io.LED(21)
cyclingButton.blink(on_time=2,off_time=7)





global previous
previous = False
global size
size = 10
global stack
stack = deque(maxlen = size)
global greenTime
global yellowTime
global redTime
greenTime = 28
yellowTime = 36
redTime = 120
global alreadyReset 
alreadyReset = 0
cycleGoal = 34 #in seconds



class MyDialog:

    def __init__(self, parent):
        top = self.top = Toplevel(parent)
        self.TopLabel = Label(top, text='Enter the information below:')
        self.TopLabel.grid(row=0,column=1)
        self.TopLabel.config(font=("Courier", 15))


        self.mySubmitButton = Button(top, text='Submit', command=self.send)
        self.mySubmitButton.grid(row=4, column=1)
        self.mySubmitButton.config(font=("Courier", 35))

        self.operatorLabel=Label(top, text='Select Operator')
        self.operatorLabel.grid(row=1, column=0)
        self.operatorLabel.config(font=("Courier", 15))

        with open('operators.txt') as f:
            operators = f.read().splitlines()
        self.operatorName = StringVar(value=operators)
        self.operatorListbox = Listbox(top, height=15, listvariable=self.operatorName,exportselection=0)
        self.operatorListbox.grid(row=2, column=0)
        self.operatorListbox.config(font=("Courier", 15))

        self.machineLabel = Label(top, text='Select CNC Number')
        self.machineLabel.grid(row=1, column=1)
        self.machineLabel.config(font=("Courier", 15))

        with open('machines.txt') as f:
            machines = f.read().splitlines()
        self.machines = StringVar(value=machines)
        self.machineListbox = Listbox(top, height=15, listvariable=self.machines,exportselection=0)
        self.machineListbox.grid(row=2, column=1)
        self.machineListbox.config(font=("Courier", 15))

        self.partsLabel = Label(top, text='Select Part Number')
        self.partsLabel.grid(row=1, column=2)
        self.partsLabel.config(font=("Courier", 15))

        with open('parts.txt') as f:
            parts = f.read().splitlines()
        self.parts = StringVar(value=parts)
        self.partListbox = Listbox(top, height=15, listvariable=self.parts, exportselection=0)
        self.partListbox.grid(row=2, column=2)
        self.partListbox.config(font=("Courier", 15))



    def send(self):
        global user
        global machine
        global part
        global reconfig
        # self.userSelected = self.operatorListbox.get(self.operatorListbox.curselection())
        # self.machineSelected = self.machineListbox.get(self.machineListbox.curselection())
        # self.partSelected = self.partListbox.get(self.partListbox.curselection())
        user = self.operatorListbox.get(self.operatorListbox.curselection())
        machine = self.machineListbox.get(self.machineListbox.curselection())
        part = self.partListbox.get(self.partListbox.curselection())
        updateCurrent()
        reconfig=0
        plt.figure(1)
        plt.clf()
        plt.gcf().canvas.draw()
        valueEntry.delete(0, 'end')
        self.top.destroy()

def onClick():
    inputDialog = MyDialog(root)
    root.wait_window(inputDialog.top)









#set up the table to enter data into
sql_command = """
CREATE TABLE  IF NOT EXISTS CycleTimes ( 
rowid INTEGER PRIMARY KEY,
datetime text,
cycleTime REAL 
);"""
cursor.execute(sql_command)

sql_command = """
CREATE TABLE  IF NOT EXISTS DowntimeReasons ( 
rowid INTEGER PRIMARY KEY,
category text,
listgroup text,
reason text); 
);"""
cursor.execute(sql_command)



def goalPlot():
	global startTime
	global greenTime
	global yellowTime
	global redTime
	plotCurrent = 0
	now=datetime.datetime.now()
	currentTime =now.hour+now.minute/60+now.second/3600
	if  5 <= now.hour < 14:
		startTime = 6
		breaks = [[6,10],[8.16,20],[11.5,30]]  #[starttime, length in mins] in order of start time
	elif 14 <= now.hour <22:
		startTime = 14
		breaks = [[14,10],[16,20],[18.5,30]]  #[starttime, length in mins] in order of start time	
	else: 
		startTime = 22
		breaks = []
	#this keeps track of breaks passed to subtract from the downtime total
	scheduledBreaksTime = 0
	for i in breaks:
		if ((i[0] +i[1]/60) < currentTime):
			scheduledBreaksTime += i[1]
			
	goalxarray= [0]
	goalyarray =[0]
	goalx = deque(goalxarray)
	goaly = deque(goalyarray)
	breakSum = 0 #minutes of break that have accumlated as day goes by.
	#breaksum keeps the predicted jars needed accurate.
	
	
	for i in breaks:
		if i[0] <= currentTime < (i[0]+i[1]/60):
			goalx.append(i[0]-startTime)
			goaly.append((i[0]-startTime-breakSum/60)*3600/cycleGoal)
			goalx.append(currentTime- startTime)
			goaly.append((i[0]-startTime-breakSum/60)*3600/cycleGoal)
			plotCurrent = 0
			break
		if (i[0] + i[1]/60)<= currentTime:
			
			goalx.append(i[0]-startTime)
			goaly.append((i[0]-startTime-breakSum/60)*3600/cycleGoal)
			goalx.append(i[0] +i[1]/60-startTime)
			goaly.append((i[0]-startTime-breakSum/60)*3600/cycleGoal)
			breakSum += i[1]
			plotCurrent = 1
	if plotCurrent == 1:
		goalx.append(currentTime-startTime)
		goaly.append((currentTime-startTime-breakSum/60)*3600/cycleGoal) 	
	plt.plot(goalx,goaly, 'r')			
	return scheduledBreaksTime


def resetShift():
	global stack
	global downtime
	global count
	global totalMean
	global cycleQue
	global jarGraph
	global timeGraph
	global cycleTimeStamp
	
	
	#put old data into a textbox
	previousText.config(state = "normal")
	previousText.delete("1.0", "end")
	scheduledBreaksTime = goalPlot()
	try:
		insertText = "PREVIOUS SHIFT\nDowntime= "+str(round(downtime/60-scheduledBreaksTime,1)) + "\nCount= " + str(count)+"\nAverage= "+ str(round(totalMean,1)) +' '
		previousText.insert('1.0',insertText)	
		previousText.config(state = "disabled")
	except:
		print("Reset too early")
	
	
	downtime = 0
	stack = deque(maxlen = size)
	downtimeValueString.set(0)
	count = 0
	countValueString.set(count)
	totalMean = 0
	overallAverageValueString.set(0)
	cycleQue = []
	averageCycleTime.set(0)
	currentCycleTime.set(0)
	averageCycle.configure(background = "tan")	
	jarGraph = []
	timeGraph = []
	
	#set the shift start as the first time stamp on bootup
	timeList= list(time.localtime())
	timeList[3] = startTime - startTime % 1
	timeList[4] = (startTime - timeList[3])*60
	timeTuple = tuple(timeList)
	cycleTimeStamp = time.mktime(timeTuple) #convert back to a time object
		
	plt.clf()
	canvas.draw()
	
	

	print ("Reset " + str(datetime.datetime.now()))
	
	





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
		global meanTime
		
		
		
		if newTime < redTime:
			stack.append(newTime)
			meanTime = stat.mean(stack)
			averageCycleTime.set(round(meanTime,1))
		
			if meanTime < greenTime:	
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
		global totalMean
		global previous
		global downtime
		global count
		global cycleQue
		global timeGraph
		global jarGraph
		global cycleTimeStamp
		global startTime
		
		

		
		debounceMax = .5
		debounce = 0
		count = 0
		cycleTime = 0
		goalPlot()	
		#set the shift start as the first time stamp on bootup
		timeList= list(time.localtime())
		timeList[3] = startTime - startTime % 1
		timeList[4] = (startTime - timeList[3])*60
		timeTuple = tuple(timeList)
		cycleTimeStamp = time.mktime(timeTuple) #convert back to a time object
		
		downtime = 0
		cycleQueArray =[]
		cycleQue = deque(cycleQueArray)
		
		
		buttonCount = 0
		scheduledBreaksTime = 0  # keeps track of breaks that have passed to subract from total downtime
		

		
		while True:

			if inputPressActive.is_pressed and buttonCount < 10:
				buttonCount +=1
			if not inputPressActive.is_pressed and buttonCount > 0:
				buttonCount -=1
			
			
			
			if buttonCount > 8 and previous == 0:
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
					
					now = datetime.datetime.now()
					nowTime = now.hour + now.minute/60 + now.second/3600
					plt.clf()
					scheduledBreaksTime = goalPlot()
					self.movingAverage(cycleTime)#calculates the moving average of last values	
					
					if cycleTime > redTime:# and (nowTime-cycleTime/3600)>startTime and cycleTimeStamp<time.time():# the second condition prevents downtime from reading all night
						downtime+=cycleTime
						downtimeValueString.set(round(downtime/60-scheduledBreaksTime, 1))
					#fond the average of all the daily values	
					if cycleTime < redTime:
						cycleQue.append(cycleTime)
						totalMean = stat.mean(cycleQue)
						overallAverageValueString.set(round(totalMean,1))
					#now put the values into the graph and replot
					
					
					timeGraph.append(nowTime-startTime)
					jarGraph.append(count)
					
					
					plt.plot(timeGraph,jarGraph, 'k')#also'ro' works
					canvas.draw()
				
					#sql_command ="INSERT INTO AutoJarCycleTimes (time,cycleTime) VALUES (%s, %s);" %(now, cycleTime)
					#cursor2.execute(sql_command)
					timestring = now.strftime('%Y-%m-%d %X.%f')
					sql_command ="INSERT INTO AutoJarCycleTimes (datetime, cycleTime) VALUES ('%s', %s);" %(timestring,cycleTime)
					cursor.execute(sql_command) 
					connection.commit()
					
					#keeps screen saver off
					pyautogui.moveRel(1, 0, duration=0.01)
					pyautogui.moveRel(-1, 0, duration=0.01)
					
					

					
					
			#this checks how long since last button press and 
			#changes the background if not already that color		
			cycleTime = time.time()-cycleTimeStamp
				
			if cycleTime < greenTime:	
				if str(currentCycle['background']) != "green":
					currentCycle.configure(background = "green")
					
			elif cycleTime < yellowTime:
				if str(currentCycle['background']) != "yellow":
					currentCycle.configure(background = "yellow")
			elif cycleTime < redTime:
				if str(currentCycle['background']) != "red":
					currentCycle.configure(background = "red")
			else:
				#clear old downtime reasons and open the window to enter the new downtime
				
				if str(currentCycle['background']) != "purple":
					print("onclick")
					onClick()
					currentCycle.configure(background = "purple")
					
			if  inputPressActive.is_pressed == 0:
				debounce += 1
				
			#if debounce > 1000 and inputPressActive.is_pressed == 0: #this is used for debounce
			if buttonCount == 0:
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

previousText = Text(mainframe, width = 20, height = 4)
previousText.grid(column = 2, row = 0,sticky=(N))
previousText.config(font=('Helvetica',30,'bold'))
previousText.config(state = "disabled")
previousText.config(bg="tan")



#start button fame at bottom
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
overallAverageValue = ttk.Label(buttonframe,textvariable=overallAverageValueString,padding="15 15 50 15") 
overallAverageValue.config(font=('Helvetica',75,'bold'))
overallAverageValue.grid(row=0,column=5, sticky=(E,W))

downtimeButton = Button(buttonframe, text='Downtime', command=onClick)
downtimeButton.grid(row=0,column=6)
downtimeButton.config(font=('Helvetica',60,'bold'))
downtimeButton.config(bg=("light blue"))




fig = plt.figure(1)
canvas = FigureCanvasTkAgg(fig, master=root)
plot_widget = canvas.get_tk_widget()
canvas.get_tk_widget().place(x=1100, y=300)
graph = fig.add_subplot(111)
graph.set_xlabel('Date')
now = datetime.datetime.now()
global timeGraph
global jarGraph
a = []
b = []
timeGraph = deque(a)
jarGraph = deque(b)
plt.plot(timeGraph,jarGraph, 'k')
plt.xlabel('Time')
plt.ylabel('Made')
plt.title('Production')


root.title("Cycle Time") 
root.geometry('1900x1200')

def checkTime(): # used to check the time to see if it is time to reset the shifts ie 6:00 and 2:00(14:00 military time)
	global alreadyReset
	now = datetime.datetime.now()
	switchMinute = 0
	
	if now.minute == switchMinute and (now.hour==6 or now.hour==14) and alreadyReset == 0:
		resetShift()
		print("shift has been reset automatically!!!!!!!!!!! at ", str(now))
		alreadyReset = 1
	if (now.minute == switchMinute + 1) and (now.hour==6 or now.hour==14):	
		alreadyReset = 0
	root.after(1000, checkTime)
	
chk1 = check_button(currentCycleTime)
c1 = Thread(target=chk1.checkloop)
c1.start()
root.after(1000, checkTime)
root.mainloop()

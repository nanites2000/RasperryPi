import sqlite3
try:
	connection = sqlite3.connect("cycleTime.db",check_same_thread = False)
	cursor = connection.cursor()
except:
	print("Database Filed to Connect")
	
	
#this finds the production during the minute of 4:00pm-4:01pm	from yesterday
cursor.execute("SELECT * FROM autojarcycletimes WHERE date('now', '-1 day') = date(datetime) and strftime('%H:%M',datetime) = '16:00'")
print("fetchall:")
result = cursor.fetchall()
for r in result:
    print(r)


#this finds the average daily cycletime for the last 13 days and returns it
for i in range (0,13):
	statement = ("SELECT date(datetime),avg(cycleTime) FROM autojarcycletimes WHERE date('now', '-"+ str(i) +" day') = date(datetime)")
	cursor.execute(statement)
	print("fetchall last 13 days:")
	result = cursor.fetchall()
	for r in result:
		print(r)
		
#this finds the average daily cycletime for the last 20 days and returns it

statement = ("SELECT date(datetime),avg(cycleTime) FROM autojarcycletimes WHERE date(datetime) <= date('now') AND date(datetime) >= date('now', '-20 day') GROUP BY date(datetime);")
cursor.execute(statement)
print("fetchall last 20 days:")
result = cursor.fetchall()
for r in result:
	print(r)	
		
		
		
		
#this finds the average daily cycletime for all the days 

statement = ("SELECT date(datetime),avg(cycleTime) FROM autojarcycletimes GROUP BY date(datetime)")
cursor.execute(statement)
print("fetchall:")
result = cursor.fetchall()
for r in result:
	print(r)
	
		
		

		
#this finds all cycle times that are longer than 3 seconds and groups them by day they happened
statement = "SELECT date(datetime),count(cycleTime),sum(cycleTime) FROM autojarcycletimes WHERE cycleTime > 3 GROUP BY date(datetime)"
cursor.execute(statement)
print("fetchall:")
result = cursor.fetchall()
for r in result:
	print(r)
	
	
#this finds the average monthly cycletime for all the months 

statement = ("SELECT strftime('%m', datetime) as valMonth, avg(cycleTime) as totalCycleMonth FROM autojarcycletimes GROUP BY valMonth")
cursor.execute(statement)
print("fetchall month sums:")
result = cursor.fetchall()
for r in result:
	print(r)			


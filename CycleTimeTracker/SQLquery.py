
import sqlite3

try:
	connection = sqlite3.connect("cycleTime.db",check_same_thread = False)
	cursor = connection.cursor()
except:
	print("Database Filed to Connect")
	
'''	
#this finds the production during the minute of 4:00pm-4:01pm	from yesterday
cursor.execute("SELECT * FROM cycletimes WHERE date('now', '-1 day') = date(datetime) and strftime('%H:%M',datetime) = '16:00'")
print("fetchall:")
result = cursor.fetchall()
for r in result:
    print(r)


#this finds the average daily cycletime for the last 13 days and returns it
for i in range (0,13):
	statement = ("SELECT date(datetime),avg(cycleTime) FROM cycletimes WHERE date('now', '-"+ str(i) +" day') = date(datetime)")
	cursor.execute(statement)
	print("fetchall last 13 days:")
	result = cursor.fetchall()
	for r in result:
		print(r)
		
#this finds the average daily cycletime for the last 20 days and returns it

statement = ("SELECT date(datetime),avg(cycleTime) FROM cycletimes WHERE date(datetime) <= date('now') AND date(datetime) >= date('now', '-20 day') GROUP BY date(datetime);")
cursor.execute(statement)
print("fetchall last 20 days:")
result = cursor.fetchall()
for r in result:
	print(r)	
		
		
		
		
#this finds the average daily cycletime for all the days 

statement = ("SELECT date(datetime),avg(cycleTime) FROM cycletimes GROUP BY date(datetime)")
cursor.execute(statement)
print("fetchall:")
result = cursor.fetchall()
for r in result:
	print(r)
	
		
		

		
#this finds all cycle times that are longer than 3 seconds and groups them by day they happened
statement = "SELECT date(datetime),count(cycleTime),sum(cycleTime) FROM cycletimes WHERE cycleTime > 3 GROUP BY date(datetime)"
cursor.execute(statement)
print("fetchall:")
result = cursor.fetchall()
for r in result:
	print(r)
	
	
#this finds the average monthly cycletime for all the months 

statement = ("SELECT strftime('%m', datetime) as valMonth, avg(cycleTime) as totalCycleMonth FROM cycletimes GROUP BY valMonth")
cursor.execute(statement)
print("fetchall month sums:")
result = cursor.fetchall()
for r in result:
	print(r)		
'''


print("1st Shift production last 40 days")
#look at all production by date for each shift
statement = "SELECT date(datetime),count(cycleTime) FROM cycletimes where time(datetime) BETWEEN '06:00:00' and '14:00:00' AND date(datetime) >=date('now', '-40 day')GROUP BY date(datetime) "
cursor.execute(statement)
result = cursor.fetchall()
for r in result:
	print(r)
	
	
	
print("2nd Shift production last 40 days")	
#look at all production by date for each shift
statement = "SELECT date(datetime),count(cycleTime) as alias  FROM cycletimes where time(datetime) BETWEEN '14:00:00' and '22:00:00' AND date(datetime) >=date('now', '-40 day')GROUP BY date(datetime) "
cursor.execute(statement)
result = cursor.fetchall()
for r in result:
	print(r)

print("1st Shift average cycle time last 40 days")
#look at all production by date for each shift
statement = "select avg(average) from(SELECT avg(cycleTime)as average FROM cycletimes where time(datetime) BETWEEN '06:00:00' and '14:00:00' AND date(datetime) >=date('now', '-40 day') and cycleTime < 300 GROUP BY date(datetime)) "
cursor.execute(statement)
result = cursor.fetchall()
for r in result:
	print(r)
	
print("2nd Shift average cycle time last 40 days")
#look at all production by date for each shift
statement = "select avg(average) from(SELECT avg(cycleTime)as average FROM cycletimes where time(datetime) BETWEEN '14:00:00' and '22:00:00' AND date(datetime) >=date('now', '-40 day') AND cycleTime <300 GROUP BY date(datetime)) "
cursor.execute(statement)
result = cursor.fetchall()
for r in result:
	print(r)
	

"""
print("1st Shift last 40 days")
#look at all production by date for each shift
statement = '''
select first.date as date,first.count,second.count
from 
(SELECT date(datetime) as date,count(cycleTime) as count 
FROM cycletimes 
where time(datetime) BETWEEN '06:00:00' and '14:00:00' AND date(datetime) >=date('now', '-40 day')
GROUP BY date(datetime)
) as first
LEFT JOIN
(SELECT date(datetime) as date,count(cycleTime) as count 
FROM cycletimes 
where time(datetime) BETWEEN '14:00:00' and '22:00:00' AND date(datetime) >=date('now', '-40 day')
GROUP BY date(datetime)
) as second
on first.date=second.date 

UNION 

select second.date as date,first.count,second.count
from 
(SELECT date(datetime) as date,count(cycleTime) as count 
FROM cycletimes 
where time(datetime) BETWEEN '14:00:00' and '22:00:00' AND date(datetime) >=date('now', '-40 day')
GROUP BY date(datetime)
) as second
LEFT JOIN
(SELECT date(datetime) as date,count(cycleTime) as count 
FROM cycletimes 
where time(datetime) BETWEEN '6:00:00' and '14:00:00' AND date(datetime) >=date('now', '-40 day')
GROUP BY date(datetime)
) as first
on first.date = second.date



 '''
cursor.execute(statement)
result = cursor.fetchall()
for r in result:
	print(r)	
	
	
	
print("why Shift last 40 days")
#look at all production by date for each shift
statement = '''
select date
from 
(SELECT date(datetime) as date,count(cycleTime) as count 
FROM cycletimes 
where time(datetime) BETWEEN '14:00:00' and '22:00:00' AND date(datetime) >=date('now', '-40 day')
GROUP BY date(datetime)
)'''
#where date(second.date) in 
#("SELECT date(datetime) FROM cycletimes where time(datetime) BETWEEN '06:00:00' and '14:00:00' AND date(datetime) >=date('now', '-40 day')GROUP BY date(datetime) "
#) 


'''
#statement= "select * from (SELECT date(datetime) as date,count(cycleTime) as count FROM cycletimes where time(datetime) BETWEEN '14:00:00' and '22:00:00' AND date(datetime) >=date('now', '-40 day') GROUP BY date(datetime))"
cursor.execute(statement)
result = cursor.fetchall()
for r in result:
	print(r)	
	
	
print("sub query")
#look at all production by date for each shift
statement = '''
SELECT date(datetime) 
FROM cycletimes 
where time(datetime) BETWEEN '6:00:00' and '14:00:00' AND date(datetime) >=date('now', '-40 day')
GROUP BY date(datetime)
 '''
statement = "SELECT date(datetime) FROM cycletimes where time(datetime) BETWEEN '06:00:00' and '14:00:00' AND date(datetime) >=date('now', '-40 day')GROUP BY date(datetime) "
cursor.execute(statement)
result = cursor.fetchall()
for r in result:
	print(r)		
	

	

print("Both Shifts")	
#look at all production by date for each shift
statement = "SELECT date(datetime), count((select cycleTime from cycletimes where time(datetime) BETWEEN '06:00:00' and '14:00:00 group by date(datetime)')) from cycletimes group by date(datetime)"
cursor.execute(statement)
result = cursor.fetchall()
for r in result:
	print(r)	

print("Both Shifts")	
#look at all production by date for each shift
statement = "select date(datetime), (select count(date(datetime)) from cycletimes where time(datetime) BETWEEN '06:00:00' and '14:00:00' group by date(datetime)) first from cycletimes  group by date(datetime) "
cursor.execute(statement)
result = cursor.fetchall()
for r in result:
	print(r)	



print("Both Shifts")	
#look at all production by date for each shift
statement = "select count(date(datetime)) from cycletimes where time(datetime) BETWEEN '06:00:00' and '14:00:00' group by date(datetime) "
cursor.execute(statement)
result = cursor.fetchall()
for r in result:
	print(r)	"""

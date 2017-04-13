from lxml import html
from collections import namedtuple
import requests
import numpy as np

timetable = [["" for x in range(12)] for y in range(5)]

Component = namedtuple("Component", "course type day startTime endTime multiplicity")

def getHour(s, change):
	hour = int(s[0:s.find(":")]) % 12
	# print  (hour + 4 + change) % 12
	if "pm" in s:
		hour += 12
	return  hour

def getDay(s):
	if s == "Monday":
		return 0
	if s == "Tuesday":
		return 1
	if s == "Wednesday":
		return 2
	if s == "Thursday":
		return 3
	if s == "Friday":
		return 4

def fillTimetable(s, course):
	# print s[2] + s[3] + s[4]
	lecDay    		= getDay(str(s[2]))
	lecStartInd  	= getHour(str(s[3]),  0) - 8  
	lecFinishInd 	= getHour(str(s[4]), -1) - 8
	free = True
	for i in range(lecStartInd, lecFinishInd):
		# print i, lecStartInd, lecFinishInd
		# print timetable[lecDay, i]
		if timetable[lecDay,i] != 0:
			free = False
	if free == True:
		for i in range(lecStartInd, lecFinishInd):
			timetable[lecDay, i] = course

def scrapeInfo(courses):
	coursesComp = []
	courseNum = 0
	for course in courses:
		courseNum += 1
		page = requests.get("https://spprd.newcastle.edu.au/Scientia/sws2017prd/reports/list.aspx?objects="+course+"/S1_CA&weeks=1-29&days=1-7;1;2;3;4;5;6;7&periods=1-30;1;2;3;4;5;6;7;8;9;10;11;12;13;14;15;16;17;18;19;20;21;22;23;24;25;26;27;28;29;30&template=module_list")
		tree = html.fromstring(page.content)
		rows = [None]
		i = 0
		numLec = 1
		numCompLab = 1
		numLab = 1
		numTut = 1
		numWor = 1
		numExam = 1
		compList = []
		while len(rows) > 0:
			rows = tree.xpath('//*[@id="aspnetForm"]/div/table/tbody/tr[' + str(i+1) + ']/td/text()')
			if len(rows) > 0:
				typeString = rows[1].replace(".","")
				if  "Pass" not in typeString and "Exam" not in typeString:
					lecDay    = getDay(str(rows[2]))
					lecStart  = getHour(str(rows[3]),  0)  
					lecFinish = getHour(str(rows[4]), -1)
					tempComp = Component(course = courses[courseNum-1], type = typeString, day = rows[2], startTime = lecStart, endTime = lecFinish, multiplicity = 1)
					compList.append(tempComp)
			i += 1
		
		print ("{}:".format(course))
		for comp in compList:
			print ("\t{}: {}, {}-{}".format(comp.type, comp.day, comp.startTime, comp.endTime))
		coursesComp.append(compList)
		print "-------------------------"
	return coursesComp	

def typeGrouping(course, set, s):
	for comp in course:
		if comp.type == s:
			for i in range(comp.startTime - 8, comp.endTime - 8):
				print i
				element = timetable[getDay(comp.day)][i]
				if element is not "" and element.course == comp.course:
					element = Component(element.course, element.type, element.day, element.startTime, element.endTime, element.multiplicity + 1)
					print ("({}):{}, {}-{}, {} (x{})".format(i,  element.day, element.startTime, element.endTime, element.course, element.multiplicity))
				else:
					if timetable[getDay(comp.day)][i] is "":
						timetable[getDay(comp.day)][i] = comp
						print ("({}):{}, {}-{}, {} (x{})".format(i,  comp.day, comp.startTime, comp.endTime, comp.course, comp.multiplicity))
					else:
						print ("Major clash, abort!!" + "{}: {}-{}".format(comp.day, comp.startTime, comp.endTime))
	return 


courses = ["COMP2270", "ELEC4700", "SENG2130", "ENGG3500"]
compList = scrapeInfo(courses)

lecComp = []
tutComp = []
worComp = []
clComp  = []
labComp = []

for course in compList:
		typeGrouping(course, lecComp, "Lecture")
		typeGrouping(course, tutComp, "Tutorial")
		typeGrouping(course, worComp, "Workshop")
		typeGrouping(course, clComp,  "Computer Laboratory")
		typeGrouping(course, labComp, "Laboratory")
	

print lecComp
print tutComp
print worComp
print clComp
print labComp




#			 0	   1	 2	   3	 4
# 	        MON | TUE | WED | THU | FRI	
#		  ______|_____|_____|_____|____
#0)  8-9  |
#1)  9-10 |
#2)  10-11|
#3)  11-12|
#4)  12-13|
#5)  13-14|
#6)  14-15|
#7)  15-16|
#8)  16-17|
#9)  17-18|
#10) 18-19|
#11) 19-20|

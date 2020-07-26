import os 
import collections
import sys
import random as r

import matplotlib.pyplot as plt

# testBranch test


# This is the testBranch02 modification

def capName( inName ):
    returnName = ""
    splitter = ""
    if cntyName.find('-') >= 0:
        splitter = '-'
    elif cntyName.find(' ') >= 0:
        splitter = ' '

    if splitter != "":
        nameSplit = inName.split( splitter )
        delimiter = ''
        name = ''
        for word in nameSplit:
            capWord = word.capitalize()
            name = name + delimiter + capWord
            delimiter = splitter
        returnName = name
    else:
        returnName = inName.capitalize()

    return returnName

if len(sys.argv) != 3:
    print("usage: covidPlot.py <county name> <state name>")
    exit()

cntyName = str(sys.argv[1])
stateAbbrev = str(sys.argv[2])

delimiter = ''
title = ''

cntyName = capName(cntyName)
stateAbbrev = capName(stateAbbrev)
cntyStateName = cntyName + stateAbbrev

#  Pull the updated data
os.chdir( "data")

if os.path.isdir("covid-19-data") and os.path.isdir("covid-19-data/.git"):
    print( "performing pull")
    os.system( "git pull") 
else:
    #  Otiginal git fetch is missing so clone the data
    print("performing clone")
    os.system("git clone https://github.com/nytimes/covid-19-data.git")

os.chdir (".." )
os.system (" cp data/covid-19-data/us-counties.csv ." )

#  Strip out the desired county data
stateLength = len(stateAbbrev)
awkCmd= "awk -F\",\" '{ if( $2==\"" + cntyName +"\" && substr($3,1," + str(stateLength) + ")==\"" + stateAbbrev +"\") print $1\"~\"$2\"~\"$3\"~\"$5\"~\"$6 }' us-counties.csv > \"" + cntyStateName + ".strip\""
#print( awkCmd )
os.system( awkCmd ) 
os.remove("us-counties.csv")
fleName = cntyStateName + ".strip"
#print ("file name -->", fleName)
inputFile = open(fleName,"r")
lines = inputFile.readlines()
inputFile.close()
#print(len(lines))
stateName = ""
totalRows = 0
dates = []
cases = []
totalCases = []
totalDays = []
totalTicks = []
tickLabels = []
data = []
dayDate = ""
monDate = ""
oldMonth = ""
dataCases = 0
oldCases = 0
minNewCases = 0
maxNewCases = 0

oldMonth = ""
startDay = ""
tickValue  = 0
for line in lines:
    splitLine = line.split('~')
    # Get the month
    monDate = splitLine[0].split("-")[1]
    dayDate = splitLine[0].split("-")[2]
    stateName = splitLine[2]
    dataCases = int(splitLine[3])
    newCases = dataCases - oldCases
    if newCases > maxNewCases:
        maxNewCases = newCases
    oldCases = dataCases
    
    totalRows += 1
    data.append( [monDate, dayDate, newCases] )
    totalDate = monDate + "-" + dayDate
    totalDays.append(totalDate)
    totalCases.append( newCases)
    totalTicks.append(tickValue)
    if oldMonth != monDate or (dayDate == "15" and totalRows > 15) :
        tickLabel = monDate + "/" + dayDate
        oldMonth = monDate
        tickLabels.append( tickLabel )
    else:
        tickLabels.append("")
    tickValue += 1

# put the last date on if it is greater than the 20th of a month
popDays = int(dayDate) - 15
#print(popDays)
if popDays > 0 and popDays < 6:
    for i in range(0, popDays+1):
        tickLabels.pop()
    for i in range(0, popDays+1):
        tickLabels.append("")

tickLabels.pop()
tickLabel = monDate + "/" + dayDate
tickLabels.append( tickLabel )


plt.plot(totalDays, totalCases)
plt.xticks(ticks = totalTicks ,labels=tickLabels)

title = cntyName + " County, " + stateName + " New Covid-19 Cases (Month/Day)\n" + "source: https://github.com/nytimes/covid-19-data"
plt.title(title)

xLabel = "Date"
plt.ylim(0, maxNewCases + 5)
plt.xlabel(xLabel)
plt.ylabel("new cases")
plt.show()
os.remove(fleName)


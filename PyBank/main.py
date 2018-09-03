##U of A Data Analytics Bootcamp Python homework
#By Dustin Rice     9/3/2018
#PyBank / main.py

import os
import csv

#declare variables
#I ended up using a dictionary so I didn't have to declare global variables all the time
FinAn = {
    "Months" : int(0), #Total number of months cycled through
    "netProf" : float(0), #Net profit so far
    "cTotal" : float(0), #Total Change
    "cAve" : 0.0, #Average change - I regret making the variable look like "cave" but I'm not changing it now
    "IncMonth" : "", #Name of month with greatest increase/change above 0
    'IncVal' : 0.0, #Greatest increase value
    "DecMonth" : "", #Name of month with greatest decrease/change below 0
    "DecVal" : 0.0, #Greatest decrease value
    "LastMonth" : [] #Stores data for comparison
}

##utput will later save the lines of the analysis as a string.
OutPut = []

def NextMonth(ThisMonth): #Iterates through profit, month, and prepares data for next month's comparison
    #Add the profit up
    FinAn['netProf'] += float(ThisMonth[1])
    #Add the total months up
    FinAn['Months'] +=1
    #This month is now last month - stored for comparison
    FinAn['LastMonth'] = ThisMonth

#Compares the profit from this month to last month
def CompareProfit(ThisMonth,LastMonth):
    change = float(ThisMonth[1]) - float(LastMonth[1])
    FinAn['cTotal'] += change

    #Checks the total change between this month and last,
    if change > FinAn['IncVal']:    #replaces the highest increase if it beats the previous record
        FinAn['IncVal'] = change
        FinAn['IncMonth'] = ThisMonth[0]
    elif change < FinAn['DecVal']:    #replaces the greatest decrease if this decrease is bigger than the record
        FinAn['DecVal'] = change
        FinAn['DecMonth'] = ThisMonth[0]

def PrepAnalysis():  #Puts the Analysis into a string for each line so it can be printed or put in a text file
    Out = []
    Out.append("Financial Analysis: ")
    Out.append("-----------------------------------------------------")
    Out.append(f"Total Months: {FinAn['Months']}")
    Out.append(f"Average Change: ${FinAn['cAve']}")
    Out.append(f"Greatest Increase in Profits: {FinAn['IncMonth']} (${FinAn['IncVal']})")
    Out.append(f"Greatest Decrease in Profits: {FinAn['DecMonth']} (${FinAn['DecVal']})")
    return Out

#find the input file
input_path = os.path.join('..', 'PyBank_Resources', 'budget_data.csv')

#open the input file
with open(input_path, 'r', newline = '') as csvfile:
    csvreader = csv.reader(csvfile, delimiter = ',')
    #skip the header
    next(csvreader, None)

    #The foor loop will total AND compare with previous months
    #First month can't be compared, so we total it BEFORE the for loop
    NextMonth(next(csvreader))

    #loop through data
    for row in csvreader:
        CompareProfit(row,FinAn['LastMonth']) #Compares profits for average, greatest change, etc.
        NextMonth(row) #increments profit and month totals, stores this month for next comparison
        #CompareProfit MUST go before NextMonth or else you're comparing this month to itself

    #Calculate the average AFTER the loop to avoid extra calculations
    FinAn["cAve"] = FinAn["cTotal"] / (FinAn['Months'] -1)   #Months -1 because the first month isn't compared
    OutPut = PrepAnalysis()  #crams the printed analysis into a list
    for i in OutPut: #each entry of the list is printed as a line
        print(i)

#writes the analysis made in PrepAnalysis and stored in list OutPut to a text file.
with open("analysis.txt", "w") as txtfile:
    for i in OutPut:
        txtfile.write(str(i) + '\n')

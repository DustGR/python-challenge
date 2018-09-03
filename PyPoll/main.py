import os
import csv

VT = {} #Vote Tally dictionary,  candidate : votes
TotalVotes = 0
Report = [] #lines of results report will be stored here later
input_path = os.path.join('..', 'PyPoll_Resources', 'election_data.csv')
Candidate = ''

def PrepReport(Data): #Takes the data and puts lines of report into a list
    Out = []
    wincount = 0
    for cand in Data: #Check vote count of each candidate to determine winner
        if Data[cand]['Votes'] > wincount:
            winner = cand
            wincount = VT[cand]['Votes']
        elif Data[cand]['Votes'] == wincount:
            winner = "Tie!"
    Out.append("Election Results")
    Out.append("------------------------")
    Out.append(f"Total Votes: {TotalVotes}")
    Out.append("------------------------")
    for cand in Data:
        Out.append(f"{str(cand)}: {Data[cand]['%']}%  ({Data[cand]['Votes']})")
    Out.append("------------------------")

    Out.append(f"Winner: {winner}")
    Out.append("------------------------")
    return Out


with open(input_path, 'r', newline = '') as csvfile:
    csvreader = csv.reader(csvfile, delimiter = ',')
    #skip the header
    next(csvreader, None)

    # limit = int(input("How far to tally?  ")) #for testing
    for row in csvreader:
        Candidate = row[2]
        #increment total of all votes
        TotalVotes += 1
        #Check the dictionary for the candidate's key
        if Candidate in VT:         #increment the candidate's key
            VT[Candidate]['Votes'] += 1
        else: #If they're new, this is their first vote
            VT[Candidate] = {'Votes' : 1, '%' : 0}
    for i in VT:
        VT[i]['%'] = round(((VT[i]['Votes'] / TotalVotes) * 100), 3)

    Report = PrepReport(VT)
    for row in Report:
        print(row)

with open("results.txt", "w") as txtfile:
    for row in Report:
        txtfile.write(str(row) + '\n')

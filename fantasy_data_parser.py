class Player:
	def __init__(self,name,rnd):
		self.name = name
		self.rnd_picked = rnd
		self.isDrafted = True 
		if rnd == 0: #use 0 for undrafted players
			self.isDrafted = False
	
	def keeperCost(self):
		cost = 0
		if self.isDrafted:
			cost = self.rnd_picked - 3
		else:
			cost = 17
			
		#if the cost is less than 1, then make it 0
		if cost < 1:
			cost = 0
		return(cost)
		
def removeSpecialChars(inputText):
	outText = ""
	for iChar in inputText:
		if (iChar.isalpha()) or (iChar == " ") or (iChar == ".") or (iChar == "-") or (iChar == "'"):
			#need additional check for latin character that represents a keeper
			if (ord(iChar) != 238):
				outText = outText + iChar
			#if ord(iChar)> 122:
				#print(f"{iChar} {ord(iChar)} {inputText}")
	return(outText.strip())

def getPickNo(pickText,rnd):
	#remove the '.' if there
	pickNo = int(pickText.rstrip(". "))
	#swap the pick number if it's an even round
	if (rnd%2 == 0):
		pickNo = 13 - pickNo
	return(pickNo - 1)
		
def readDraft():
	#this routine will take in the draft results that are copied and pasted to file
	#and create a parsed draft file with players separated by tabs
	#the input file and output file names are currently hard-coded
	draftDict = dict()
	#initialize list to hold players of each round
	players = []
	for iPlayer in range(12):
		players.append("")
	currentRound = 0
	draftFile = open("draft_results_2025.txt",'r')
	rawdata = draftFile.readlines()
	draftFile.close()
	parsedDraft = open("parsed_drafted_2025.txt",'w')
	for line in rawdata:
		#check for blank line
		if (line.strip() == ""):
			continue
		if (line.find("Round") > -1):
			currentRound = int((line.split())[1])
			if currentRound > 1:
				parsedDraft.write('\n')
		else:
			splitline = line.split('\t')
			pickNo = getPickNo(splitline[0],currentRound)
			fullPlayerName = parsePlayerLine(splitline[1])
			playerName = removeSuffix(fullPlayerName)
			print(f"{playerName}")
			players[pickNo] = playerName
			#create the player object and add it to the draft dictionary
			currentPlayer = Player(playerName,currentRound)
			draftDict[playerName] = currentPlayer
			#if this was the last pick of the round, then write them all out
			#it is the last pick if "12" is in the text
			if (splitline[0].find("12") > -1):
				for iPlayer in players:
					parsedDraft.write(f"{iPlayer}" + '\t')
	parsedDraft.close()
	for iP in draftDict:
		print(f"{draftDict[iP].name} {draftDict[iP].rnd_picked}")
	return(draftDict)

def removeSuffix(fullName):
	noSuffix = fullName
	if fullName.find("Sr.") > -1:
		noSuffix = fullName.replace("Sr.","")
	elif fullName.find("Sr") > -1:
		noSuffix = fullName.replace("Sr","")
	elif fullName.find("Jr.") > -1:
		noSuffix = fullName.replace("Jr.","")
	elif fullName.find("Jr") > -1:
		noSuffix = fullName.replace("Jr","")

	return(noSuffix)

def parsePlayerLine(playerLine):
	#this routine will parse the line and only spit back the player's name
	#this may change from year to year.  In 2023, the player's names were all that was there
	#the 2024 draft results included team and position which needs to be removed
	#the Jr and Sr suffix is also removed now - may have to revisit this later
	
	#as of 2024, we need to remove the team name and position in quotes
	beginParen = playerLine.find("(")
	endParen = playerLine.find(")")
	removedPositionAndTeam = playerLine.replace(playerLine[beginParen:endParen+1],"")
	removedSuffix = removeSuffix(removedPositionAndTeam)
	playerName = removeSpecialChars(removedSuffix)
	return(playerName)
 	
def parseRawRoster(draft_results):
	#this routine reads the FINAL rosters from the year and assigns the players
	#to a dictionary of teams.
	#Most likely, year to year, this routine will have to adjust for special characters
	teams = dict()
	#set flag that signals that the next read is the team name
	gettingTeam = False
	gettingPlayers = False
	gotPosition = False
	currentTeam = ""
	rawRoster = open("final_rosters_2025.txt",'r')
	allLines = rawRoster.readlines()
	rawRoster.close()
	for iLine in allLines:
		#check for special characters introduced in 2025
		if (iLine.strip() == "î€¾"):
			continue
		print(f"Line is: {iLine}({len(iLine)})")
		#for iChar in iLine:
		#	print(f"{iChar}")
		#if team flag is set, then next read is the team name
		if (gettingTeam):
			currentTeam = iLine.strip()
			gettingTeam = False
			print(f"Current team is {currentTeam}")
			teams[currentTeam] = list()
			print(currentTeam)
		#if blank line, then next line is the team name
		if iLine.strip() == "":
			gettingTeam = True
			gettingPlayers = False 
		#if the word "Player" is in the line, then we are getting the players
		if iLine.find("Player") > -1:
			#set the flag that we are aquiring players for the current team
			gettingPlayers = True
			continue
		if iLine.find("Final") == 0:
			#just skip this line and continue
			continue
		if (gettingPlayers):
			if (gotPosition):
				#next should be the player's name unless it's "Empty"
				if iLine.find("Empty")< 0:
					cleanName = parsePlayerLine(iLine)
					if (cleanName in draft_results):
						rnd_picked = draft_results[cleanName].rnd_picked
						#add the player to the team's list
						print(f"Current team is {currentTeam}")
						teams[currentTeam].append(draft_results[cleanName])
						print(f"\t{cleanName} {rnd_picked}")
					else:
						print(f"Adding {cleanName} to {currentTeam}")
						#create a new player and add to the team's list
						rnd_picked = 0
						newPlayer = Player(cleanName,rnd_picked)
						teams[currentTeam].append(newPlayer)
						print(f"\t{cleanName} undrafted")
				gotPosition = False
			else:
				gotPosition = True
	return(teams)
		
		
		
				
def removeBlankLines(fileName,outfileName):
	import os
	os.chdir("/psd37/linux/home/dearly/Personal/Fantasy");
	input = open(fileName,'r');
	rawdata = input.readlines();
	input.close();

	output = open(outfileName,'w')
	playerLine = ""
	iPlayer = 0
	for iLine in rawdata:
		if iLine != "\n":
			player = iLine.replace('\n','')
			playerLine = playerLine + "   " + player
			if iPlayer%5 == 0:
				output.write(playerLine + "\n");
				playerLine = ""
		iPlayer = iPlayer + 1
	output.close();	
	return;	

def parseRawNamesAndPos(fileName,outfileName):
	import os
	os.chdir("/psd37/linux/home/dearly/Personal/Fantasy");
	input = open(fileName,'r');
	rawdata = input.readlines();
	input.close();

	output = open(outfileName,'w')
	playerLine = ""
	iLine = 0
	iPlayer = 1
	for line in rawdata:
		line = line.lstrip();
		if iLine == 0:
			player = line.replace('\n','')
		if iLine == 2:
			position = line.replace('\n','')
			playerPosition = "%d. %s%s\n" % (iPlayer,player,position)
			output.write(playerPosition)
			##print playerPosition
			iPlayer = iPlayer + 1
		if line != "NA\n":	
			iLine = iLine + 1
		if iLine == 6:
			iLine = 0
	output.close();	
	return;	

def createSchedule_before_2014(fileName,outfileName):
	#Read in the team order
	import os
	os.chdir("/psd37/linux/home/dearly/Personal/Fantasy");
	input = open(fileName,'r');
	rawdata = input.readlines();
	input.close();
	
	team = list()
	weekSched = ["1","2","3","4","5","6"]
	games = list()
	for iWeek in range(11):
		games.append(weekSched)
		games.append(["1","2","3","4","5","6"])
	#print(games[0])
	#print(games[10])	
	
	for iTeam in rawdata:
		teamName = iTeam.replace("\n","")
		team.append(teamName)
		#print teamName
		

	#Week 1
	week = 0
	games[week][0] = "%s vs %s" % (team[1],team[2])
	games[week][1] = "%s vs %s" % (team[3],team[4])
	games[week][2] = "%s vs %s" % (team[5],team[6])
	games[week][3] = "%s vs %s" % (team[7],team[8])
	games[week][4] = "%s vs %s" % (team[9],team[10])
	games[week][5] = "%s vs %s" % (team[11],team[12])
	#print "\nWeek %d" % (week)
	#print games[week][0]
	#print games[week][1]
	#print games[week][2]
	#print games[week][3]
	#print games[week][4]
	#print games[week][5]

	#Week 2
	week = week + 1
	#print "\nWeek %d" % (week)
	games[week][0] = "%s vs %s" % (team[1],team[7])
	games[week][1] = "%s vs %s" % (team[2],team[8])
	games[week][2] = "%s vs %s" % (team[3],team[9])
	games[week][3] = "%s vs %s" % (team[4],team[10])
	games[week][4] = "%s vs %s" % (team[5],team[11])
	games[week][5] = "%s vs %s" % (team[6],team[12])
	#print games[week][0]
	#print games[week][1]
	#print games[week][2]
	#print games[week][3]
	#print games[week][4]
	#print games[week][5]

	#Week 3
	week = week + 1
	#print "\nWeek %d" % (week)
	games[week][0] = "%s vs %s" % (team[1],team[3])
	games[week][1] = "%s vs %s" % (team[2],team[5])
	games[week][2] = "%s vs %s" % (team[4],team[6])
	games[week][3] = "%s vs %s" % (team[7],team[9])
	games[week][4] = "%s vs %s" % (team[10],team[11])
	games[week][5] = "%s vs %s" % (team[8],team[12])
	#print games[week][0]
	#print games[week][1]
	#print games[week][2]
	#print games[week][3]
	#print games[week][4]
	#print games[week][5]

	#Week 4
	week = week + 1
	#print "\nWeek %d" % (week)
	games[week][0] = "%s vs %s" % (team[1],team[8])
	games[week][1] = "%s vs %s" % (team[2],team[9])
	games[week][2] = "%s vs %s" % (team[3],team[10])
	games[week][3] = "%s vs %s" % (team[4],team[11])
	games[week][4] = "%s vs %s" % (team[5],team[12])
	games[week][5] = "%s vs %s" % (team[6],team[7])
	#print games[week][0]
	#print games[week][1]
	#print games[week][2]
	#print games[week][3]
	#print games[week][4]
	#print games[week][5]

	#Week 5
	week = week + 1
	#print "\nWeek %d" % (week)
	games[week][0] = "%s vs %s" % (team[1],team[4])
	games[week][1] = "%s vs %s" % (team[2],team[6])
	games[week][2] = "%s vs %s" % (team[3],team[5])
	games[week][3] = "%s vs %s" % (team[7],team[10])
	games[week][4] = "%s vs %s" % (team[8],team[11])
	games[week][5] = "%s vs %s" % (team[9],team[12])
	#print games[week][0]
	#print games[week][1]
	#print games[week][2]
	#print games[week][3]
	#print games[week][4]
	#print games[week][5]

	#Week 6
	week = week + 1
	#print "\nWeek %d" % (week)
	games[week][0] = "%s vs %s" % (team[1],team[9])
	games[week][1] = "%s vs %s" % (team[2],team[10])
	games[week][2] = "%s vs %s" % (team[6],team[8])
	games[week][3] = "%s vs %s" % (team[4],team[12])
	games[week][4] = "%s vs %s" % (team[5],team[7])
	games[week][5] = "%s vs %s" % (team[3],team[11])
	#print games[week][0]
	#print games[week][1]
	#print games[week][2]
	#print games[week][3]
	#print games[week][4]
	#print games[week][5]

	#Week 7
	week = week + 1
	#print "\nWeek %d" % (week)
	games[week][0] = "%s vs %s" % (team[1],team[5])
	games[week][1] = "%s vs %s" % (team[2],team[4])
	games[week][2] = "%s vs %s" % (team[3],team[6])
	games[week][3] = "%s vs %s" % (team[8],team[10])
	games[week][4] = "%s vs %s" % (team[9],team[11])
	games[week][5] = "%s vs %s" % (team[7],team[12])
	#print games[week][0]
	#print games[week][1]
	#print games[week][2]
	#print games[week][3]
	#print games[week][4]
	#print games[week][5]

	#Week 8
	week = week + 1
	#print "\nWeek %d" % (week)
	games[week][0] = "%s vs %s" % (team[1],team[10])
	games[week][1] = "%s vs %s" % (team[2],team[11])
	games[week][2] = "%s vs %s" % (team[3],team[12])
	games[week][3] = "%s vs %s" % (team[4],team[7])
	games[week][4] = "%s vs %s" % (team[5],team[8])
	games[week][5] = "%s vs %s" % (team[6],team[9])
	#print games[week][0]
	#print games[week][1]
	#print games[week][2]
	#print games[week][3]
	#print games[week][4]
	#print games[week][5]

	#Week 9
	week = week + 1
	#print "\nWeek %d" % (week)
	games[week][0] = "%s vs %s" % (team[1],team[6])
	games[week][1] = "%s vs %s" % (team[2],team[3])
	games[week][2] = "%s vs %s" % (team[4],team[5])
	games[week][3] = "%s vs %s" % (team[7],team[11])
	games[week][4] = "%s vs %s" % (team[8],team[9])
	games[week][5] = "%s vs %s" % (team[10],team[12])
	#print games[week][0]
	#print games[week][1]
	#print games[week][2]
	#print games[week][3]
	#print games[week][4]
	#print games[week][5]

	#Week 10
	week = week + 1
	#print "\nWeek %d" % (week)
	games[week][0] = "%s vs %s" % (team[1],team[12])
	games[week][1] = "%s vs %s" % (team[2],team[7])
	games[week][2] = "%s vs %s" % (team[3],team[8])
	games[week][3] = "%s vs %s" % (team[4],team[9])
	games[week][4] = "%s vs %s" % (team[5],team[10])
	games[week][5] = "%s vs %s" % (team[6],team[11])
	#print games[week][0]
	#print games[week][1]
	#print games[week][2]
	#print games[week][3]
	#print games[week][4]
	#print games[week][5]

	#Week 11
	week = week + 1
	#print "\nWeek %d" % (week)
	games[week][0] = "%s vs %s" % (team[1],team[12])
	games[week][1] = "%s vs %s" % (team[2],team[7])
	games[week][2] = "%s vs %s" % (team[3],team[8])
	games[week][3] = "%s vs %s" % (team[4],team[9])
	games[week][4] = "%s vs %s" % (team[5],team[10])
	games[week][5] = "%s vs %s" % (team[6],team[11])
	#print games[week][0]
	#print games[week][1]
	#print games[week][2]
	#print games[week][3]
	#print games[week][4]
	#print games[week][5]

	#add the week 12 and 13 games by duplicating weeks 1 and 2
	#Week 12
	week = week + 1
	#print "\nWeek %d" % (week)
	games[week][0] = "%s vs %s" % (team[1],team[2])
	games[week][1] = "%s vs %s" % (team[3],team[4])
	games[week][2] = "%s vs %s" % (team[5],team[6])
	games[week][3] = "%s vs %s" % (team[7],team[8])
	games[week][4] = "%s vs %s" % (team[9],team[10])
	games[week][5] = "%s vs %s" % (team[11],team[12])
	#print games[week][0]
	#print games[week][1]
	#print games[week][2]
	#print games[week][3]
	#print games[week][4]
	#print games[week][5]

	#Week 13
	week = week + 1
	#print "\nWeek %d" % (week)
	games[week][0] = "%s vs %s" % (team[1],team[7])
	games[week][1] = "%s vs %s" % (team[2],team[8])
	games[week][2] = "%s vs %s" % (team[3],team[9])
	games[week][3] = "%s vs %s" % (team[4],team[10])
	games[week][4] = "%s vs %s" % (team[5],team[11])
	games[week][5] = "%s vs %s" % (team[6],team[12])
	#print games[week][0]
	#print games[week][1]
	#print games[week][2]
	#print games[week][3]
	#print games[week][4]
	#print games[week][5]

	##print games
	##print games[0]
	##print games[10]

	#games.append(games[1]);

	#write the data to screen
	#for iWeek in range(13):
		##print "\nWeek %d:" % (iWeek+1)
		#for iGame in range(6):
			##print "%d. %s" % (iGame+1, games[iWeek][iGame])

def makeWeek(team,games,week,weekOrder):
	games[week][0] = "%s vs %s" % (team[weekOrder[0]],team[weekOrder[1]])
	games[week][1] = "%s vs %s" % (team[weekOrder[2]],team[weekOrder[3]])
	games[week][2] = "%s vs %s" % (team[weekOrder[4]],team[weekOrder[5]])
	games[week][3] = "%s vs %s" % (team[weekOrder[6]],team[weekOrder[7]])
	games[week][4] = "%s vs %s" % (team[weekOrder[8]],team[weekOrder[9]])
	games[week][5] = "%s vs %s" % (team[weekOrder[10]],team[weekOrder[11]])
	thisWeekGames = "Week %d\n" % (week+1)
	thisWeekGames = thisWeekGames + games[week][0] + "\n"
	thisWeekGames = thisWeekGames + games[week][1] + "\n"
	thisWeekGames = thisWeekGames + games[week][2] + "\n"
	thisWeekGames = thisWeekGames + games[week][3] + "\n"
	thisWeekGames = thisWeekGames + games[week][4] + "\n"
	thisWeekGames = thisWeekGames + games[week][5] + "\n\n"
	return thisWeekGames

def createSchedule(fileName,outfileName):
	#Read in the team order
	import os
	os.chdir("/psd37/linux/home/dearly/Personal/Fantasy");
	input = open(fileName,'r');
	rawdata = input.readlines();
	input.close();
	
	team = list()
	weekSched = ["1","2","3","4","5","6"]
	games = list()
	for iWeek in range(11):
		games.append(weekSched)
		games.append(["1","2","3","4","5","6"])
	
	for iTeam in rawdata:
		teamName = iTeam.replace("\n","")
		team.append(teamName)
		#print teamName
		

	outfile = open(outfileName,'w')

	#Week 1
	weekOrder = [1,2,3,4,5,6,7,8,9,10,11,12]
	week = 0
	scheduleText = makeWeek(team,games,week,weekOrder)
	outfile.write(scheduleText)

	#Week 2
	weekOrder = [1,7,2,8,3,9,4,10,5,11,6,12]
	week = 1
	scheduleText = makeWeek(team,games,week,weekOrder)
	outfile.write(scheduleText)


	#Week 3
	weekOrder = [1,3,2,5,4,6,7,9,8,11,10,12]
	week = 2
	scheduleText = makeWeek(team,games,week,weekOrder)
	outfile.write(scheduleText)


	#Week 4
	weekOrder = [1,8,2,9,3,10,4,11,5,12,6,7]
	week = 3
	scheduleText = makeWeek(team,games,week,weekOrder)
	outfile.write(scheduleText)


	#Week 5
	weekOrder = [1,4,2,6,3,5,7,10,8,12,9,11]
	week = 4
	scheduleText = makeWeek(team,games,week,weekOrder)
	outfile.write(scheduleText)


	#Week 6
	weekOrder = [1,9,2,10,3,11,4,12,5,7,6,8]
	week = 5
	scheduleText = makeWeek(team,games,week,weekOrder)
	outfile.write(scheduleText)


	#Week 7
	weekOrder = [1,5,2,4,3,6,7,11,8,10,9,12]
	week = 6
	scheduleText = makeWeek(team,games,week,weekOrder)
	outfile.write(scheduleText)


	#Week 8
	weekOrder = [1,10,2,11,3,12,4,7,5,8,6,9]
	week = 7
	scheduleText = makeWeek(team,games,week,weekOrder)
	outfile.write(scheduleText)


	#Week 9
	weekOrder = [1,6,2,3,4,5,7,12,8,9,10,11]
	week = 8
	scheduleText = makeWeek(team,games,week,weekOrder)
	outfile.write(scheduleText)


	#Week 10
	weekOrder = [1,11,2,12,3,7,4,8,5,9,6,10]
	week = 9
	scheduleText = makeWeek(team,games,week,weekOrder)
	outfile.write(scheduleText)


	#Week 11
	weekOrder = [1,12,2,7,3,8,4,9,5,10,6,11]
	week = 10
	scheduleText = makeWeek(team,games,week,weekOrder)
	outfile.write(scheduleText)


	#Week 12
	weekOrder = [1,2,3,4,5,6,7,8,9,10,11,12]
	week = 11
	scheduleText = makeWeek(team,games,week,weekOrder)
	outfile.write(scheduleText)


	#Week 13
	weekOrder = [1,7,2,8,3,9,4,10,5,11,6,12]	
	week = 12
	scheduleText = makeWeek(team,games,week,weekOrder)
	outfile.write(scheduleText)

	outfile.close()

def createScheduleFromTemplate(fileName,fileName2,outfileName):
	#Read in the team order
	import os
	os.chdir("/psd37/linux/home/dearly/Personal/Fantasy");
	input = open(fileName,'r');
	rawdata = input.readlines();
	input.close();
	
	team = list()
	weekSched = ["1","2","3","4","5","6"]
	games = list()
	for iWeek in range(11):
		games.append(weekSched)
		games.append(["1","2","3","4","5","6"])
	
	for iTeam in rawdata:
		teamName = iTeam.replace("\n","")
		team.append(teamName)
		#print teamName

	#Read in the entire template
	templateFile = open(fileName2,'r');
	template = templateFile.read();
	templateFile.close();

	template = template.replace("team12",team[12])
	template = template.replace("team11",team[11])
	template = template.replace("team10",team[10])
	template = template.replace("team9",team[9])
	template = template.replace("team8",team[8])
	template = template.replace("team7",team[7])
	template = template.replace("team6",team[6])
	template = template.replace("team5",team[5])
	template = template.replace("team4",team[4])
	template = template.replace("team3",team[3])
	template = template.replace("team2",team[2])
	template = template.replace("team1",team[1])		

	outfile = open(outfileName,'w')
	outfile.write(template);
	outfile.close();



	##print games
	##print games[0]
	##print games[10]

	#games.append(games[1]);

	#write the data to screen
	#for iWeek in range(13):
		##print "\nWeek %d:" % (iWeek+1)
		#for iGame in range(6):
			##print "%d. %s" % (iGame+1, games[iWeek][iGame])


if __name__ == "__main__":
	#inputDir = sys.argv[1]
	#outputDir = sys.argv[2]
	#command = sys.argv[3]
	#createSchedule("final_order_2012.txt","schedule_2014.txt")
	#createScheduleFromTemplate("final_order_2012.txt","schedule_template","schedule_2014.txt")
	#*********Note that the team names need to match in all files!***************************
	#Also remember to change "Video Forecast" to empty in the final rosters file
	#First line of final roster file should be blank
	draft_results = readDraft()
	#exit()
	fullTeams = parseRawRoster(draft_results)
	keepers = open("keepers_2026.txt",'w')
	for iTeam in fullTeams:
		print(f"{iTeam}")
		keepers.write(f"{iTeam}\n")
		for iPlayer in fullTeams[iTeam]:
			keeperVal = iPlayer.keeperCost()
			if keeperVal > 0:
				print(f"{iPlayer.name} {keeperVal}")
				keepers.write(f"{iPlayer.name} {keeperVal}")
				if iPlayer.isDrafted == False:
					keepers.write("(u)")
				keepers.write('\n')
		print('\n')
		keepers.write('\n')
	keepers.close()

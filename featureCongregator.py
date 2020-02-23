import os
import csv

battingPath = 'D:\\Baseball\\Database\\Batting\\'
metaPath = 'D:\\Baseball\\Database\\Meta\\'
pitchingPath = 'D:\\Baseball\\Database\\Pitching\\'
startingLineupsPath = 'D:\\Baseball\\Database\\startingLineups\\'
teamAndScoresPath = 'D:\\Baseball\\Database\\teamAndScores\\'
umpiresPath = 'D:\\Baseball\\Database\\Umpires\\'
weatherPath = 'D:\\Baseball\\Database\\Weather_Pass_2\\'
numberOfGamesToConsider = 20
homeAwayList = ['home', 'away']
dataDict = {}


def getFilesInPath(path):
    temp_file_names = []
    for r, d, f in os.walk(path):
        for file in f:
            if '.csv' in file:
                temp_file_names.append(file)
    return temp_file_names


def fixLoadingErrors(file_info):
    if(isinstance(file_info, list)):
        for x in range(0, len(file_info)):
            file_info[x] = fixLoadingErrors(file_info[x])
    else:
        if('\', ' in file_info):
            file_info = file_info.split(', ')
            if(len(file_info) == 0):
                return file_info
            for y in range(0, len(file_info)):
                if(len(file_info[y]) != 0):
                    file_info[y] = file_info[y].replace('[', '').strip()
                    file_info[y] = file_info[y].replace(']', '').strip()
                    file_info[y] = file_info[y].replace('\' ', '').strip()
                    file_info[y] = file_info[y].replace(' \'', '').strip()
                    file_info[y] = file_info[y].replace('\"', '').strip()
                    if('\'' in file_info[y]):
                        if(file_info[y][0] == '\''):
                            file_info[y] = file_info[y][1:]
                    if('\'' in file_info[y]):
                        if(file_info[y][len(file_info[y])-1] == '\''):
                            file_info[y] = file_info[y][:-1]

    return file_info


def extractData(base_path, file_names):
    file_info = []
    for x in file_names:
        with open(base_path+x, "r", newline='') as f:
            reader = csv.reader(f)
            file_info.append(list(reader))
    file_info = fixLoadingErrors(file_info)
    return file_info


def extractUID(gameURLString):
    gameURLString = gameURLString.split('/')
    if(len(gameURLString) == 0):
        return ''
    gameURLString2 = ""
    for section in gameURLString:
        if('.' in section):
            gameURLString2 = section.split('.')[0]
            break
    return gameURLString2


# Structure of data
# {
#     Game Title: {
#         Batting:[]
#         Pitching:[]
#         ...
#     }
# }

########################################################################
##########################Setting Up Data Structure#####################
teamAndScores_file_names = []
teamAndScores_file_names = getFilesInPath(teamAndScoresPath)
teamAndScoresRaw = extractData(
    teamAndScoresPath, teamAndScores_file_names[0:3])
for game in teamAndScoresRaw:
    gameUID = extractUID(game[0][0])
    dataDict[gameUID] = {}
    dataDict[gameUID]['teamAndScores'] = {}
    for homeAway in homeAwayList:
        dataDict[gameUID][homeAway] = {}
        dataDict[gameUID][homeAway]['batting'] = []
        dataDict[gameUID][homeAway]['pitching'] = []
        dataDict[gameUID][homeAway]['startingLineup'] = []
        dataDict[gameUID][homeAway]['general'] = {}
    dataDict[gameUID]['weather'] = {}
    dataDict[gameUID]['meta'] = {}


########################################################################
###########################TEAM AND SCORES##############################

# grab the unique game ID and use that as dictionary title
# then grab the game data and store it in a nested dictionary
for game in teamAndScoresRaw:
    gameUID = extractUID(game[0][0])
    # check to see who won the game to add to dictionary for future ease
    winnerList = ['tie', 'tie']
    winner = 'tie'
    if(int(game[1][3]) > int(game[2][3])):
        winnerList = ['winner', 'loser']
        winner = game[1][1]
    elif(int(game[1][3]) < int(game[2][3])):
        winnerList = ['loser', 'winner']
        winner = game[2][1]

    # temporary dictionary to be stored under 'teamsAndScores'
    for homeAway in range(0, len(homeAwayList)):
        dataDict[gameUID][homeAwayList[homeAway]
                          ]['general']['team'] = game[homeAway+1][1]
        dataDict[gameUID][homeAwayList[homeAway]
                          ]['general']['teamFullName'] = game[homeAway+1][2]
        dataDict[gameUID][homeAwayList[homeAway]
                          ]['general']['score'] = game[homeAway+1][3]
        dataDict[gameUID][homeAwayList[homeAway]
                          ]['general']['outcome'] = winnerList[homeAway]
        dataDict[gameUID][homeAwayList[homeAway]
                          ]['general']['previousGame'] = extractUID(game[homeAway+1][4])
        dataDict[gameUID][homeAwayList[homeAway]
                          ]['general']['nextGame'] = extractUID(game[homeAway+1][5])
        dataDict[gameUID][homeAwayList[homeAway]
                          ]['general']['yearLink'] = extractUID(game[homeAway+1][0])
    dataDict[gameUID]['teamAndScores']['winner'] = winner
    dataDict[gameUID]['teamAndScores']['homeTeam'] = game[1][1]
    dataDict[gameUID]['teamAndScores']['awayTeam'] = game[2][1]
    dataDict[gameUID]['teamAndScores']['totalScore'] = int(
        game[1][3]) + int(game[2][3])
    dataDict[gameUID]['teamAndScores']['pointSpread'] = abs(
        int(game[1][3]) - int(game[2][3]))

    # tempDict = {
    #     'homeTeam': game[1][1],
    #     'homeTeamFullName': game[1][2],
    #     'homeTeamScore': game[1][3],
    #     'homePreviousGame': extractUID(game[1][4]),
    #     'homeNextGame': extractUID(game[1][5]),
    #     'homeTeamYearLink': game[1][0],
    #     'awayTeam': game[2][1],
    #     'awayTeamFullName': game[2][2],
    #     'awayTeamScore': game[2][3],
    #     'awayPreviousGame': extractUID(game[2][4]),
    #     'awayNextGame': extractUID(game[2][5]),
    #     'awayTeamYearLink': game[2][0],
    #     'winner': winner,
    #     'totalScore': int(game[1][3]) + int(game[2][3]),
    #     'pointSpread': abs(int(game[1][3]) - int(game[2][3]))
    # }

    # dataDict[gameUID]['teamAndScores'] = tempDict

#################################################################
###########################BATTING###############################

batting_file_names = []
batting_file_names = getFilesInPath(battingPath)
battingRaw = extractData(battingPath, batting_file_names[0:3])

for game in battingRaw:
    gameUID = extractUID(game[0][0])
    dataDict[gameUID]['home']['batting'] = game[1]
    dataDict[gameUID]['away']['batting'] = game[2]

#################################################################
###########################PITCHING##############################

pitching_file_names = []
pitching_file_names = getFilesInPath(pitchingPath)
pitchingRaw = extractData(pitchingPath, pitching_file_names[0:3])

for game in pitchingRaw:
    gameUID = extractUID(game[0][0])
    dataDict[gameUID]['home']['pitching'] = game[1]
    dataDict[gameUID]['away']['pitching'] = game[2]

#################################################################
#######################STARTING LINEUP###########################
startingLineups_file_names = []
startingLineups_file_names = getFilesInPath(startingLineupsPath)
startingLineupsRaw = extractData(
    startingLineupsPath, startingLineups_file_names[0:3])

for game in startingLineupsRaw:
    gameUID = extractUID(game[0][0])
    dataDict[gameUID]['home']['startingLineup'] = game[1]
    dataDict[gameUID]['away']['startingLineup'] = game[2]

#################################################################
#######################Weather###################################

weather_file_names = []
weather_file_names = getFilesInPath(weatherPath)
weatherRaw = extractData(
    weatherPath, weather_file_names[0:3])

for game in weatherRaw:
    gameUID = extractUID(game[0][0])
    dataDict[gameUID]['weather'] = {
        'temperature': game[0][1],
        'windSpeed': game[0][2],
        'directionText': game[0][3],
        'precipitation': game[0][4],
        'weatherOverview': game[0][5]
    }
    if('Dome' in game[0][6]):
        dataDict[gameUID]['weather']['weatherOverview'] = game[0][6]
        dataDict[gameUID]['weather']['precipitation'] = game[0][6]
        dataDict[gameUID]['weather']['directionText'] = game[0][6]
        dataDict[gameUID]['weather']['windSpeed'] = game[0][6]
    if('Unknown' in game[0][7]):
        dataDict[gameUID]['weather']['weatherOverview'] = game[0][7]
        dataDict[gameUID]['weather']['precipitation'] = game[0][7]
        dataDict[gameUID]['weather']['directionText'] = game[0][7]
        dataDict[gameUID]['weather']['windSpeed'] = game[0][7]
        dataDict[gameUID]['weather']['temperature'] = game[0][7]
    dataDict

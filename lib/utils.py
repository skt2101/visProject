from .db import Database
from scipy.stats import entropy
import os
def getAllDatafromTable(tableName):
    # avoid creating multiple handles for every call to this function.
    if not hasattr(getAllDatafromTable,"connection"):
        setattr(getAllDatafromTable,"connection",Database())
    
    retVal = []
    data = getAllDatafromTable.connection.execute('select * from '+tableName)
    for row in data:
        retVal.append(row)
    return retVal

def createFile(data, fileName, featureVector):
    # Helper function to write a dataset to a csv file along with the column headers.
	# Will error out if the output file already exists.
    if os.path.exists(os.path.join(os.getcwd(), fileName)):
        print("WARNING:FileExists, will be over written")
    if not fileName.endswith('csv'):
        fileName += ".csv"
    with open(fileName, 'w') as f:

        f.write(",".join(featureVector))
        f.write("\n")
        for row in data:
            f.write(",".join(list(map(str, row))))
            f.write("\n")

def calculateEntropy(match):
    #print ("entropy function called")
    
    chances = [match[-3],match[-2],match[-1]]
    chances = [1/chance for chance in chances]
    normalizedChances = sum(chances)
    probabilities = [p/normalizedChances for p in chances]
    return entropy(probabilities)
    

def removeNan(data):
    return [row for row in data if None not in row]
# This is a helper function to build a map of country --> team -->players from the entire dataset.

def removeNanPlayer(data):
    return [row for row in data if None not in row[55:76]]
def buildCountryTeamPlayerMap():
    # 1. Get the list of all the countries in the dataset.
    countries=[]
    leagues = []
    playerTeamMap = dict()
    mathces = getAllDatafromTable('match')
    matches =removeNan(matches)
    for match in matches:
        players = match[55:76]
        homeTeam = match[7]
        awayTeam = match[8]


def temp():
    
    leagues = getAllDatafromTable('league')
    leagueNameMap = dict()
    for league in leagues:
        leagueNameMap[league[0]] = league[2]
    matches = getAllDatafromTable('match')
    matches = removeNanPlayer(matches)
    matches = matches[::-1]
    print(len(matches))
    to_keep = [ 1729,4769,7809,10257,21518,13274,17642]
    playerTeamMap = dict()
    
    for match in matches:
            players =set( match[55:77])
            for t in players:
                if playerTeamMap.get(t) is None:playerTeamMap[t] = []
                playerTeamMap[t].append(match[2])
    
    leagueTransferDict = dict()
    leagueId = [row[0] for row in leagues]
    for s in leagueId:
        leagueTransferDict[s] = dict()
        for t in leagueId:
            if s!=t:
                leagueTransferDict[s][t] = 0
    print(playerTeamMap.get(19243))
    
    for player in playerTeamMap.keys():
        temp = playerTeamMap.get(player)
        
        #print(temp)
        #print(leagueIds)
        i = 0 
        while i < len(temp) -1:
            
            fromLeague = temp[i]
            toLeague = temp[i+1]
            try:
                leagueTransferDict[fromLeague][toLeague] +=1
                #leagueTransferDict[toLeague][fromLeague] +=1
            except :
                pass
            i+=1
    #print(leagueTransferDict)
    #exit()
    retVal = dict()
    for k in leagueTransferDict.keys():
        name = leagueNameMap.get(k)
        retVal[name] = dict()
        for k1 in leagueTransferDict.get(k):
            temp = leagueNameMap.get(k1)
            retVal[name][temp] = leagueTransferDict[k][k1]
    #for k in leagueTransferDict:
    #    for k1 in leagueTransferDict.get(k):
    #        transfers.append(k1)
    #print(sorted(transfers,reverse=True))
    print(retVal)
    return retVal    
        
def temp1():
    
    leagueTeamScore = dict()    
    leagues = getAllDatafromTable('league')
    teams = getAllDatafromTable('team')
    leagueNameMap = dict()
    for league in leagues:
        leagueNameMap[league[0]] = league[2]
    teamNameMap = dict()
    for team in teams:
        teamNameMap[team[1]] = team[3]
    matches = getAllDatafromTable('match')
    matches = removeNanPlayer(matches)
    matches = matches[::-1]
    print(len(matches))
    to_keep = [ 1729,4769,7809,10257,21518,13274,17642]
    playerTeamMap = dict()
    all_seasons = set([row[3] for row in matches])
    all_seasons = sorted(list(all_seasons))
    print(all_seasons)
    #exit()
    for match in matches:
            players =set( match[55:77])
            for t in players:
                if playerTeamMap.get(t) is None:playerTeamMap[t] = dict()
                playerTeamMap[t][match[3]]=match[2]
            if match[2] in to_keep:
                if leagueTeamScore.get(leagueNameMap.get(match[2])) is None:leagueTeamScore[leagueNameMap.get(match[2])] = dict()
                home_team_goals = int(match[9])
                away_team_goals = int(match[10])
                if home_team_goals == away_team_goals:
                    home_team_score = 1
                    away_team_score = 1
                elif home_team_goals > away_team_goals:
                    home_team_score = 3
                    away_team_score = 0
                else:
                    away_team_score = 3
                    home_team_score = 0
                home_team = match[7]
                away_team = match[8]
                season = match[3]
                home_team_name = teamNameMap.get(home_team)
                away_team_name = teamNameMap.get(away_team)
                league_name = leagueNameMap.get(match[2])
                if leagueTeamScore.get(league_name).get(home_team_name) is None:
                    leagueTeamScore.get(league_name)[home_team_name] = dict()
                
                if leagueTeamScore.get(league_name).get(away_team_name) is None:
                    leagueTeamScore.get(league_name)[away_team_name] = dict()
                if leagueTeamScore.get(league_name).get(home_team_name).get(season) is None:
                    leagueTeamScore.get(league_name)[home_team_name][season] = 0
                
                if leagueTeamScore.get(league_name).get(away_team_name).get(season) is None:
                    leagueTeamScore.get(league_name)[away_team_name][season] = 0
                leagueTeamScore[league_name][home_team_name][season] += home_team_score
                leagueTeamScore[league_name][away_team_name][season] += away_team_score
    leagueTransferDict = dict()
    leagueId = [row[0] for row in leagues if row[0] in to_keep]
    for s in leagueId:
        leagueTransferDict[s] = dict()
        for t in leagueId:
            if s!=t:
                leagueTransferDict[s][t] = 0
    #print(playerTeamMap.get(19243))
    
    for player in playerTeamMap.keys():
        temp = playerTeamMap.get(player)
           
        #print(temp)
        #print(leagueIds)
        i = 0 
        while i < len(all_seasons) -1:
            
            fromLeague = temp.get(all_seasons[i])
            toLeague = temp.get(all_seasons[i+1])
            try:
                leagueTransferDict[fromLeague][toLeague] +=1
                #leagueTransferDict[toLeague][fromLeague] +=1
            except :
                pass
            i+=1
    #print(leagueTransferDict)
    #exit()
    retVal = dict()
    for k in leagueTransferDict.keys():
        name = leagueNameMap.get(k)
        retVal[name] = dict()
        for k1 in leagueTransferDict.get(k):
            temp = leagueNameMap.get(k1)
            retVal[name][temp] = leagueTransferDict[k][k1]
    #for k in leagueTransferDict:
    #    for k1 in leagueTransferDict.get(k):
    #        transfers.append(k1)
    #print(sorted(transfers,reverse=True))
    print(retVal)
    return retVal,leagueTeamScore    

def playerRatingFromId(playerId):
    if not hasattr(playerRatingFromId,"playerData"):
        setattr(playerRatingFromId,"playerData",getAllDatafromTable('player_attributes'))
    for row in playerRatingFromId.playerData:
        if row[2] == playerId:return row[4]
def getWinningChancesLeague(leagueId,team1,team2):
    matches = getAllDatafromTable('match')
    matches = removeNan(matches)
    matches = [match for match in matches if match[2]== leagueId]
    # get all matches for that league
    average_player_rating 
              

from .db import Database
from scipy.stats import entropy
import os
import numpy as np
import random
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
	# Will warn if the output file already exists.
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
    
    to_keep = [ 1729,4769,7809,10257,21518,13274,17642]
    playerTeamMap = dict()
    all_seasons = set([row[3] for row in matches])
    all_seasons = sorted(list(all_seasons))
    
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
    
    retVal = dict()
    for k in leagueTransferDict.keys():
        name = leagueNameMap.get(k)
        retVal[name] = dict()
        for k1 in leagueTransferDict.get(k):
            temp = leagueNameMap.get(k1)
            retVal[name][temp] = leagueTransferDict[k][k1]
    
    return retVal,leagueTeamScore    
'''
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
'''


def temp2():
       
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
    all_seasons = set([row[3] for row in matches])
    all_seasons = sorted(list(all_seasons))
    leagueTeamMap = dict()
    teamTransferMap = dict()

    for match in matches:
        if leagueTeamMap.get(match[2]) is None:
            leagueTeamMap[match[2]] = []
        leagueTeamMap.get(match[2]).append(match[7])
        leagueTeamMap.get(match[2]).append(match[8])
    playerTeamMap = dict()
  
    for match in matches:
            home_players =match[55:66]
            away_players =match[66:77]
            season = match[3]
            for t in home_players:
                if playerTeamMap.get(t) is None:
                    playerTeamMap[t] = dict()
                    
                playerTeamMap[t][season] = match[7]
            for t in away_players:
                if playerTeamMap.get(t) is None:
                    playerTeamMap[t] = dict()
                playerTeamMap[t][season] = match[8]


    for player in playerTeamMap.keys():
        seasonTeam = playerTeamMap.get(player)
        #print(seasonTeam)
        teams = []
        for season in all_seasons:
            teams.append(seasonTeam.get(season))
        #print(teams)    
        i = 1 
        while i < len(teams):
            if teams[i]!=teams[i-1]:
            # incoming transfer for team at index i
                if teamTransferMap.get(teams[i]) is None:teamTransferMap[teams[i]]= dict()
                if teamTransferMap.get(teams[i]).get(all_seasons[i]) is None:teamTransferMap.get(teams[i])[all_seasons[i]]=0
                teamTransferMap[teams[i]][all_seasons[i]] +=1
            i+=1
        
    #print(teamTransferMap)  

    retVal = dict()
    for league in leagueTeamMap.keys():
        leagueName = leagueNameMap.get(league)
        retVal[leagueName]=dict()
        for team in leagueTeamMap.get(league):
            #print(team)
            teamName = teamNameMap.get(team)
            retVal[leagueName][teamName] = dict()
            #print(teamTransferMap.get(team))
            if teamTransferMap.get(team) is not None:
                for season,incoming in teamTransferMap.get(team).items():
                #print(type(t))
                #for season,incoming in t.values():
                    #print(season,incoming)
                    retVal[leagueName][teamName][season] = incoming
    #exit()
    #print(retVal)
    return retVal          


def minePredictionData(leagueId):
    leagues = getAllDatafromTable('league')
    leagueIdMap = dict()
    for league in leagues:
        leagueIdMap[league[0]] = league[2]
    matches = getAllDatafromTable('match')
    matches = removeNan(matches)
    matches = [match for match in matches if match[2] == leagueId]
    # matches will now have only the matches for that league.
    # now we need to get all the teams for this league.
    teams = []
    for match in matches:
        teams.append(match[7])
        teams.append(match[8])
    teams = set(teams)
    retVal = dict()
    for team in teams:
        retVal[team] = dict()
        for team1 in teams:
            if team!=team1:
                # need to create a mapping for team,team2 now.
                retVal[team][team1] = predict(matches,team,team1)
    return retVal
# method to return the evolution of the top 5 players for each team for each league.
def getCurrentPlayerRating(playerId):
    if not hasattr(getCurrentPlayerRating,"data"):
        setattr(getCurrentPlayerRating,"data",getAllDatafromTable('player_attributes'))
    values = getCurrentPlayerRating.data
    
    ratings = []
    for row in values:
         if row[2] == playerId:ratings.append(row[5])
    if len(ratings) == 0:return 0
    idx = -1
    while ratings[idx] is None:
        idx -=1
    return ratings[idx]
def getMeanRating(playerId):
    retVal = dict()
    retVal[playerId] = dict()
    # when this function is called, player_Attributes should already be there in getCurrentPlayerRating data
    values = getCurrentPlayerRating.data
    playerMap = dict()
    for row in Database().execute('select date,overall_rating from Player_Attributes where player_api_id is '+str(playerId)):
        if row[1] is not None:
            if playerMap.get(row[0].split('-')[0]) is None:
                playerMap[row[0].split('-')[0]] = []
            playerMap[row[0].split('-')[0]].append(row[1])
    for k,v in playerMap.items():
        
            retVal[playerId][k]=np.mean(v)
    #print(retVal)
    return retVal 
def getTopPlayerforTeam(teamId):
    if not hasattr(getTopPlayerforTeam,"data"):
        setattr(getTopPlayerforTeam,"data",getAllDatafromTable('match'))
    matches = getTopPlayerforTeam.data
    players =set()
    
    #print(7809 in t)
    for match in matches:
        #print(match[7])
        if teamId == match[7]:
            #print("home")
            temp = match[55:66]
            for x in temp:
                players.add(x)
        if teamId == match[8]:
            #print("away")
            temp = match[66:77]
            for x in temp:
                players.add(x)
    players = list(players)
    
    return sorted(players,key=getCurrentPlayerRating,reverse=True)[:5]
def playerNameMap():
    retVal = dict()
    players = getAllDatafromTable('player')
    for player in players:retVal[player[1]] = player[2]
    return retVal
def topPlayerEvolution():
    retVal = dict()
    playerName = playerNameMap()
    leagues = getAllDatafromTable('league')
    teams = getAllDatafromTable('team')
    matches = getAllDatafromTable('match')
    leagueNameMap = dict()
    for league in leagues:
        leagueNameMap[league[0]] = league[2]
    teamNameMap = dict()
    for team in teams:
        teamNameMap[team[1]] = team[3]
    leagueTeamMap = dict()
    for match in matches:
        if leagueTeamMap.get(match[2]) is None:leagueTeamMap[match[2]]=set()
        
        leagueTeamMap.get(match[2]).add(match[7])
        leagueTeamMap.get(match[2]).add(match[8])
    for league in  [ 1729,7809,21518,4769,10257]:
        leagueName = leagueNameMap.get(league)
        retVal[leagueName] = dict()
        teams = leagueTeamMap.get(league)
        for team in teams:
            teamName=teamNameMap.get(team)
            retVal[leagueName][teamName] = dict()
            topPlayers = getTopPlayerforTeam(team)
            for player in topPlayers:
                t = playerName.get(player)
                retVal[leagueName][teamName][t] = getMeanRating(player).get(player)
    retVal1= dict()
    for league in leagueTeamMap.keys():
        leagueName = leagueNameMap.get(league)
        #print(leagueName)
        retVal1[leagueName] = []
        teams = list(leagueTeamMap.get(league))
        #if league == 1729:print(teams)
        #print(teams)
        for team in teams:
            #if league == 1729:
            #    print("adding team for england")
            #retVal1[leagueName]["id"] = team
            #retVal1[leagueName]["name"] = teamNameMap.get(team)
            retVal1[leagueName].append({"id":team,"name":teamNameMap.get(team)})
        retVal1[leagueName] = random.sample(retVal1.get(leagueName),10)
    return retVal,retVal1


def diversity():
    import collections
    leagues = getAllDatafromTable('league')
    leagueNameMap = dict()
    for league in leagues:
        leagueNameMap[league[0]] = league[2]
    retVal = dict()
    teamPlayer = dict()
    # get unique teams
    teams = getAllDatafromTable('team')
    teams = [ team[1] for team in teams]
    rev_matches = getAllDatafromTable('match')[::-1]
    matches = getAllDatafromTable('match')
    completed_teams = set()
    for match in rev_matches:
        home_team =  match[7]
        away_team = match[8]
        if teamPlayer.get(home_team) is None:
            teamPlayer[home_team] = []
        home_playes = match[55:66]
        away_players = match[66:77]
        home_to_insert =  25 - len(teamPlayer.get(home_team))
        if home_to_insert <= 0:
            completed_teams.add(home_team)
        if home_to_insert > 0:teamPlayer[home_team].append(home_playes[:home_to_insert])
        if teamPlayer.get(away_team) is None:
            teamPlayer[away_team] = []
        away_to_insert =  25 - len(teamPlayer.get(away_team))
        if away_to_insert <= 0 :
            completed_teams.add(away_team)
        if away_to_insert >0: teamPlayer[away_team].append(away_players[:away_to_insert])
        if len(completed_teams) == len(teams):
            #print("done with all teams breaking")
            break
    #print("out of outer match loop")
    print(teamPlayer)
    
    for team in teamPlayer.keys():
        t = []
        players = teamPlayer.get(team)
        for player in players:
            for match in matches:
                players = match[55:77]
                if player in players:
                    t.append(leagueNameMap.get(match[2]))
        retVal[team] = collections.Counter(t)
    print(retVal)

def diversity1():
    leagues = getAllDatafromTable('league')
    #teams = getAllDatafromTable('team')
    matches = removeNanPlayer(getAllDatafromTable('match'))
    rev_matches = matches[::-1]
    leagueNameMap = dict()
    for league in leagues:
        leagueNameMap[league[0]] = league[2]
    teamNameMap = dict()
    #for team in teams:
    #    teamNameMap[team[1]] = team[3]
    leagueTeamMap = dict()
    for match in matches:
        if leagueTeamMap.get(match[2]) is None:leagueTeamMap[match[2]]=set()
        
        leagueTeamMap.get(match[2]).add(match[7])
        leagueTeamMap.get(match[2]).add(match[8])
    teams_to_mine = []
    for league in  [ 1729,7809,21518,10257,4769]:
        teams_to_mine +=leagueTeamMap.get(league)
    print(teams_to_mine)
    print(teams_to_mine.index(8455))
    
    completed_teams = set()
    teamPlayer = dict()
    for match in rev_matches:
        if match[7] in teams_to_mine: 
            home_team =  match[7]
        #away_team = match[8]
            if teamPlayer.get(home_team) is None:
                teamPlayer[home_team] = set()
        #if teamPlayer.get(away_team) is None:
        #    teamPlayer[away_team] = set()
              
            home_playes = match[55:66]
            #away_players = match[66:77]
            for player in home_playes:
                teamPlayer[home_team].add(player)
                if len(teamPlayer.get(home_team)) >=25:
                    completed_teams.add(home_team)
                    break
        if match[8] in teams_to_mine:
           
            away_team = match[8]
        #if teamPlayer.get(home_team) is None:
        #    teamPlayer[home_team] = set()
            if teamPlayer.get(away_team) is None:
                teamPlayer[away_team] = set()
              
        #home_playes = match[55:66]
            away_players = match[66:77]
            for player in away_players:
                teamPlayer[home_team].add(player)
                if len(teamPlayer.get(home_team)) >=25:
                    completed_teams.add(home_team)
                    break
        if len(completed_teams) == len(teams_to_mine):
            #print("done with all teams breaking")
            break
    #print(teamPlayer)
    import collections
    retVal = dict()
    for team in teamPlayer.keys():
        t = []
        players = teamPlayer.get(team)
        for player in players:
            for match in matches:
                players = match[55:77]
                if player in players:
                    t.append(leagueNameMap.get(match[2]))
                    break
        x=collections.Counter(t)
        retVal[team] = []
        for a,b in x.items():
            #retVal[team]["name"] = a
            #retVal[team]["value"] = b
            retVal[team].append({"name":a,"value":b})
    print(len((retVal.keys())))
    return retVal

def prediction():
    teamNameMap = dict()
    teams = getAllDatafromTable('team')
    for team in teams:
        teamNameMap[team[1]] = team[3]
    #print(teamNameMap.keys())
    
    import random
    leagues = getAllDatafromTable('league')
    
    matches = removeNanPlayer(getAllDatafromTable('match'))
    rev_matches = matches[::-1]
    leagueNameMap = dict()
    
    #teamNameMap = dict()
    playerRatingId = dict()
    players = getAllDatafromTable('player_Attributes')
    for player in players[::-1]:
        playerRatingId[player[2]] = player[4]
        
    leagueTeamMap = dict()
    for match in matches:
        if leagueTeamMap.get(match[2]) is None:leagueTeamMap[match[2]]=set()
        
        leagueTeamMap.get(match[2]).add(match[7])
        leagueTeamMap.get(match[2]).add(match[8])
    retVal = dict()
    #print(leagueTeamMap)
    #exit()
    #teams = leagueTeamMap.get(1729) + leagueTeamMap.get(7809) + leagueTeamMap.get(21518) + leagueTeamMap.get(10257) + leagueTeamMap.get(4769)
    for league in  [ 1729,7809,21518,10257,4769]:
        teams = leagueTeamMap.get(league)
        randomteams = random.sample(teams,10)
        #print(teams)
        leagueDict = dict()
        #print([teamNameMap.get(x) for x in teams])
        
        for t in teams:
            tkey = teamNameMap[t]
            #currentTeam = dict()
            leagueDict[tkey] = dict()
            for match in rev_matches:
                if match[7] == t:
                    players = match[55:66]
                    break
                if match[8] == t:
                    players = match[66:77]
                    break
            for s in randomteams:
                    #print(teamNameMap.get(s))
                    #print("new team for "+ tkey)
                  
                    for match in rev_matches:
                        if match[7] == s:
                            #print("found match for "+tkey)
                            against_players = match[55:66]
                            break
                        if match[8] == s:
                            #print("found match for "+tkey)
                            against_players = match[66:77]
                            break
                    rating = sum([playerRatingId.get(x) if playerRatingId.get(x) is not None else 0 for x in players])
                    against_rating = sum([playerRatingId.get(x) if playerRatingId.get(x) is not None else 0 for x in against_players])
                    #print(players,against_players)
                    # print(rating,against_rating)
                    key = teamNameMap.get(s)
                    if abs(rating-against_rating) < 10:
                        leagueDict[tkey][key]=1
                        
                    elif rating > against_rating:
                        leagueDict[tkey][key] =3
                        
                    else:leagueDict[tkey][key] = 0
            
            #print("done with teams for "+tkey)
            if leagueDict[tkey].get(tkey) is not None:del(leagueDict[tkey][tkey])
            #leagueDict[tkey] = copy.deepcopy(currentTeam)
        retVal[league] = leagueDict
    
    #print(retVal)
    return retVal
import json
from lib import utils
countries = utils.getAllDatafromTable('Country')
matches = utils.getAllDatafromTable('Match')
leagues = utils.getAllDatafromTable('League')
teams = utils.getAllDatafromTable('Team')
players = utils.getAllDatafromTable('player_attributes')
leagueNames = []
myMap = dict()
myMap["teams"] = []
for league in leagues:
    myMap["teams"].append(league[2])
    leagueNames.append(league[2])

myMap["graphs"] = dict()
for t in leagueNames:
    myMap["graphs"][t] = dict()
    myMap["graphs"][t]["nodes"] = []
    myMap["graphs"][t]["links"] = []
#filteredPlayers = utils.removeNan(players)
#filteredPlayers = [player for player in filteredPlayers if player[4]>=80]
leaguePlayer = dict()
visitedPlayers = set()
matches = utils.removeNan(matches)
playerRatingMap = dict()
for player in players:
    playerRatingMap[player[0]] = player[4]
print(playerRatingMap)
for match in matches:
    league = match[2]
    players = match[55:77]
    for player in players:
        
        if player not in visitedPlayers and (playerRatingMap.get(player) is None or playerRatingMap.get(player) > 80) :
            visitedPlayers.add(player)
            if leaguePlayer.get(league) is None:
                leaguePlayer[league] = []
            leaguePlayer[league].append(player)
print(leaguePlayer)
    
with open('data.json','w') as f:
    f.write(json.dumps(myMap))

from lib import utils
def topPlayerEvolution():
    retVal = dict()
    
    leagues = utils.getAllDatafromTable('league')
    teams = utils.getAllDatafromTable('team')
    matches = utils.getAllDatafromTable('match')
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
    
    retVal1= dict()
    for league in leagueTeamMap.keys():
        leagueName = leagueNameMap.get(league)
        #print(leagueName)
        retVal1[leagueName] = []
        teams = list(leagueTeamMap.get(league))
        if league == 1729:print(teams)
        #print(teams)
        for team in teams:
            #if league == 1729:
            #    print("adding team for england")
            #retVal1[leagueName]["id"] = team
            #retVal1[leagueName]["name"] = teamNameMap.get(team)
            retVal1[leagueName].append({"id":team,"name":teamNameMap.get(team)})
    print(retVal1.get('England Premier League'))
    return retVal1
def test(leagueId):
    from flask import jsonify
    leagues = utils.getAllDatafromTable('league')
    leagueName=''
    for league in leagues:
        if league[0] == leagueId:leagueName = league[2]

    #print(leagueName)
    
    x = topPlayerEvolution()
    #print(leagueName in x.keys())
    #print(x.keys())
    #print(x.values())
    return (x.get(leagueName))
print(test(1729))
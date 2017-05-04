from lib import utils
leagues = utils.getAllDatafromTable('league')
matches = utils.getAllDatafromTable('match')
countries = utils.getAllDatafromTable('country')
leagueIdMap = dict()
leagueTeamMap = dict()
leagueCountryMap = dict()
for league in leagues:
    leagueIdMap[league[0]]=league[2]
for league in leagues:
    leagueCountryMap[league[1]] = league[0]
#matches = utils.removeNan(matches)
for match in matches:
    if leagueTeamMap.get(match[2]) is None:leagueTeamMap[match[2]] = set()
    #print(match[2])
    leagueTeamMap[match[2]].add(match[7])
    leagueTeamMap[match[2]].add(match[8])
#print(leagueTeamMap.keys())
data = []
for country in countries:
    leagueId = leagueCountryMap.get(country[0])
    #print(leagueId)
    leagueName = leagueIdMap.get(leagueId)
    countryName = country[1]
    numTeams = len(leagueTeamMap.get(leagueId))
    
    data.append([countryName,leagueName,numTeams])
utils.createFile(data,"euroMap.csv",["country","league","# Teams"])

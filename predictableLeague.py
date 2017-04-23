from lib import utils

import numpy as np
def generateLeagueData():
    countries = utils.getAllDatafromTable('Country')
    matches = utils.getAllDatafromTable('Match')
    leagues = utils.getAllDatafromTable('League')
    teams = utils.getAllDatafromTable('Team')
    countryId = [row[0] for row in countries]
    mergedLeagueCountry = generateMergedLeagueCountryData(countryId,countries,leagues)
    filteredMatches = getFilteredMatches(matches, mergedLeagueCountry)
    filteredMatches = utils.removeNan(filteredMatches)
    matchEntropies = list(map(utils.calculateEntropy,filteredMatches))
    entropyLeagueDict = getEntropyLeagueDict(filteredMatches, matchEntropies)
    saveToFile(entropyLeagueDict, leagues)

def getEntropyLeagueDict(filteredMatches, matchEntropies):
    retVal = dict()
    countDict = dict()
    for match, entropy in zip(filteredMatches, matchEntropies):
        if retVal.get(match[1]) is None:
            # this league not yet added in the hashmap
            retVal[match[1]] = dict()
            countDict[match[1]] = dict()
        retVal[match[1]][match[3]] = retVal[match[1]].get(match[3],0) + entropy
        countDict[match[1]][match[3]] = countDict[match[1]].get(match[3],0) + 1
    for k in retVal.keys():
        for k1 in retVal.get(k).keys():
            retVal[k][k1] /= countDict[k][k1]
    retVal[1]['2013/2014'] = 1.004
    return retVal
def saveToFile(entropyLeagueDict, leagues):
    
    featureVector = []
    idNameMap = mapLeagueIdtoName(leagues)
    
    data = []
    for league in leagues:
        
        leagueRow = []
        
        entropyMap = entropyLeagueDict.get(league[0])
        if entropyMap is None: continue
        
        featureVector.append(idNameMap.get(league[0]))
        leagueRow.append(entropyMap.get('2008/2009'))
        leagueRow.append(entropyMap.get('2009/2010'))
        leagueRow.append(entropyMap.get('2010/2011'))
        leagueRow.append(entropyMap.get('2011/2012'))
        leagueRow.append(entropyMap.get('2012/2013'))
        leagueRow.append(entropyMap.get('2013/2014'))
        leagueRow.append(entropyMap.get('2014/2015'))
        leagueRow.append(entropyMap.get('2015/2016'))
       
        data.append(leagueRow)
    data = np.asarray(data)
    utils.createFile(data.T,"seasonEntropy.csv",featureVector)
    
    
def mapLeagueIdtoName(leagues):
    retVal = dict()
    
    for league in leagues:
        retVal[league[0]] = league[2]
    
    return retVal
def generateMergedLeagueCountryData(countryId,countries,leagues):

    retVal = []
    for country in countryId:
        row = []
        row.append(country)
        row.append(country)
        for temp in countries:
            if temp[0] == country:
                row.append(temp[1])
        for league in leagues:
            if league[0] == country:
                row.append(league[2])
        retVal.append(row)
    return retVal
def getFilteredMatches(matches, mergedLeagueCountry):
    retVal = []
    leagueIds = [merged[0] for merged in mergedLeagueCountry]
    for league in leagueIds:
        for match in matches:
            if match[2] == league:
                row = []
                row.append(match[0])
                row.append(match[1])
                row.append(match[2])
                row.append(match[3])
                row.append(match[4])
                row.append(match[5])
                row.append(match[6])
                row.append(match[7])
                row.append(match[8])
                row.append(match[85])
                row.append(match[86])
                row.append(match[87])
                retVal.append(row)
    return retVal

if __name__ =='__main__':
    generateLeagueData()
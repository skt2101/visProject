from lib import utils
from lib.db import Database
from datetime import datetime
from sklearn.decomposition.pca import PCA
import numpy as np
def generatePlayerStats():
    query = """SELECT * FROM Player_Attributes a
           INNER JOIN (SELECT player_name, player_api_id AS p_id FROM Player) b ON a.player_api_id = b.p_id;"""
    data = []
    for row in Database().execute(query):
        data.append(row)
    data = [player for player in data if player[4] is not None]
    cutoff = datetime(2015,1,1)
    temp =[]
    for player in data:
        string = list(map(int,player[3].split()[0].split('-')))
        currentDate = datetime(string[0],string[1],string[2])
        if currentDate > cutoff:
            temp.append(player)
        
    visitedId = set()
    filtered = []
    for t in temp:
        if t[2] not in visitedId:
            filtered.append(t)
            visitedId.add(t[2])
        else:
            continue
    
    toRemove = {0,1,3,6,7,8}
    final = []
    for player in filtered:
        row = []
        for i in range(len(player)):
            if i not in toRemove:row.append(player[i])
        final.append(row)
    temp = []
    for row in final:
        temp.append(row[:-2])
    temp = np.asarray(temp)
    pca = PCA().fit(temp)
    
    data =[(a,b) for a,b in  zip(pca.components_[0],pca.components_[1])]
    featureVector = ["pc1","pc2"]
    utils.createFile(data, "components.csv",featureVector)
    getEvolutionData(final)
def getEvolutionData(players):
    #print (players[0])
    retVal = dict()
    sortedByRating = sorted(players, key = lambda x  : x[1],reverse=True)[:10]
    for player in sortedByRating:
        playerMap = dict()
        maptoAttach = dict()
        playerName = player[-2]
        x = player[0]
        temp = []
        for row in Database().execute('select date,overall_rating from Player_Attributes where player_api_id is '+str(x)):
            temp.append(row)
        for row in temp:
            if playerMap.get(row[0].split('-')[0]) is None:
                playerMap[row[0].split('-')[0]] = []
            playerMap[row[0].split('-')[0]].append(row[1])
        #print(playerMap)
        retVal[playerName] = dict()
        for k,v in playerMap.items():
            retVal[playerName][k]=np.mean(v)
        #print(retVal)
    data = []
    featureVector = []
    for player in retVal.keys():
        row = []
        featureVector.append(player)
        row.append(retVal.get(player).get('2007'))
        row.append(retVal.get(player).get('2008'))
        row.append(retVal.get(player).get('2009'))
        row.append(retVal.get(player).get('2010'))
        row.append(retVal.get(player).get('2011'))
        row.append(retVal.get(player).get('2012'))
        row.append(retVal.get(player).get('2013'))
        row.append(retVal.get(player).get('2014'))
        row.append(retVal.get(player).get('2015'))
        data.append(row)
    data = np.asarray(data)
    utils.createFile(data.T,"topPlayerRating.csv",featureVector)
if __name__ =='__main__':
    generatePlayerStats()
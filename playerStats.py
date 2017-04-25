from lib import utils
from lib.db import Database
from datetime import datetime
from sklearn.decomposition.pca import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.manifold import TSNE
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
    namesRating = []
    for player in filtered:
        namesRating.append([player[-2],player[4]])
        row = []
        for i in range(len(player)):
            if i not in toRemove:row.append(player[i])
        final.append(row)
    temp = []
    for row in final:
        temp.append(row[:-2])
    temp = np.asarray(temp)
    temp = StandardScaler().fit_transform(temp)
    DimRed(temp,'PCA',namesRating)
    DimRed(temp,'TSNE',namesRating)
    getEvolutionData(final)
def DimRed(temp,algo,namesRating):
    if algo == 'PCA':
        pca = PCA(n_components=2,random_state=0).fit_transform(temp)
    else:
        pca = TSNE(n_components=2,random_state=0).fit_transform(temp)
    comp1 = pca[:,0]
    comp2 = pca[:,1]
    data = []
    for a,b,c in zip(comp1,comp2,namesRating):
        data.append([a,b,c[0],c[1]])
    data = [row for row in data if row[3]>80]
    data.sort(key = lambda x: x[3],reverse=True)
    #data =[[a,b] for a,b in  zip(comp1,comp2)]
    featureVector = ["pc1","pc2","name","rating"]
    if algo == 'PCA':
        utils.createFile(data, "components.csv",featureVector)
    else:
        utils.createFile(data, "TSNEcomponents.csv",featureVector)
    
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
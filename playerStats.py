from lib import utils
from lib.db import Database
from datetime import datetime
from sklearn.decomposition.pca import PCA
import numpy as np
def generatePlayerStats():
    #utils.getAllDatafromTable('Player _Stats')
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
            filtered.append(t[:-2])
            visitedId.add(t[2])
        else:
            continue
    #print(len(filtered))
    #rint(len(filtered[0]))
    toRemove = {0,1,3,6,7,8}
    final = []
    for player in filtered:
        row = []
        for i in range(len(player)):
            if i not in toRemove:row.append(player[i])
        final.append(row)
    print(len(final))
    print(len(final[0]))
    print(final[0])
    final = np.asarray(final)
    pca = PCA().fit(final)
    print (pca.components_)
    data =[(a,b) for a,b in  zip(pca.components_[0],pca.components_[1])]
    featureVector = ["pc1","pc2"]
    utils.createFile(data, "components.csv",featureVector)
if __name__ =='__main__':
    generatePlayerStats()
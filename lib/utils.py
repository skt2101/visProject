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


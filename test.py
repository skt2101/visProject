from lib.db import Database
from lib import utils

if __name__ == '__main__':
    obj = Database()
    obj.cursor.execute('select * from player_attributes')
    #names = [description[0] for description in obj.cursor.description]
    #print(names[55:77])
    #print(names)
    
    #print(names.index('positioning'))
    #print([player[-1] for player in utils.getAllDatafromTable('player_attributes')])
    obj.tearDown()
    utils.diversity1()
    #print(x.get(10212))
    #utils.prediction()
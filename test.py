from lib.db import Database
from lib import utils
import random
import json
if __name__ == '__main__':
    obj = Database()
    obj.cursor.execute('select * from player_attributes')
    print("Total Teams= "+str(len(utils.getAllDatafromTable('team'))))
    print("Total Players= "+str(len(utils.getAllDatafromTable('player'))))
    #utils.prediction1()
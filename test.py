from lib.db import Database
from lib import utils

if __name__ == '__main__':
    obj = Database()
    obj.cursor.execute('select * from team')
    names = [description[0] for description in obj.cursor.description]
    print(names)
    #matches = utils.getAllDatafromTable('match')
    #matches = sorted(matches,key = lambda x : x[5],reverse=True)
    #print(matches)
    #print(names.index('home_player_X1'))
    #print(names.index('home_player_Y1'))
    #print(names.index('home_player_1'))
    #print(names.index('away_player_11'))
    #print(names.index('home_player_1'))
    #print(names.index('away_player_11'))
    #for row in obj.execute('select * from match'):
    #    if 9987 in row:print(row)
    teams = utils.getAllDatafromTable('team')
    for team in teams:
        #if team[1] == 8456:print(team[3])
        if 'madri' in team[3].lower():print(team[1])
    obj.tearDown()
    
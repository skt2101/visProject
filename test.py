from lib.db import Database
if __name__ == '__main__':
    obj = Database()
    obj.cursor.execute('select * from match')
    names = [description[0] for description in obj.cursor.description]
    print(names)
    #print(names.index('home_player_X1'))
    #print(names.index('home_player_Y1'))
    #print(names.index('home_player_1'))
    #print(names.index('away_player_11'))
    #print(names.index('home_player_1'))
    #print(names.index('away_player_11'))
    #for row in obj.execute('select * from match'):
    #    if 9987 in row:print(row)
    obj.tearDown()
    
from lib.db import Database
if __name__ == '__main__':
    obj = Database()
    obj.cursor.execute('select * from  team')
    names = [description[0] for description in obj.cursor.description]
    print(names)
    #for row in obj.execute('select * from match'):
    #    if 9987 in row:print(row)
    obj.tearDown()
    
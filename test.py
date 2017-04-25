from lib.db import Database
if __name__ == '__main__':
    obj = Database()
    obj.cursor.execute('select * from Player_Attributes')
    names = [description[0] for description in obj.cursor.description]
    print(names)
    obj.tearDown()
    
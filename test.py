from lib.db import Database
if __name__ == '__main__':
    obj = Database()
    for row in obj.execute('select * from country'):
        print row
    obj.tearDown()
    
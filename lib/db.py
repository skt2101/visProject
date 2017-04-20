import sqlite3
import traceback
class Database:
    def __init__(self):
        self.connection = None
        self.connectDB()
        self.cursor = self.connection.cursor()
        self.connClosed = False
    def connectDB(self):
        try:
            self.connection = sqlite3.connect('database/database.sqlite')
        except :
            raise ValueError("Failed to connect to DB")
            traceback.print_exc()
    def execute(self, query):
        if not self.connection or self.connClosed:
            # connection attempt to DB had failed earlier. Abort
            raise ValueError("DB connection not valid or has been closed previously.")
        else:
            # valid connection.
            return self.cursor.execute(query)
    def tearDown(self):
        if self.connection:
            self.connection.close()
            self.connClosed = True
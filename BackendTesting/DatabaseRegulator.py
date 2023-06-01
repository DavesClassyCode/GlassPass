import sqlite3, pandas
from DBUserHandler import DBHandler

def eraseUserData(cursor):
    cursor.execute('DELETE FROM Users;')

def addDummyData(cursor):
    data = pandas.read_csv('logins.csv',header=None)
    dbFiller = DBHandler()
    for val in data.values:
        try:
            dbFiller.insertNewUserData(val[0], val[1], val[2], val[3], val[4])
        except Exception as e:
            print(e)

if __name__ == '__main__':
    print('start')
    import os
    print(os.listdir())
    dbPath = 'unittestDB.db'
    print(os.path.isfile(dbPath))
    connection = sqlite3.connect(dbPath)
    cursor = connection.cursor()
    eraseUserData(cursor)
    addDummyData(cursor)
    print('done')

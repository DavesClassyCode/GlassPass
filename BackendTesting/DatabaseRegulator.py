import sqlite3, pandas, os
from DBUserHandler import DBHandler

def eraseUserData(cursor):
    cursor.execute('DELETE FROM Users;')

def addDummyData(cursor,dbPath):
    data = pandas.read_csv('logins.csv',header=None)
    dbFiller = DBHandler(dbPath)
    for val in data.values:
        print(val)
        dbFiller.insertNewUserData(val[0], val[1], val[2], val[3], val[4])

if __name__ == '__main__':
    print('start')
    # dbPath = 'unittestDB.db'
    os.chdir('..')
    dbPath = 'SkateDB.db'
    connection = sqlite3.connect(dbPath)
    cursor = connection.cursor()
    eraseUserData(cursor)
    connection.commit()
    addDummyData(cursor,dbPath)
    connection.commit()
    print('done')

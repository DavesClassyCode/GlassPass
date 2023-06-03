"""
FYI when this is run, it will wipe out everything in the users table of the SkateDB.db database unless
the dbPath variable is changed

Database cleaning tool

Created by Dillon M
Created 6/1/2023
Last Edited by Dillon M
Last Modified  6/1/2023
Created for CSI2999 Polyrhythm Skate semester project to regulate the data present in the
SkateDB.db database to remove clutter from the database and to establish known testing data

Relevant online documentation:
N/A

Change Log:
6/1/2023 Initial Version

Future Task List:
Make more values in logins.csv to populate the table
"""

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

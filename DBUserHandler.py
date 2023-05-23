"""
Database interaction tool

Created by Dillon M
Created 5/20/2023
Last Edited by Dillon M
Last Modified  5/22/2023
Created for CSI2999 Polyrhythm Skate semester project

Relevant online documentation:
https://passlib.readthedocs.io/en/stable/narr/hash-tutorial.html#hashing-verifying
https://docs.python.org/3/library/sqlite3.html#module-sqlite3

Change Log:
5/20/2023: Initial Version

5/22/2023: Modified exception classes to avoid using general "Exception" class
Work on preliminary unit testing

Future Task List:
Create function to add dummy user data
Do unit testing
"""

import os
import sqlite3
import unittest

from passlib.hash import pbkdf2_sha256

tableColumnDict = {'Users': '("UID" INTEGER NOT NULL UNIQUE, "FirstName" TEXT, "LastName" TEXT, "Email" TEXT, "Password" TEXT, PRIMARY KEY ("UID" AUTOINCREMENT))'}
tableInsertDict = {'Users': '("UID", "FirstName", "LastName", "Email", "Password") VALUES (?, ?, ?, ?)'}

class DBHandler():

    def __init__(self,databasePath = None):
        """
        Initializes the SQLite Database Connection, raises FileNotFoundError if the database is missing
        """
        self.dbPath = databasePath
        if self.dbPath is None:
            self.dbPath = 'SkateDB.db'
        if not os.path.isfile(self.dbPath):
            raise FileNotFoundError("Database file not found in base program directory")
        self.dbConnection = sqlite3.connect(self.dbPath)
        self.dbCursor = self.dbConnection.cursor()

        #make sure the table exists before trying to do work later
        self.createTable('Users')

    def createTable(self,tableName):
        """
        Verify that table exists before doing further SQL work, mainly for initialization purposes
        :param tableName:
        :return: None
        """
        self.dbCursor.execute(f'CREATE TABLE IF NOT EXISTS {tableName} {tableColumnDict[tableName]}')
        self.dbConnection.commit()

    def insertNewUserData(self, args):
        """
        Adds a single new user to the database
        :param args: length 4 tuple (or data which can be converted to a list) in format of firstname, lastname, email, password
        :return:
        """
        FirstName, LastName, Email, Password = tuple(args)
        try:
            self.checkDuplicateUserInfo(FirstName, LastName, Email)
        except sqlite3.DataError as e:
            print(e)
            return False
        passHash = self.hashPassword(str(Password))
        statement = 'INSERT INTO Users (FirstName, LastName, Email, Password) VALUES (?, ?, ?, ?);'
        arg = (str(FirstName), str(LastName), str(Email), passHash)
        self.dbCursor.execute(statement, arg)
        self.dbConnection.commit()
        return True

    def checkDuplicateUserInfo(self, FirstName, LastName, Email):
        """
        Verify that the database does not have a matching first/last name pair as a new user
        and that a new email does not already exist in the database
        :param FirstName:
        :param LastName:
        :param Email:
        :return:
        """
        statement = 'SELECT FirstName, LastName FROM Users WHERE FirstName=? AND LastName = ?;'
        arg = (FirstName, LastName,)
        if len(self.dbCursor.execute(statement, arg).fetchall()) > 0:
            raise sqlite3.DataError('Duplicate First and Last name pair')
        statement = 'SELECT Email FROM Users WHERE Email=?;'
        arg = (Email,)
        if self.dbCursor.execute(statement, arg).fetchone() is not None:
            raise sqlite3.DataError('Duplicate Email found in table')

    def retrievePassHash(self, UID=None, FirstName=None, LastName=None, Email=None):
        """
        Retrieves hashed password from database, accepts UID, First and Last name, or email
        :param UID:
        :param FirstName:
        :param LastName:
        :param Email:
        :return: password hash
        """
        if UID is not None:
            statement = 'SELECT Password FROM USERS WHERE UID=?;'
            arg = (str(UID),)
            return self.dbCursor.execute(statement, arg).fetchone()[0]
        elif FirstName is not None and LastName is not None:
            statement = 'SELECT Password FROM USERS WHERE FirstName=? AND LastName=?;'
            arg = (str(FirstName), str(LastName),)
            return self.dbCursor.execute(statement, arg).fetchone()[0]
        elif Email is not None:
            statement = 'SELECT Password FROM Users WHERE Email=?;'
            arg = (str(Email),)
            return self.dbCursor.execute(statement, arg).fetchone()[0]
        else:
            raise ValueError("No arguments given")

    def hashPassword(self,rawPassword):
        """
        Use passlib to securely hash the user password
        :param rawPassword: string password value
        :return: hashed password
        """
        return pbkdf2_sha256.hash(str(rawPassword))

    def verifyPassword(self,rawPassword,UID=None,FirstName=None,LastName=None,Email=None):
        """
        return true/false depending on whether the provided raw password matches the password hash retrieved from
        the database

        accepts UID, FirstName and LastName, or Email
        :param rawPassword: user password entered in HTML login form
        :param UID:
        :param FirstName:
        :param LastName:
        :param Email:
        :return: True or False depending on password match
        """
        return pbkdf2_sha256.verfy(str(rawPassword), self.retrievePassHash(UID, FirstName, LastName, Email))

    def attemptLogin(self, emailArg, passwordArg):
        """
        Verifies that user email exists then attempts password verification
        :param emailArg:
        :param passwordArg:
        :return: False if email and password match is not found, True if a match is found
        """
        statement = "SELECT Email FROM Users WHERE Email=?;"
        arg = (str(emailArg),)
        if self.dbCursor.execute(statement,arg).fetchone()[0] is None:
            return False
        return self.verifyPassword(passwordArg, Email=emailArg)

class DBUserHandlerUnitTesting(unittest.TestCase):
    def testBasicNewUserInsert(self):
        testDB = DBHandler('unittestDB.db')
        testDB.dbCursor.execute('DELETE FROM Users;')
        testDB.dbConnection.commit()
        unittest.TestCase.assertTrue(self, expr=testDB.insertNewUserData(['testFirstName1', 'testLastName1', 'test1@mail.com', 'password1']), msg='Failed to add first user')
        unittest.TestCase.assertTrue(self, expr=testDB.insertNewUserData(['testFirstName2', 'testLastName2', 'test2@mail.com', 'password2']), msg='Failed to add second user')
        unittest.TestCase.assertTrue(self, expr=testDB.insertNewUserData(['testFirstName3', 'testLastName3', 'test3@mail.com', 'password2']), msg='Failed to add user with duplicate password')
        unittest.TestCase.assertTrue(self, expr=testDB.insertNewUserData(['testFirstName2', 'testLastName3', 'test4@mail.com', 'password3']), msg='Failed to add user with mismatched repeat names')
        testDB.dbCursor.execute('DELETE FROM Users;')
        testDB.dbConnection.commit()

    def testDuplicateUserInsert(self):
        testDB = DBHandler('unittestDB.db')
        testDB.dbCursor.execute('DELETE FROM Users;')
        testDB.insertNewUserData(['testFirstName1', 'testLastName1', 'test1@mail.com', 'password1'])
        unittest.TestCase.assertFalse(self, expr=testDB.insertNewUserData(['testFirstName1', 'testLastName1', 'test2@mail.com', 'password2']),msg='Did not add duplicate user firstname/lastname')
        unittest.TestCase.assertFalse(self, expr=testDB.insertNewUserData(['testFirstName2', 'testLastName2', 'test1@mail.com', 'password3']),msg='Did not add duplicate user email')
        testDB.dbCursor.execute('DELETE FROM Users;')
        testDB.dbConnection.commit()

    def testGoodLogin(self):
        pass

    def testBadLogin(self):
        pass

if __name__ == '__main__':
    #Only for unit testing database connector
    unittest.main()
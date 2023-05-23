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
import re

from passlib.hash import pbkdf2_sha256, argon2

tableColumnDict = {'Users': '("UID" INTEGER NOT NULL UNIQUE, "FirstName" TEXT, "LastName" TEXT, "Username" TEXT, "Email" TEXT, "Password" TEXT, PRIMARY KEY ("UID" AUTOINCREMENT))'}
tableInsertDict = {'Users': '("UID", "FirstName", "LastName", "Username", "Email", "Password") VALUES (?, ?, ?, ?, ?)'}

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
        :param args: length 5 tuple (or data which can be converted to a list) in format of firstname, lastname, email, password
        :return:
        """
        #TODO: sanitize input
        FirstName, LastName, Username, Email, Password = tuple(args)
        try:
            self.checkDuplicateUserInfo(Username, Email)
        except sqlite3.DataError:
            return False
        passHash = self.hashPassword(str(Password))
        statement = 'INSERT INTO Users (FirstName, LastName,  Username, Email, Password) VALUES (?, ?, ?, ?, ?);'
        arg = (str(FirstName), str(LastName), str(Username), str(Email), passHash)
        self.dbCursor.execute(statement, arg)
        self.dbConnection.commit()
        return True

    def checkDuplicateUserInfo(self, Username, Email):
        """
        Verify that the database does not have a matching first/last name pair as a new user
        and that a new email does not already exist in the database
        :param Username:
        :param Email:
        :return:
        """
        statement = 'SELECT Username FROM Users WHERE Username=?;'
        arg = (Username,)
        if len(self.dbCursor.execute(statement, arg).fetchall()) > 0:
            raise sqlite3.DataError('Duplicate Username')
        statement = 'SELECT Email FROM Users WHERE Email=?;'
        arg = (Email,)
        if len(self.dbCursor.execute(statement, arg).fetchall()) > 0:
            raise sqlite3.DataError('Duplicate Email found in table')

    def retrievePassHash(self, Username=None, Email=None):
        """
        Retrieves hashed password from database, accepts Username or email
        :param Username:
        :param Email:
        :return: password hash
        """
        if Username is not None:
            statement = 'SELECT Password FROM USERS WHERE Username=?;'
            arg = (str(Username),)
            try:
                return self.dbCursor.execute(statement, arg).fetchone()[0]
            except TypeError:
                raise ValueError('No matching username and password pair')
        elif Email is not None:
            statement = 'SELECT Password FROM Users WHERE Email=?;'
            arg = (str(Email),)
            try:
                return self.dbCursor.execute(statement, arg).fetchone()[0]
            except TypeError:
                raise ValueError('No matching email and password pair')
        else:
            raise ValueError('No input')

    def hashPassword(self, rawPassword):
        """
        Use passlib to securely hash the user password
        :param rawPassword: string password value
        :return: hashed password
        """
        #TODO: Sanitize input and check password integrity
        return pbkdf2_sha256.hash(str(rawPassword))

    def verifyPassword(self, rawPassword, Username=None, Email=None):
        """
        return true/false depending on whether the provided raw password matches the password hash retrieved from
        the database

        accepts Username or Email
        :param rawPassword: user password entered in HTML login form
        :param Username:
        :param Email:
        :return: True or False depending on password match
        """
        try:
            return pbkdf2_sha256.verify(str(rawPassword), self.retrievePassHash(Username, Email))
        except ValueError:
            return False

    def attemptLogin(self, passwordArg, Email=None, Username=None):
        """
        Verifies that user email exists then attempts password verification
        :param emailArg:
        :param passwordArg:
        :return: False if email and password match is not found, True if a match is found
        """
        #TODO: sanitize input
        return self.verifyPassword(passwordArg, Email=Email, Username=Username)

class DBUserHandlerUnitTesting(unittest.TestCase):
    def testBasicNewUserInsert(self):
        testDB = DBHandler('unittestDB.db')
        testDB.dbCursor.execute('DELETE FROM Users;')
        testDB.dbConnection.commit()
        unittest.TestCase.assertTrue(self, expr=testDB.insertNewUserData(['testFirstName1', 'testLastName1', 'testUsername1', 'test1@mail.com', 'password1']), msg='Failed to add first user')
        unittest.TestCase.assertTrue(self, expr=testDB.insertNewUserData(['testFirstName2', 'testLastName2', 'testUsername2', 'test2@mail.com', 'password2']), msg='Failed to add second user')
        unittest.TestCase.assertTrue(self, expr=testDB.insertNewUserData(['testFirstName3', 'testLastName3', 'testUsername3', 'test3@mail.com', 'password2']), msg='Failed to add user with duplicate password')
        unittest.TestCase.assertTrue(self, expr=testDB.insertNewUserData(['testFirstName3', 'testLastName3', 'testUsername4', 'test4@mail.com', 'password3']), msg='Failed to add user with duplicate names')
        testDB.dbCursor.execute('DELETE FROM Users;')
        testDB.dbConnection.commit()

    def testDuplicateUserInsert(self):
        testDB = DBHandler('unittestDB.db')
        testDB.dbCursor.execute('DELETE FROM Users;')
        testDB.dbConnection.commit()
        testDB.insertNewUserData(['testFirstName1', 'testLastName1', 'testUsername1', 'test1@mail.com', 'password1'])
        unittest.TestCase.assertFalse(self, expr=testDB.insertNewUserData(['testFirstName1', 'testLastName1', 'testUsername1', 'test2@mail.com', 'password2']),msg='Did not add duplicate user firstname/lastname')
        unittest.TestCase.assertFalse(self, expr=testDB.insertNewUserData(['testFirstName2', 'testLastName2', 'testUsername3', 'test1@mail.com', 'password3']),msg='Did not add duplicate user email')
        testDB.dbCursor.execute('DELETE FROM Users;')
        testDB.dbConnection.commit()

    def testGoodLogin(self):
        testDB = DBHandler('unittestDB.db')
        testDB.dbCursor.execute('DELETE FROM Users;')
        testDB.dbConnection.commit()
        testDB.insertNewUserData(['testFirstName1', 'TestLastName1', 'testUsername1', 'test1@mail.com', 'password1'])
        unittest.TestCase.assertTrue(self, expr=testDB.attemptLogin('password1', Username='testUsername1'))
        unittest.TestCase.assertTrue(self, expr=testDB.attemptLogin('password1', Email='test1@mail.com'))
        testDB.dbCursor.execute('DELETE FROM Users;')
        testDB.dbConnection.commit()

    def testBadLogin(self):
        testDB = DBHandler('unittestDB.db')
        testDB.dbCursor.execute('DELETE FROM Users;')
        testDB.dbConnection.commit()
        testDB.insertNewUserData(['testFirstName1', 'TestLastName1', 'testUsername1', 'test1@mail.com', 'password1'])
        unittest.TestCase.assertFalse(self, expr=testDB.attemptLogin('password2', Username='testUsername1'))
        unittest.TestCase.assertFalse(self, expr=testDB.attemptLogin('password2', Email='test1@mail.com'))
        unittest.TestCase.assertFalse(self, expr=testDB.attemptLogin('password1', Username='testUsername2'))
        unittest.TestCase.assertFalse(self, expr=testDB.attemptLogin('password1', Email='test2@mail.com'))
        testDB.dbCursor.execute('DELETE FROM Users;')
        testDB.dbConnection.commit()

if __name__ == '__main__':
    #Only for unit testing database connector
    unittest.main()
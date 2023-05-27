"""
Database interaction tool

Created by Dillon M
Created 5/20/2023
Last Edited by Dillon M
Last Modified  5/27/2023
Created for CSI2999 Polyrhythm Skate semester project

Relevant online documentation:
https://passlib.readthedocs.io/en/stable/narr/hash-tutorial.html#hashing-verifying
https://docs.python.org/3/library/sqlite3.html#module-sqlite3

Change Log:
5/20/2023: Initial Version

5/22/2023: Modified exception classes to avoid using general "Exception" class
Work on preliminary unit testing

5/24/2023: Added input sanitization and misc improvements for good coding practices

5/27/2023: Fixed regex and modified exceptions to be custom exception classes

Future Task List:
Do unit testing for input sanitization
"""

import os, sqlite3, unittest, re
from passlib.hash import pbkdf2_sha256
from exceptions import *

tableColumnDict = {'Users': '("UID" INTEGER NOT NULL UNIQUE, "FirstName" TEXT NOT NULL, "LastName" TEXT NOT NULL, "Username" TEXT NOT NULL UNIQUE, "Email" TEXT NOT NULL UNIQUE, "Password" TEXT NOT NULL, PRIMARY KEY ("UID" AUTOINCREMENT))'}
tableInsertDict = {'Users': '("UID", "FirstName", "LastName", "Username", "Email", "Password") VALUES (?, ?, ?, ?, ?)'}


class DBHandler():

    def __init__(self, databasePath=None):
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

        # make sure the table exists before trying to do work later
        self.createTable('Users')

    def createTable(self, tableName):
        """
        Verify that table exists before doing further SQL work, mainly for initialization purposes
        :param tableName:
        :return: None
        """
        self.dbCursor.execute(f'CREATE TABLE IF NOT EXISTS {tableName} {tableColumnDict[tableName]}')
        self.dbConnection.commit()

    def insertNewUserData(self, FirstName, LastName, Username, Email, Password):
        """
        Adds new user to database.
        :param FirstName:
        :param LastName:
        :param Username:
        :param Email:
        :param Password:
        :return: True if storage is successful, false if not
        """
        # if FirstName is None or LastName is None or Username is None or Email is None or Password is None:
        #     raise ValueError('Missing Data in new user storage')
        if self.sanitze(FirstName, 'Name') is None or self.sanitze(LastName, 'Name') is None or self.sanitze(Username, 'Name') is None or self.sanitze(
                Email, 'Email') is None:
            raise UnsanitaryInputException('Unsanitary input')
        if self.checkPasswordIntegrity(Password) is None:
            raise BadPasswordException('Password is not strong enough')
        self.checkDuplicateUserInfo(Username, Email)
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
        Use passlib to securely store the user password
        :param rawPassword: string password value
        :return: hashed password
        """
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
        return pbkdf2_sha256.verify(str(rawPassword), self.retrievePassHash(Username, Email))

    def attemptLogin(self, passwordArg, Email=None, Username=None):
        """
        Verifies that user email exists then attempts password verification. Mostly exists to sanitze input
        before login and as a wrapper that makes more sense for naming than verifyPassword
        :param emailArg:
        :param passwordArg:
        :return: False if email and password match is not found, True if a match is found
        """
        if Username is not None:
            if self.sanitze(Username, 'Name') is None:
                raise UnsanitaryInputException('Unsanitary Input')
        elif Email is not None:
            if self.sanitze(Email, 'Email') is None:
                raise UnsanitaryInputException('Unsanitary Input')
        return self.verifyPassword(passwordArg, Email=Email, Username=Username)

    def sanitze(self, arg, typeflag=None):
        """
        Name type verifies that arg only contains ', -, or alphabetical characters
        Email tag verifies that arg only contains -,_,@,. and alphanumeric characters
        :param arg:
        :param typeflag:
        :return:
        """
        if typeflag == 'Name':
            regexStr = '^[A-Za-z]+(((\'|\-|\.)?([A-Za-z])+))?$'
        if typeflag == 'Email':
            regexStr = '^[a-zA-Z0-9.!#$%&’*+=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$'
        return re.match(regexStr, arg)

    def checkPasswordIntegrity(self, pwd):
        """
        verifies that passwords are between minlen and maxlen, and have one capital letter, one lowercase letter,
        one symbol, and one number
        :param pwd:
        :return:
        """
        minLen = 6
        maxLen = 20
        regexStr = '^(?=\S{' + str(minLen) + ',' + str(maxLen) + '}$)(?=.*?\d)(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[^A-Za-z\s0-9])'
        return re.match(regexStr, pwd)

class DBUserHandlerUnitTesting(unittest.TestCase):
    def testBasicNewUserInsert(self):
        testDB = DBHandler('unittestDB.db')
        testDB.dbCursor.execute('DELETE FROM Users;')
        testDB.dbConnection.commit()
        unittest.TestCase.assertTrue(self, expr=testDB.insertNewUserData('testFirstName1', 'testLastName1', 'testUsername1', 'test1@mail.com', 'password1'), msg='Failed to add first user')
        unittest.TestCase.assertTrue(self, expr=testDB.insertNewUserData('testFirstName2', 'testLastName2', 'testUsername2', 'test2@mail.com', 'password2'), msg='Failed to add second user')
        unittest.TestCase.assertTrue(self, expr=testDB.insertNewUserData('testFirstName3', 'testLastName3', 'testUsername3', 'test3@mail.com', 'password2'), msg='Failed to add user with duplicate password')
        unittest.TestCase.assertTrue(self, expr=testDB.insertNewUserData('testFirstName3', 'testLastName3', 'testUsername4', 'test4@mail.com', 'password3'), msg='Failed to add user with duplicate names')
        testDB.dbCursor.execute('DELETE FROM Users;')
        testDB.dbConnection.commit()

    def testDuplicateUserInsert(self):
        testDB = DBHandler('unittestDB.db')
        testDB.dbCursor.execute('DELETE FROM Users;')
        testDB.dbConnection.commit()
        testDB.insertNewUserData('testFirstName1', 'testLastName1', 'testUsername1', 'test1@mail.com', 'password1')
        unittest.TestCase.assertFalse(self, expr=testDB.insertNewUserData('testFirstName1', 'testLastName1', 'testUsername1', 'test2@mail.com', 'password2'), msg='Did not add duplicate user firstname/lastname')
        unittest.TestCase.assertFalse(self, expr=testDB.insertNewUserData('testFirstName2', 'testLastName2', 'testUsername3', 'test1@mail.com', 'password3'), msg='Did not add duplicate user email')
        testDB.dbCursor.execute('DELETE FROM Users;')
        testDB.dbConnection.commit()

    def testGoodLogin(self):
        testDB = DBHandler('unittestDB.db')
        testDB.dbCursor.execute('DELETE FROM Users;')
        testDB.dbConnection.commit()
        testDB.insertNewUserData('testFirstName1', 'TestLastName1', 'testUsername1', 'test1@mail.com', 'password1')
        testDB.insertNewUserData('testFirstName2', 'testLastName2', 'testUsername2', 'test2@mail.com', 'password2')
        unittest.TestCase.assertTrue(self, expr=testDB.attemptLogin('password1', Username='testUsername1'))
        unittest.TestCase.assertTrue(self, expr=testDB.attemptLogin('password1', Email='test1@mail.com'))
        unittest.TestCase.assertTrue(self, expr=testDB.attemptLogin('password2', Username='testUsername2'))
        unittest.TestCase.assertTrue(self, expr=testDB.attemptLogin('password2', Email='test2@mail.com'))
        testDB.dbCursor.execute('DELETE FROM Users;')
        testDB.dbConnection.commit()

    def testBadLogin(self):
        testDB = DBHandler('unittestDB.db')
        testDB.dbCursor.execute('DELETE FROM Users;')
        testDB.dbConnection.commit()
        testDB.insertNewUserData('testFirstName1', 'TestLastName1', 'testUsername1', 'test1@mail.com', 'password1')
        testDB.insertNewUserData('testFirstName2', 'testLastName2', 'testUsername2', 'test2@mail.com', 'password2')
        unittest.TestCase.assertFalse(self, expr=testDB.attemptLogin('password2', Username='testUsername1'))
        unittest.TestCase.assertFalse(self, expr=testDB.attemptLogin('password2', Email='test1@mail.com'))
        unittest.TestCase.assertFalse(self, expr=testDB.attemptLogin('password1', Username='testUsername2'))
        unittest.TestCase.assertFalse(self, expr=testDB.attemptLogin('password1', Email='test2@mail.com'))
        testDB.dbCursor.execute('DELETE FROM Users;')
        testDB.dbConnection.commit()

    def testUnsanitaryInput(self):
        pass

if __name__ == '__main__':
    # Only for unit testing database connector
    unittest.main()

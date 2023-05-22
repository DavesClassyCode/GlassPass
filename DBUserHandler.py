"""
Database interaction tool

Created by Dillon M
Created 5/20/2023
Last Edited by Dillon M
Last Modified  5/20/2023
Created for CSI2999 Polyrhythm Skate semester project

Relevant online documentation:
https://passlib.readthedocs.io/en/stable/narr/hash-tutorial.html#hashing-verifying
https://docs.python.org/3/library/sqlite3.html#module-sqlite3

Change Log:
5/20/2023: Initial Version

To Do List:
Create function to add dummy user data
"""

import os
import sqlite3
from passlib.hash import pbkdf2_sha256

tableColumnDict = {'Users': '("UID" INTEGER NOT NULL UNIQUE, "FirstName" TEXT, "LastName" TEXT, "Email" TEXT, "Password" TEXT, PRIMARY KEY ("UID" AUTOINCREMENT))'}
tableInsertDict = {'Users': '("UID", "FirstName", "LastName", "Email", "Password") VALUES (?, ?, ?, ?)'}

class DBHandler():

    def __init__(self):
        """
        Initializes the SQLite Database Connection, raises FileNotFoundError if the database is missing
        """
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
        self.checkDuplicateUserInfo(FirstName, LastName, Email)
        passHash = self.hashPassword(str(Password))
        statement = 'INSERT INTO Users (FirstName, LastName, Email, Password) VALUES (?, ?, ?, ?);'
        arg = (str(FirstName), str(LastName), str(Email), passHash)
        self.dbCursor.execute(statement, arg)
        self.dbConnection.commit()

    def checkDuplicateUserInfo(self, FirstName, LastName, Email):
        statement = 'SELECT FirstName, LastName FROM Users WHERE FirstName=? AND LastName = ?;'
        arg = (FirstName, LastName,)
        if self.dbCursor.execute(statement, arg).fetchone()[0] is not None:
            raise DataError('Duplicate First and Last name pair')
        statement = 'SELECT Email FROM Users WHERE Email=?;'
        arg = (Email,)
        if self.dbCursor.execute(statement, arg).fetchone()[0] is not None:
            raise DataError('Duplicate Email found in table')

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
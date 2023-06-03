"""
Database handler unit testing

Created by Dillon M
Created 5/22/2023
Last Edited by Dillon M
Last Modified  6/1/2023
Created for CSI2999 Polyrhythm Skate semester project to test the functionality of the database

Relevant online documentation:
N/A

Change Log:
5/22/2023: Initial Version

Future Task List:
Update values to correspond with new input sanitization rules
"""
import sqlite3
import unittest

from DBUserHandler import DBHandler
from exceptions import *

class DBUserHandlerUnitTesting(unittest.TestCase):
    def testBasicNewUserInsert(self):
        testDB = DBHandler('unittestDB.db')
        testDB.dbCursor.execute('DELETE FROM Users;')
        testDB.dbConnection.commit()
        unittest.TestCase.assertTrue(self, expr=testDB.insertNewUserData('testFirstNameOne', 'testLastNameOne', 'testUsernameOne', 'test1@mail.com', 'P@ssword1'), msg='Failed to add first user')
        unittest.TestCase.assertTrue(self, expr=testDB.insertNewUserData('testFirstNameTwo', 'testLastNameTwo', 'testUsernameTwo', 'test2@mail.com', 'P@ssword2'), msg='Failed to add second user')
        unittest.TestCase.assertTrue(self, expr=testDB.insertNewUserData('testFirstNameThree', 'testLastNameThree', 'testUsernameThree', 'test3@mail.com', 'P@ssword2'), msg='Failed to add user with duplicate password')
        unittest.TestCase.assertTrue(self, expr=testDB.insertNewUserData('testFirstNameThree', 'testLastNameThree', 'testUsernameFour', 'test4@mail.com', 'P@ssword3'), msg='Failed to add user with duplicate names')
        testDB.dbCursor.execute('DELETE FROM Users;')
        testDB.dbConnection.commit()

    def testBadUserInsert(self):
        testDB = DBHandler('unittestDB.db')
        testDB.dbCursor.execute('DELETE FROM Users;')
        testDB.dbConnection.commit()
        testDB.insertNewUserData('testFirstNameOne', 'testLastNameOne', 'testUsernameOne', 'test1@mail.com', 'P@ssword1')
        unittest.TestCase.assertRaises(self, sqlite3.DataError, testDB.insertNewUserData, *('testFirstNameOne', 'testLastNameOne', 'testUsernameOne', 'test2@mail.com', 'P@ssword2'))
        unittest.TestCase.assertRaises(self, sqlite3.DataError, testDB.insertNewUserData, *('testFirstNameTwo', 'testLastNameTwo', 'testUsernameThree', 'test1@mail.com', 'P@ssword3'))
        testDB.dbCursor.execute('DELETE FROM Users;')
        testDB.dbConnection.commit()

    def testGoodLogin(self):
        testDB = DBHandler('unittestDB.db')
        testDB.dbCursor.execute('DELETE FROM Users;')
        testDB.dbConnection.commit()
        testDB.insertNewUserData('testFirstNameOne', 'TestLastNameOne', 'testUsernameOne', 'test1@mail.com', 'P@ssword1')
        testDB.insertNewUserData('testFirstNameTwo', 'testLastNameTwo', 'testUsernameTwo', 'test2@mail.com', 'P@ssword2')
        unittest.TestCase.assertTrue(self, expr=testDB.attemptLogin('P@ssword1', Username='testUsernameOne'))
        unittest.TestCase.assertTrue(self, expr=testDB.attemptLogin('P@ssword1', Email='test1@mail.com'))
        unittest.TestCase.assertTrue(self, expr=testDB.attemptLogin('P@ssword2', Username='testUsernameTwo'))
        unittest.TestCase.assertTrue(self, expr=testDB.attemptLogin('P@ssword2', Email='test2@mail.com'))
        testDB.dbCursor.execute('DELETE FROM Users;')
        testDB.dbConnection.commit()

    def testBadLogin(self):
        testDB = DBHandler('unittestDB.db')
        testDB.dbCursor.execute('DELETE FROM Users;')
        testDB.dbConnection.commit()
        testDB.insertNewUserData('testFirstNameOne', 'TestLastNameOne', 'testUsernameOne', 'test1@mail.com', 'P@ssword1')
        testDB.insertNewUserData('testFirstNameTwo', 'testLastNameTwo', 'testUsernameTwo', 'test2@mail.com', 'P@ssword2')
        unittest.TestCase.assertFalse(self, expr=testDB.attemptLogin('P@ssword2', Username='testUsernameOne'))
        unittest.TestCase.assertFalse(self, expr=testDB.attemptLogin('P@ssword2', Email='test1@mail.com'))
        unittest.TestCase.assertFalse(self, expr=testDB.attemptLogin('P@ssword1', Username='testUsernameTwo'))
        unittest.TestCase.assertFalse(self, expr=testDB.attemptLogin('P@ssword1', Email='test2@mail.com'))
        testDB.dbCursor.execute('DELETE FROM Users;')
        testDB.dbConnection.commit()

    def testUnsanitaryInput(self):
        testDB = DBHandler('unittestDB.db')
        testDB.dbCursor.execute('DELETE FROM Users;')
        testDB.dbConnection.commit()
        unittest.TestCase.assertRaises(self, UnsanitaryInputException, testDB.insertNewUserData, *('TestFirstname1', 'TestLastNameOne', 'TestUsernameOne', 'test1@mail.com', 'P@ssword1'))
        unittest.TestCase.assertRaises(self, UnsanitaryInputException, testDB.insertNewUserData, *('TestFirstnameOne', 'TestLastName1', 'TestUsernameOne', 'test1@mail.com', 'P@ssword1'))
        unittest.TestCase.assertRaises(self, UnsanitaryInputException, testDB.insertNewUserData, *('TestFirstnameOne', 'TestLastNameOne', 'TestUsername1', 'test1@mail.com', 'P@ssword1'))
        #Do testing with names/usernames with ' or - here
        #Do email regex testing here
        unittest.TestCase.assertRaises(self, BadPasswordException, testDB.insertNewUserData, *('TestFirstnameOne', 'TestLastnameOne', 'TestUsernameOne', 'test1@mail.com', 'p@ssword1'))
        unittest.TestCase.assertRaises(self, BadPasswordException, testDB.insertNewUserData, *('TestFirstnameOne', 'TestLastnameOne', 'TestUsernameOne', 'test1@mail.com', 'Password1'))
        unittest.TestCase.assertRaises(self, BadPasswordException, testDB.insertNewUserData, *('TestFirstnameOne', 'TestLastnameOne', 'TestUsernameOne', 'test1@mail.com', 'P@ssword'))
        unittest.TestCase.assertRaises(self, BadPasswordException, testDB.insertNewUserData, *('TestFirstnameOne', 'TestLastnameOne', 'TestUsernameOne', 'test1@mail.com', '$H0rt'))
        unittest.TestCase.assertRaises(self, BadPasswordException, testDB.insertNewUserData, *('TestFirstnameOne', 'TestLastnameOne', 'TestUsernameOne', 'test1@mail.com', 'L0ng!aaaaaaaaaaaaaaaa'))
if __name__ == '__main__':
    # Only for unit testing database connector
    unittest.main()

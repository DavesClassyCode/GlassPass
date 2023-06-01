import unittest

from DBUserHandler import DBHandler

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

"""
Project specific exception class

Created by Dillon M
Created 5/20/2023
Last Edited by Dillon M
Last Modified  5/27/2023
Created for CSI2999 Polyrhythm Skate semester project

Change Log:
5/27/2023 Initial version

Future Task List:
-
"""
class BadPasswordException(Exception):
    """Password does not meet requirements defined in DBUserHandler.py"""
    def __init__(self, arg):
        super().__init__(arg)

class UnsanitaryInputException(Exception):
    """Input contains illegal characters. See requirements in DBUserHandler.py"""
    def __init__(self, arg):
        super().__init__(arg)

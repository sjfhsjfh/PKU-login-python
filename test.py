import unittest
from PKULogin import PKULogin, PKUWebApps

testUser = "testUser"
testPassword = "testPassword"

class TestStringMethods(unittest.TestCase):

    def testLogin(self):
        login = PKULogin(testUser, testPassword)
        login.login(PKUWebApps.portal)

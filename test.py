import logging
import os
import unittest
from PKULogin import PKULogin, PKUWebApps, logger


logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

logger.addHandler(console_handler)



class TestStringMethods(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.username = os.environ["PKU_STUDENT_ID"]
        self.password = os.environ["PKU_PASSWORD"]


    def test_login(self):
        login = PKULogin(self.username, self.password)
        for app in list(PKUWebApps):
            login.login(app.value)

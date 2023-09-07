import logging
import os
import unittest
from PKULogin import PKULogin, APPS, logger, SyllabusLogin


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
        for app in APPS:
            login.login(APPS[app])

    def test_syllabus(self):
        login = SyllabusLogin(self.username, self.password)
        login.login()
        self.assertEqual(
            login.session.get(
                "https://elective.pku.edu.cn/elective2008/edu/pku/stu/elective/controller/electiveWork/showResults.do"
            ).status_code,
            200
        )

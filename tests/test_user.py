import unittest
from app.models import User,Pitch

class UserModelTest(unittest.TestCase):
    def SetUp(self):
        self.new_user = User(password = 'banana')

    def test_password_setter(self):
        self.assertTrue(self.new_user.password_secure is not None)

    def test_no_access_passoword(self):
        with self.assertRaises(AttributeError):
            self.new_user.password
            
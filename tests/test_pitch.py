from app.models import Pitch,User
from app import db


def setUp(self):
    self.User_James = User(username = 'James',password = 'potato', email = 'james@ms.com')
    
from sqlalchemy import Column, Integer, String
from database import DB
from sqlalchemy_utils import EncryptedType

secret_key = '%4gggtr##4545'

class User(DB.db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True)
    email = Column(String(120), unique=True)
    password = Column(EncryptedType(String, secret_key))

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.username

    def toJSON(self):
        return {'id':self.id,
                'username': self.username,
                 'email': self.email}

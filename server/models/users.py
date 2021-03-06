#models/users.py
from db import db

class UserModel(db.Model):
    '''
    Usermodel. If some REST api should be restricted, they can force authentication.
    '''
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def save_to_db(self):
        '''
        Saves a user to the db.
        '''
        db.session.add(self) # session is collection of objects we want to write into the db
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        '''
        Returns an user by it's username.
        '''
        return UserModel.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        '''
        Returns an user by it's id.
        '''
        return cls.filter_by(id=_id).first()

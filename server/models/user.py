import sqlite3
from db import db

class UserModel(db.Model):
    #infos for sqlalchemy
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def save_to_db(self): # saving to the db
        '''
        Returns a json representation of a survey with all reports belonging to this survey.
        '''
        db.session.add(self) # session is collection of objects we want to write into the db
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        '''
        Returns a json representation of a survey with all reports belonging to this survey.
        '''
        return UserModel.query.filter_by(username=username).first() #(tablename by which we filter=uebergebenes argument)

    @classmethod
    def find_by_id(cls, _id):
        '''
        Returns a json representation of a survey with all reports belonging to this survey.
        '''        
        return cls.filter_by(id=_id).first()

#models/summaries.py

import json
from datetime import datetime
from db import db


class SummaryModel(db.Model):
    #infos for sqlalchemy
    __tablename__ = "summaries"
    id = db.Column(db.Integer, primary_key=True)
    qid = db.Column(db.Integer)             # id of a question
    surveyid = db.Column(db.String(100))    # survey id
    name = db.Column(db.String(30))         # name of a question
    type = db.Column(db.String(15))         # type of a question
    options = db.Column(db.String)          # possible answer options
    answers = db.Column(db.String)          # summaries of all answers from reports
    created = db.Column(db.String(50))      # creation data of a summary
    counter = db.Column(db.Integer)         # id of a question

    def __init__(self, qid, surveyid, name, type, options, answers,counter):
        self.qid = qid
        self.surveyid = surveyid
        self.name = name
        self.type = type
        self.options = options
        self.answers = answers
        self.created = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        self.counter = counter

    def __repr__(self):
        '''
        Representation of a summary object.
        '''
        return f" surveyid: {self.surveyid}, qid: {self.qid}, created: {self.created}, counter: {self.counter}, answers: {self.answers}"

    def tojson(self):
        '''
        JSON representation of a summary object.
        '''
        return {'surveyid': self.surveyid, 'name': self.name, 'type': self.type, 'options': json.loads(self.options), 'answers': json.loads(self.answers), 'created': self.created, 'counter': self.counter}

    def save_to_db(self):
        '''
        Saves a summary object to the database.
        '''
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        '''
        deletes a summary from the db
        '''
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_surveyid(cls, surveyid):
        '''
        Returns all summaries belonging to a surveyid.
        '''
        return cls.query.filter_by(surveyid=surveyid).all()

    @classmethod
    def find_unique_summary(cls, surveyid,qid):
        '''
        Returns a summary with the unique combination survey id and qid.
        '''
        return cls.query.filter_by(surveyid=surveyid).filter_by(qid=qid).first()

    @classmethod
    def find_by_id(cls, _id):
        '''
        Returns a summary object by its id.
        '''
        return cls.filter_by(id=_id).first()

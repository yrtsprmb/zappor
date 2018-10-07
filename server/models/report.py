import sqlite3
from db import db

## internal representation of an Report

class ReportModel(db.Model):
    #infos for sqlalchemy
    __tablename__ = "reports"
    #__abstract__ = True #no idea why this works

    #rid = db.Column(db.Integer)
    surveyid = db.Column(db.String(30), primary_key = True)
    prr = db.Column(db.Integer)
    irr = db.Column(db.Integer)
    f = db.Column(db.Float(precision=5))
    p = db.Column(db.Float(precision=5))
    q = db.Column(db.Float(precision=5))
    answers = db.Column(db.String(1000))

    def __init__(self, surveyid, prr, irr, f, p, q, answers):
        #self.rid = rid
        self.surveyid = surveyid
        self.prr = prr
        self.irr = irr
        self.f = f
        self.p = p
        self.q = q
        self.answers = answers

    # returns a json representation of the report model
    def json(self):
        return {'surveyid': self.surveyid, 'prr': self.prr, 'irr': self.irr, 'f': self.f, 'p': self.p,'q': self.q, 'answers': self.answers}


    #find a survey by its name, should be classmethod, because it returns an object of Survey Model
    @classmethod
    def find_report_by_surveyid(cls, surveyid):
        pass

    def insert(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO reports VALUES (?,?,?,?,?,?,?)"
        cursor.execute(query, (self.surveyid, self.prr, self.irr, self.f, self.p, self.q, self.answers))
        connection.commit()
        connection.close()

#import sqlite3
from db import db

## internal representation of an Report

class ReportModel(db.Model):
    #infos for sqlalchemy
    __tablename__ = "reports"
    #__abstract__ = True #no idea why this works
    id = db.Column(db.Integer, primary_key=True)
    surveyid = db.Column(db.String(30))
    prr = db.Column(db.Integer)
    irr = db.Column(db.Integer)
    f = db.Column(db.Float(precision=5))
    p = db.Column(db.Float(precision=5))
    q = db.Column(db.Float(precision=5))
    answers = db.Column(db.String(1000))

    def __init__(self, surveyid, prr, irr, f, p, q, answers):
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


    #find all reports belonging to one survey
    @classmethod
    def find_report_by_surveyid(cls, surveyid):
        return ReportModel.query.filter_by(surveyid=surveyid).all()

    def save_report_to_db(self):
            db.session.add(self)
            db.session.commit()

    def delete_report_from_db(self):
            db.session.delete(self)
            db.session.commit()

    # def insert(self):
    #     connection = sqlite3.connect('data.db')
    #     cursor = connection.cursor()
    #
    #     query = "INSERT INTO reports VALUES (?,?,?,?,?,?,?)"
    #     cursor.execute(query, (self.surveyid, self.prr, self.irr, self.f, self.p, self.q, self.answers))
    #     connection.commit()
    #     connection.close()

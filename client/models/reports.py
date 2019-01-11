#models/reports.py
import json
from db import db


class ReportModel(db.Model):
    '''
    Internal client representation for a report.
    '''
    __tablename__ = "reports"
    id = db.Column(db.Integer, primary_key=True)
    surveyid = db.Column(db.String(30))
    prr = db.Column(db.Integer)
    irr = db.Column(db.Integer)
    f = db.Column(db.Float(precision=5))
    p = db.Column(db.Float(precision=5))
    q = db.Column(db.Float(precision=5))
    answers = db.Column(db.String())

    #survey_sid = db.Column(db.Integer, db.ForeignKey('surveys.sid'))
    #survey = db.relationship('SurveyModel')

    def __init__(self, surveyid, prr, irr, f, p, q, answers):
        self.surveyid = surveyid
        self.prr = prr
        self.irr = irr
        self.f = f
        self.p = p
        self.q = q
        self.answers = answers

    def __repr__(self):
        '''
        Representation of a report object.
        '''
        return f" surveyid: {self.surveyid}, prr: {bool(self.prr)}, irr: {bool(self.irr)}, f: {self.f}, p: {self.p}, q: {self.q}, answers: {self.answers}"

    def tojson(self):
        '''
        Returns a json representation of a report model.
        '''
        return {'surveyid': self.surveyid, 'prr': bool(self.prr), 'irr': bool(self.irr), 'f': self.f, 'p': self.p,'q': self.q, 'answers': json.loads(self.answers)}

    @classmethod
    def find_report_by_surveyid(cls, surveyid):
        '''
        Returns all reports belonging to a specific survey.
        '''
        return ReportModel.query.filter_by(surveyid=surveyid).all()

    @classmethod
    def find_by_surveyid(cls, surveyid):
        '''
        Returns a report belongig to a specific survey id.
        '''
        return cls.query.filter_by(surveyid=surveyid).first()

    def save_to_db(self):
        '''
        Saves a report to the db.
        '''
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        '''
        Deletes a report from the db.
        '''
        db.session.delete(self)
        db.session.commit()

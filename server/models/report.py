import json
from db import db

#internal representation of an Report
class ReportModel(db.Model):
    #infos for sqlalchemy
    __tablename__ = "reports"
    id = db.Column(db.Integer, primary_key=True)
    #surveyid = db.Column(db.String(30))
    prr = db.Column(db.Integer)
    irr = db.Column(db.Integer)
    f = db.Column(db.Float(precision=5))
    p = db.Column(db.Float(precision=5))
    q = db.Column(db.Float(precision=5))
    answers = db.Column(db.String())

    surveyid = db.Column(db.String, db.ForeignKey('surveys.surveyid'))
    survey = db.relationship('SurveyModel')

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
        return {'surveyid': self.surveyid, 'prr': self.prr, 'irr': self.irr, 'f': self.f, 'p': self.p,'q': self.q, 'answers': json.loads(self.answers)}

    #find all reports belonging to one survey
    @classmethod
    def find_report_by_surveyid(cls, surveyid):
        return ReportModel.query.filter_by(surveyid=surveyid).all()

    #saves a report to the db
    def save_report_to_db(self):
            db.session.add(self)
            db.session.commit()

    #deletes a report from the db
    def delete_report_from_db(self):
            db.session.delete(self)
            db.session.commit()
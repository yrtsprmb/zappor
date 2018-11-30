import json
from datetime import datetime
from db import db

# internal representation of a survey
class SurveyModel(db.Model):
    #infos for sqlalchemy
    __tablename__ = "surveys"
    id = db.Column(db.Integer, primary_key=True)
    surveyid = db.Column(db.String(100), unique=True)
    serviceprovider = db.Column(db.String(50))
    surveyname = db.Column(db.String(50))
    status = db.Column(db.String(15))
    comment = db.Column(db.String(300))
    questions = db.Column(db.String)

    reports = db.relationship('ReportModel', lazy='dynamic') # a list of report models

    def __init__(self, surveyid, serviceprovider, surveyname, status, comment, questions):
        self.surveyid = serviceprovider + "_" + datetime.now().strftime('%Y-%m-%d_%H%M%S')
        self.serviceprovider = serviceprovider
        self.surveyname = surveyname
        self.status = status
        self.comment = comment
        self.questions = questions

    #representation of the object for the GUI
    def __repr__(self):
        return f" surveyid: {self.surveyid}, name: {self.surveyname}, status: {self.status}, comment: {self.comment}"

    # returns a json representation of the survey model for the serviceprovider
    def tojson(self):
        return {'surveyid': self.surveyid, 'serviceprovider': self.serviceprovider, 'surveyname': self.surveyname, 'status': self.status, 'comment': self.comment, 'questions': json.loads(self.questions)}

    #creates a json representation for clients which are asking for new surveys
    def tojsonforclient(self):
        return {'surveyid': self.surveyid, 'serviceprovider': self.serviceprovider, 'questions': json.loads(self.questions)}

    def tojsonwithreports(self):
        return {'surveyid': self.surveyid, 'serviceprovider': self.serviceprovider, 'surveyname': self.surveyname, 'status': self.status, 'comment': self.comment, 'questions': json.loads(self.questions), 'reports': [report.tojson() for report in self.reports.all()]}

    #find a survey by its name, returns an object of Survey Model
    @classmethod
    def find_survey_by_id(cls, surveyid):
        return SurveyModel.query.filter_by(surveyid=surveyid).first()

    #find an active survey by its name, returns an object of Survey Model
    @classmethod
    def find_active_survey_by_id(cls, surveyid):
        return SurveyModel.query.filter_by(surveyid=surveyid).filter_by(status='active').first()

    #find a survey by its name, returns an object of Survey Model
    @classmethod
    def find_survey_by_name(cls, surveyname):
        return SurveyModel.query.filter_by(surveyname=surveyname).first()

    def save_to_db(self):
        db.session.add(self) # session is a collection of objects we going to write into the db
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

#models/surveys.py
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
    created_on = db.Column(db.String(50))
    sdescription = db.Column(db.String(300))
    questions = db.Column(db.String)

    reports = db.relationship('ReportModel', lazy='dynamic') # a list of report models

    def __init__(self, surveyid, serviceprovider, surveyname, status, sdescription, questions):
        self.surveyid = serviceprovider + "_" + datetime.now().strftime('%Y-%m-%d_%H%M%S') #surveyid consists of name of serviceprovider and a timestamp
        self.serviceprovider = serviceprovider
        self.surveyname = surveyname
        self.status = status
        self.created_on = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        self.sdescription = sdescription
        self.questions = questions

    def __repr__(self):
        '''
        Representation of a survey object.
        '''
        return f" surveyid: {self.surveyid}, name: {self.surveyname}, status: {self.status}, created on: {self.created_on}, sdescription: {self.sdescription}, questions: {json.loads(self.questions)}"


    def tojson(self):
        '''
        Returns a json representation for a survey object.
        '''
        return {'surveyid': self.surveyid, 'serviceprovider': self.serviceprovider, 'surveyname': self.surveyname, 'status': self.status, 'created on': self.created_on, 'sdescription': self.sdescription, 'questions': json.loads(self.questions)}


    def tojsonforclient(self):
        '''
        Returns a json representation for clients asking for surveys.
        '''
        return {'surveyid': self.surveyid, 'serviceprovider': self.serviceprovider, 'questions': json.loads(self.questions)}


    def tojsonwithreports(self):
        '''
        Returns a json representation of a survey with all reports belonging to this survey.
        '''
        return {'surveyid': self.surveyid, 'serviceprovider': self.serviceprovider, 'surveyname': self.surveyname, 'status': self.status, 'created on': self.created_on, 'sdescription': self.sdescription, 'questions': json.loads(self.questions), 'reports': [report.tojson() for report in self.reports.all()]}


    @classmethod
    def find_survey_by_id(cls, surveyid):
        '''
        Finds a survey by its surveyid, returns a SurveyModel object.
        '''
        return SurveyModel.query.filter_by(surveyid=surveyid).first()


    @classmethod
    def find_active_survey_by_id(cls, surveyid):
        '''
        Finds an 'active' survey by its surveyid, returns a SurveyModel object.
        '''
        return SurveyModel.query.filter_by(surveyid=surveyid).filter_by(status='active').first()


    @classmethod
    def find_survey_by_name(cls, surveyname):
        '''
        Finds a survey by its name, returns an object of Survey Model.
        '''
        return SurveyModel.query.filter_by(surveyname=surveyname).first()


    def save_to_db(self):
        '''
        Saves a survey to the database.
        '''
        db.session.add(self) # session is a collection of objects we going to write into the db
        db.session.commit()


    def delete_from_db(self):
        '''
        Deletes a survey from the database.
        '''
        db.session.delete(self)
        db.session.commit()

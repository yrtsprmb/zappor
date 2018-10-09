from db import db

# internal representation of a survey
class SurveyModel(db.Model):
    #infos for sqlalchemy
    __tablename__ = "surveys"
    id = db.Column(db.Integer, primary_key=True)
    surveyid = db.Column(db.String(30))
    serviceprovider = db.Column(db.String(50))
    surveyname = db.Column(db.String(50))
    status = db.Column(db.String(15))
    comment = db.Column(db.String(200))
    questions = db.Column(db.String(1000))

    def __init__(self, surveyid, serviceprovider, surveyname, status, comment, questions):
        self.surveyid = surveyid
        self.serviceprovider = serviceprovider
        self.surveyname = surveyname
        self.status = status
        self.comment = comment
        self.questions = questions

    # returns a json representation of the survey model for the serviceprovider
    def json(self):
        return {'surveyid': self.surveyid, 'serviceprovider': self.serviceprovider, 'surveyname': self.surveyname, 'status': self.status, 'comment': self.comment, 'questions': self.questions}

    #creates a json representation for clients which are asking for new surveys
    def jsonforclient(self):
        return {'surveyid': self.surveyid, 'serviceprovider': self.serviceprovider, 'status': self.status, 'questions': self.questions}

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

    def save_survey_to_db(self): # like save_to_db
        db.session.add(self) # session is a collection of objects we going to write into the db
        db.session.commit()

    def delete_survey_from_db(self):
        db.session.delete(self) # session is a collection of objects we going to write into the db
        db.session.commit()

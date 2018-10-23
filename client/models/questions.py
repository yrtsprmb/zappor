import json
from db import db

# represents all questions which a client can answer
class QuestionModel(db.Model):

    __tablename__ = "client_questions"
    id = db.Column(db.Integer, primary_key=True)
    qid = db.Column(db.Integer)
    surveyid = db.Column(db.String(100))
    serviceprovider = db.Column(db.String(100))
    qname = db.Column(db.String(30))
    qtype = db.Column(db.String(30))
    qoptions = db.Column(db.String)

    def __init__(self, qid, surveyid, serviceprovider, qname, qtype, qoptions):
        self.qid = qid
        self.surveyid = surveyid
        self.serviceprovider = serviceprovider
        self.qname = qname
        self.qtype = qtype
        self.qoptions = qoptions

    #json represtation of a question from a service provider
    def tojson(self):
        return {'qid': self.qid,
            'surveyid': self.surveyid,
            'serviceprovider': self.serviceprovider,
            'qname': self.qname,
            'qtpye': self.qtype,
            'qoptions': json.loads(self.qoptions)}

    @classmethod
    def find_by_name(cls, qname):
        return QuestionModel.query.filter_by(qname=qname).first()

    @classmethod
    def find_by_surveyid(cls, surveyid):
        return QuestionModel.query.filter_by(surveyid=surveyid).first()

    def save_to_db(self): # saving to the db
        db.session.add(self) # session is collection of objects we want to write into the db
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

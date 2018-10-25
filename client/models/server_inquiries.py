import json
from db import db

# represents all questions which a client can answer
class ServerInquiriesModel(db.Model):

    __tablename__ = "server_inquiries"
    id = db.Column(db.Integer, primary_key=True)
    qid = db.Column(db.Integer)
    surveyid = db.Column(db.String(100))
    serviceprovider = db.Column(db.String(100))
    name = db.Column(db.String(30))
    type = db.Column(db.String(30))
    options = db.Column(db.String)

    def __init__(self, qid, surveyid, serviceprovider, name, type, options):
        self.qid = qid
        self.surveyid = surveyid
        self.serviceprovider = serviceprovider
        self.name = name
        self.type = type
        self.options = options

    #json represtation of a service provider question
    def tojson(self):
        return {'qid': self.qid,
            'surveyid': self.surveyid,
            'serviceprovider': self.serviceprovider,
            'name': self.name,
            'tpye': self.type,
            'options': json.loads(self.options)}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_surveyid(cls, surveyid):
        return cls.query.filter_by(surveyid=surveyid).first()

    def save_to_db(self):
        db.session.add(self) # session is collection of objects we want to write into the db
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

import json
from db import db

# represents all questions which a client can answer
class ServerInquiriesModel(db.Model):

    __tablename__ = "server_inquiries"
    id = db.Column(db.Integer, primary_key=True)
    qid = db.Column(db.Integer)                     # order of questions inside of a surveyid
    surveyid = db.Column(db.String(100))            # name of the surveyid
    serviceprovider = db.Column(db.String(50))      # name of the service provider
    name = db.Column(db.String(30))                 # name of a question
    type = db.Column(db.String(15))                 # type of a question
    options = db.Column(db.String)                  # possible answer options
    locked = db.Column(db.Integer)                  # if inquiry should be deleted after editing
    quizmode = db.Column(db.Integer)                    # if questions should be answered later by the client user

    def __init__(self, qid, surveyid, serviceprovider, name, type, options, locked, quizmode):
        self.qid = qid
        self.surveyid = surveyid
        self.serviceprovider = serviceprovider
        self.name = name
        self.type = type
        self.options = options
        self.locked = locked
        self.quizmode = quizmode

    #representation of the object for the GUI
    def __repr__(self):
        return f" surveyid: {self.surveyid},  serviceprovider: {self.serviceprovider}, qid: {self.qid}, name: {self.name}, type: {self.type}, options: {self.options}, locked: {bool(self.locked)}, quizmode: {bool(self.quizmode)}"

    #json represtation of a service provider question
    def tojson(self):
        return {'qid': self.qid,
            'surveyid': self.surveyid,
            'serviceprovider': self.serviceprovider,
            'name': self.name,
            'type': self.type,
            'options': json.loads(self.options),
            'locked': bool(self.locked),
            'quizmode': bool(self.quizmode)}

    # def compare_json(self):
    #     return {
    #         'name': self.name,
    #         'tpye': self.type,
    #         'options': json.loads(self.options)}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def already_in_db(cls, surveyid, name):
        return cls.query.filter_by(surveyid=surveyid).filter_by(name=name).first()

    @classmethod
    def find_by_surveyid(cls, surveyid):
        return cls.query.filter_by(surveyid=surveyid).first()

    @classmethod
    def find_all_by_surveyid(cls, surveyid):
        return cls.query.filter_by(surveyid=surveyid).all()

    @classmethod ## TODO: implement function from the send reports file
    def delete_all_by_surveyid(cls, surveyid):
        pass
        # vorschlag von oli, ausprobieren
        # cls.query.filter_by(surveyid==surveyid).delete()
    #db.session.query(ServerInquiriesModel).filter(ServerInquiriesModel.surveyid==surveyid).delete()

    def save_to_db(self):
        db.session.add(self) # session is collection of objects we want to write into the db
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

#models/server_inquiries.py
import json
from db import db

class ServerInquiriesModel(db.Model):
    '''
    Defines the model for the internal representation of server inquiries.
    Table will be created after first request was made after starting the app.
    '''
    __tablename__ = "server_inquiries"
    id = db.Column(db.Integer, primary_key=True)
    qid = db.Column(db.Integer)                     # order of questions inside of a surveyid
    surveyid = db.Column(db.String(100))            # name of the surveyid
    serviceprovider = db.Column(db.String(50))      # name of the service provider
    name = db.Column(db.String(30))                 # name of a question
    type = db.Column(db.String(15))                 # type of a question
    options = db.Column(db.String)                  # possible answer options
    qdescription = db.Column(db.String(300))        # description of a question
    locked = db.Column(db.Integer)                  # if inquiry should be deleted after editing
    quizmode = db.Column(db.Integer)                # if questions should be answered later by the client user

    def __init__(self, qid, surveyid, serviceprovider, name, type, options, qdescription, locked, quizmode):
        self.qid = qid
        self.surveyid = surveyid
        self.serviceprovider = serviceprovider
        self.name = name
        self.type = type
        self.options = options
        self.qdescription = qdescription
        self.locked = locked
        self.quizmode = quizmode

    def __repr__(self):
        '''
        JSON representation of a server inquiry.
        '''
        return f" surveyid: {self.surveyid},  serviceprovider: {self.serviceprovider}, qid: {self.qid}, name: {self.name}, type: {self.type}, options: {self.options}, description: {self.qdescription}, locked: {bool(self.locked)}, quizmode: {bool(self.quizmode)}"

    def tojson(self):
        '''
        JSON representation of a server inquiry.
        '''
        return {'qid': self.qid,
            'surveyid': self.surveyid,
            'serviceprovider': self.serviceprovider,
            'name': self.name,
            'type': self.type,
            'options': json.loads(self.options),
            'qdescription': self.qdescription,
            'locked': bool(self.locked),
            'quizmode': bool(self.quizmode)}


    @classmethod
    def find_by_name(cls, name):
        '''
        Checks if a server inquiry to a specific surveyid already exists.
        '''
        return cls.query.filter_by(name=name).first()

    @classmethod
    def already_in_db(cls, surveyid, name):
        '''
        Checks if a server inquiry to a specific surveyid already exists.
        '''
        return cls.query.filter_by(surveyid=surveyid).filter_by(name=name).first()

    @classmethod
    def find_by_surveyid(cls, surveyid):
        '''
        Returns one server inquiry belonging to a specific surveyid.
        '''
        return cls.query.filter_by(surveyid=surveyid).first()

    @classmethod
    def find_all_by_surveyid(cls, surveyid):
        '''
        Returns all server inquiries belonging to a specific surveyid.
        '''
        return cls.query.filter_by(surveyid=surveyid).all()

    @classmethod ## TODO: implement function from the send reports file
    def delete_all_by_surveyid(cls, surveyid):
        '''
        TODO: needs to be implemented.
        '''
        pass
        # vorschlag von oli, ausprobieren
        # cls.query.filter_by(surveyid==surveyid).delete()
        #db.session.query(ServerInquiriesModel).filter(ServerInquiriesModel.surveyid==surveyid).delete()

    def save_to_db(self):
        '''
        Saves a server inquiry to the database.
        '''
        db.session.add(self) # a session is collection of objects we want to write into the db.
        db.session.commit()

    def delete_from_db(self):
        '''
        Deletes a server inquiry from the database.
        '''
        db.session.delete(self)
        db.session.commit()

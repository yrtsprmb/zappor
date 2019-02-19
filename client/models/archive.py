#models/archive.py
from db import db
from datetime import datetime


class ArchiveModel(db.Model):
    '''
    Defines the model for the archive.
    It gives an overview which surveys were processed by the client and helps to avoid duplicate reports.
    '''
    __tablename__ = "archive"
    id = db.Column(db.Integer, primary_key=True)
    surveyid = db.Column(db.String(100))              # id of the survey
    #modus                # for future use. Longitudinal surveys.
    #enddate              # for future use. Longitudinal surveys.
    #repeat               # for future use. Longitudinal surveys.
    processed = db.Column(db.Integer)                 # if the survey is answered
    entry = db.Column(db.String(50))                  # timestamp. when survey arrived from the server
    exit = db.Column(db.String(50))                   # timestamp, when survey was sent to the server

    def __init__(self, surveyid):
        self.surveyid = surveyid
        self.processed = False
        #self.longterm = False
        self.entry = datetime.now().strftime('%d.%m.%Y - %H:%M:%S')
        self.exit = ""

    def __repr__(self):
        '''
        Representation of an archive object.
        '''
        return f" surveyid: {self.surveyid}, processed: {bool(self.processed)}, entry: {self.entry}, exit: {self.exit}"

    @classmethod
    def find_by_surveyid(cls, surveyid):
        '''
        Returns an archive object by it's surveyid.
        '''
        return cls.query.filter_by(surveyid=surveyid).first()

    def save_to_db(self):
        '''
        Saves an archive object.
        '''
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        '''
        Deletes an archive object.
        '''
        db.session.delete(self)
        db.session.commit()

    def delete_archive():
        '''
        Deletes the whole archive.
        '''
        db.session.query(ArchiveModel).delete()
        db.session.commit()

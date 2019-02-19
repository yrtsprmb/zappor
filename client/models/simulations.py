#models/distributions.py
from db import db



class SimulationModel(db.Model):
    '''
    Defines the model for the archive.
    It gives an overview which surveys were processed by the client and helps to avoid duplicate reports.
    '''
    __tablename__ = "simulation"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))            # name of a question
    count = db.Column(db.Integer)              # type of a question
    average_irr = db.Column(db.String)         # possible answer options

    def __init__(self, name):
        self.name = name
        self.count = 0
        self.average_irr = ""


    def __repr__(self):
        '''
        Representation of an archive object.
        '''
        return f" name: {self.name}, count: {self.count}, irr: {self.average_irr}"

    @classmethod
    def find_by_name(cls, name):
        '''
        Returns an archive object by it's surveyid.
        '''
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        '''
        Saves an simulation object.
        '''
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        '''
        Deletes an simulation object.
        '''
        db.session.delete(self)
        db.session.commit()

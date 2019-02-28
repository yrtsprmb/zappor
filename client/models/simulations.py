#models/distributions.py
from db import db


class SimulationModel(db.Model):
    '''
    Defines the model for the simulation of IRR.
    '''
    __tablename__ = "simulation"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))            # name of a question
    count = db.Column(db.Integer)              # type of a question
    added_irr = db.Column(db.String)           # possible answer options
    average_irr = db.Column(db.String)         # possible answer options

    def __init__(self, name):
        self.name = name
        self.count = 0
        self.added_irr = ""
        self.average_irr = ""


    def __repr__(self):
        '''
        Representation of a simulation object.
        '''
        return f" name: {self.name}, count: {self.count}, added_irr: {self.added_irr}, average_irr: {self.average_irr}"

    @classmethod
    def find_by_name(cls, name):
        '''
        Returns an simulation object by it's name.
        '''
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        '''
        Saves a simulation object.
        '''
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        '''
        Deletes a simulation object.
        '''
        db.session.delete(self)
        db.session.commit()

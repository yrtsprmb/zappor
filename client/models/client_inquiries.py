#models/client_inquiries.py
import json
from db import db

class ClientInquiriesModel(db.Model):
    '''
    Defines the model for the internal representation of client inquiries.
    They represent all answers a client have to offer.
    Table will be created after first request was made after starting the app.
    '''
    __tablename__ = "client_inquiries"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))         # name of a question
    type = db.Column(db.String(15))         # type of a question
    options = db.Column(db.String)          # possible answer options
    answer = db.Column(db.String)           # answer in bits 1 true, 0 false
    prr_answer = db.Column(db.String)       # answer after prr
    irr_answer = db.Column(db.String)       # answer after irr
    qdescription = db.Column(db.String(300))# description of a question
    responded = db.Column(db.Integer)       # if answer was edited by the user
    locked = db.Column(db.Integer)          # if answer is locked by the user
    f = db.Column(db.Float(precision=5))    # privacy value f
    p = db.Column(db.Float(precision=5))    # privacy value p
    q = db.Column(db.Float(precision=5))    # privacy value q

    def __init__(self, name, type, options, answer, prr_answer, irr_answer, qdescription, responded, locked, f, p, q):
        self.name = name
        self.type = type
        self.options = options
        self.answer = answer
        self.prr_answer = prr_answer
        self.irr_answer = irr_answer
        self.qdescription = qdescription
        self.responded = responded
        self.locked = locked
        self.f = f
        self.p = p
        self.q = q

    def __repr__(self):
        '''
        Representation of a client inquiry object.
        '''
        return f" name: {self.name}, type: {self.type}, options: {self.options}, answer: {self.answer}, prr_answer: {self.prr_answer}, irr_answer: {self.irr_answer}, description: {self.qdescription}, responded: {bool(self.responded)}, locked: {bool(self.locked)}, f: {self.f}, p: {self.p}, q: {self.q}"

    def tojson(self):
        '''
        Returns a json representation of the client inquiry model.
        '''
        return {'name': self.name,
            'type': self.type,
            'options': json.loads(self.options),
            'answer': json.loads(self.answer),
            'prr_answer': json.loads(self.prr_answer),
            'irr_answer': json.loads(self.irr_answer),
            'qdescription': self.qdescription,
            'responded': bool(self.responded),
            'locked': bool(self.locked),
            'f': self.f,
            'p': self.p,
            'q': self.q,
            }

    @classmethod
    def find_by_name(cls, name):
        '''
        Returns a client inquiry called by its name.
        '''
        return ClientInquiriesModel.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, id):
        '''
        Returns a client inquiry called by its id.
        '''
        return ClientInquiriesModel.query.filter_by(id=id).first()

    def save_to_db(self):
        '''
        Saves a client inquiry to the database.
        '''
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        '''
        Deletes a client inquiry from the database.
        '''
        db.session.delete(self)
        db.session.commit()

    def delete_all_client_inquiries():
        '''
        Deletes all client inquiries.
        '''
        db.session.query(ClientInquiriesModel).delete()
        db.session.commit()

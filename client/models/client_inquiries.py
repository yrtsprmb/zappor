import json
from db import db

# represents all answers a client has to offer
class ClientInquiriesModel(db.Model):

    __tablename__ = "client_inquiries"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))         # name of a question
    type = db.Column(db.String(15))         # type of a question
    options = db.Column(db.String)          # possible answer options
    answer = db.Column(db.String)           # answer in bits 1 true, 0 false
    prr_answer = db.Column(db.String)       # answer after prr
    irr_answer = db.Column(db.String)       # answer after irr
    responded = db.Column(db.Integer)       # if answer was edited by the user
    locked = db.Column(db.Integer)          # if answer is locked by the user
    f = db.Column(db.Float(precision=5))    # privacy value f
    p = db.Column(db.Float(precision=5))    # privacy value p
    q = db.Column(db.Float(precision=5))    # privacy value q

    def __init__(self, name, type, options, answer, prr_answer, irr_answer, responded, locked, f, p, q):
        self.name = name
        self.type = type
        self.options = options
        self.answer = answer
        self.prr_answer = prr_answer
        self.irr_answer = irr_answer
        self.responded = responded
        self.locked = locked
        self.f = f
        self.p = p
        self.q = q

    #representation of the object for the GUI
    def __repr__(self):
        return f" name: {self.name}, type: {self.type}, options: {self.options}, answer: {self.answer}, prr_answer: {self.prr_answer}, irr_answer: {self.irr_answer}, responded: {bool(self.responded)}, locked: {bool(self.locked)}, f: {self.f}, p: {self.p}, q: {self.q}"

    #json representation of a client privacy data set
    def tojson(self):
        return {'name': self.name,
            'type': self.type,
            'options': json.loads(self.options),
            'answer': json.loads(self.answer),
            'prr_answer': json.loads(self.prr_answer),
            'irr_answer': json.loads(self.irr_answer),
            'responded': bool(self.responded),
            'locked': bool(self.locked),
            'f': self.f,
            'p': self.p,
            'q': self.q,
            }


    @classmethod
    def find_by_name(cls, name):
        return ClientInquiriesModel.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, id):
        return ClientInquiriesModel.query.filter_by(id=id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

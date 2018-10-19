import json
from db import db

# represents all answers a client has to offer
class AnswerModel(db.Model):

    __tablename__ = "answers"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    type = db.Column(db.String(15))
    options = db.Column(db.String)
    answer = db.Column(db.String)
    arandom = db.Column(db.String)
    locked = db.Column(db.Integer)
    f = db.Column(db.Float(precision=5))
    p = db.Column(db.Float(precision=5))
    q = db.Column(db.Float(precision=5))

    def __init__(self, name, type, options, answer, arandom, locked, f, p, q):
        self.name = name
        self.type = type
        self.options = options
        self.answer = answer
        self.arandom = arandom
        self.locked = locked
        self.f = f
        self.p = p
        self.q = q

    #json representation of a client privacy data set
    def tojson(self):
        return {'name': self.name,
            'type': self.type,
            'options': json.loads(self.options),
            'answer': json.loads(self.answer),
            'arandom': json.loads(self.arandom),
            'locked': self.locked,
            'f': self.f,
            'p': self.p,
            'q': self.q,
            }

    @classmethod
    def find_by_name(cls, name):
        return AnswerModel.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self) # session is collection of objects we want to write into the db
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

from db import db
import json

# represents all questions which a client can answer
class ListModel(db.Model):

    __tablename__ = "listen"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    liste = db.Column(db.String(1000))
    antworten = db.Column(db.Integer)

    def __init__(self, name, liste, antworten):
        self.name = name
        self.liste = liste
        self.antworten = antworten


    def json(self):
        return {'name': self.name, 'liste': json.loads(self.liste), 'antworten': json.loads(self.antworten)}

    @classmethod
    def find_by_name(cls, name):
        return ListModel.query.filter_by(name=name).first()

    def save_to_db(self): # saving to the db
        db.session.add(self) # session is collection of objects we want to write into the db
        db.session.commit()

    def delete_from_db(self): #item parameter is a dictionary of name and price
        db.session.delete(self) # session is collection of objects we want to write into the db
        db.session.commit()

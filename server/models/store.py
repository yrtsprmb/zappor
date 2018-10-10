from db import db

class StoreModel(db.Model):
    #infos for sqlalchemy
    __tablename__ = "stores"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    items = db.relationship('ItemModel', lazy='dynamic')

    def __init__(self,name):
        self.name = name


    # returns a json representation of the StoreModel
    def json(self):
        return {'name': self.name, 'items': [item.json() for item in self.items.all()] }
        #'items': self.items

    #find an item by its name, should be classmethod, because it returns an object of ItemModel
    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()


    def save_to_db(self): # saving to the db
        db.session.add(self) # session is collection of objects we want to write into the db
        db.session.commit()

    def delete_from_db(self): #item parameter is a dictionary of name and price
        db.session.delete(self) # session is collection of objects we want to write into the db
        db.session.commit()

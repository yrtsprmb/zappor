from db import db

class ItemModel(db.Model):
    #infos for sqlalchemy
    __tablename__ = "items"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    def __init__(self,name,price):
        self.name = name
        self.price = price

    # returns a json representation of the model
    def json(self):
        return {'name': self.name, 'price': self.price}


    #find an item by its name, should be classmethod, because it returns an object of ItemModel
    @classmethod
    def find_by_name(cls, name):
        return ItemModel.query.filter_by(name=name).first()
        # return cls.query.filter_by(name=name).first() also possible
        # SELECT * FROM items WHERE name=name LIMIT 1
        #returns an ItemModel object, that has self.name and self.price

    def save_to_db(self): # saving to the db
        db.session.add(self) # session is collection of objects we want to write into the db
        db.session.commit()

    def delete_from_db(self): #item parameter is a dictionary of name and price
        db.session.delete(self) # session is collection of objects we want to write into the db
        db.session.commit()

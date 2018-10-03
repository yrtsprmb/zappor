import sqlite3

class ItemModel:
    def __init__(self,name,price):
        self.name = name
        self.price = price

    # returns a json representation of the model
    def json(self):
        return {'name': self.name, 'price': self.price}


    #find an item by its name, should be classmethod, because it returns an object of ItemModel
    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return cls(row[0], row[1]) #works also cls(*row)


    def insert(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES (?,?)"
        cursor.execute(query, (self.name, self.price))

        connection.commit()
        connection.close()


    def update(self): #item parameter is a dictionary of name and price
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(query, (self.price, self.name)) #reihenfolge muss wie bei query eingehalten werden

        connection.commit()
        connection.close()
        return {'message': 'Item wurde upgedatet'}

import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required


############################################
######## Ressourcen Tutorial
############################################


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="Fehler in der Payload"
    )

    @jwt_required()
    def get(self, name):
        item = self.find_by_name(name)
        if item:
            return item
        return {'message': 'Item not found'}, 404

    #findet ein item bei seinem namen
    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {'item': {'name': row[0], 'price': row[1]}}


    def post(self, name):
        ## schreibt ein neues item in die db, falls es den namen nicht schon gibt
        # first, deal with errors
        if self.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400

        # second: do things
        data = Item.parser.parse_args()
        item = {'name': name, 'price': data['price']}

        try:
            self.insert(item)
        except:
            return {'message': "ein Fehler ist beim einfugen aufgetreten"}, 500 #internal server error
        return item, 201

    @classmethod
    def insert(cls,item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES (?,?)"
        cursor.execute(query, (item['name'], item['price']))

        connection.commit()
        connection.close()

    # loescht ein item aus der DB (noch nicht)
    def delete(self,name):
        if self.find_by_name(name):
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()

            query = "DELETE FROM items WHERE name=?"
            cursor.execute(query, (name,))

            connection.commit()
            connection.close()
            return {'message': 'Item deleted'}
        return {'message': 'not in db'}, 400



    def put(self,name):
        data = Item.parser.parse_args()
        item = self.find_by_name(name)
        updated_item = { 'name': name, 'item': data['price']}

        #data = request.get_json() #uebergibt python payolad an variable data
        if item is None:
            try:
                self.insert(updated_item)
            except:
                return {"message": "An error occured inserting"}, 500
        else:
            try:
                self.update(updated_item)
            except:
                return {"message": "An error occured updating"}, 500

        return item

    @classmethod
    def update(cls,item): #item parameter is a dictionary of name and price
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(query, (item['price'],item['name']))

        connection.commit()
        connection.close()
        return {'message': 'Item wurde upgedatet'}




class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        result = cursor.execute(query)
        items = []
        for row in result:
            items.append({'name': row[0], 'price': row[1]})

        connection.close()
        return {'items': items}

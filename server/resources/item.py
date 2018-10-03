import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.item import ItemModel

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

    # gibt ein item zurueck, das durch seinen namen gesucht wird
    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404


    ## schreibt ein neues item in die db, falls es den namen nicht schon gibt
    def post(self, name):
        # first, deal with errors
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400

        # second: do things
        data = Item.parser.parse_args()
        item = ItemModel(name, data['price'])

        try:
            item.insert()
        except:
            return {'message': "ein Fehler ist beim einfugen aufgetreten"}, 500 #internal server error
        return item.json(), 201


    # loescht ein item aus der DB
    def delete(self,name):
        if ItemModel.find_by_name(name):
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()

            query = "DELETE FROM items WHERE name=?"
            cursor.execute(query, (name,))

            connection.commit()
            connection.close()
            return {'message': 'Item deleted'}
        return {'message': 'not in db'}, 400

    # ueberschreibt den preis eines items, wenn dieses vorhanden ist, ansonsten legt es ein neues item an
    def put(self,name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        updated_item = ItemModel(name, data['price'])

        #data = request.get_json() #uebergibt python payolad an variable data
        if item is None:
            try:
                updated_item.insert()
            except:
                return {"message": "An error occured inserting"}, 500
        else:
            try:
                updated_item.update()
            except:
                return {"message": "An error occured updating"}, 500
        return updated_item.json()

# gibt eine Liste aller Items an
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

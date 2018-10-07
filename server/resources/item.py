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
        return {'message': 'Item not found'}, 404 #not found


    ## schreibt ein neues item in die db, falls es den namen nicht schon gibt
    def post(self, name):
        # first, deal with errors
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400 #bad request

        # second: do things
        data = Item.parser.parse_args()
        item = ItemModel(name, data['price'])

        try:
            item.save_to_db()
        except:
            return {'message': "ein Fehler ist beim einfugen aufgetreten"}, 500 #internal server error
        return item.json(), 201


    # loescht ein item aus der DB
    def delete(self,name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message': 'Item deleted'}
        return {'message': 'not in db'}, 400


    # ueberschreibt den preis eines items, wenn dieses vorhanden ist, ansonsten legt es ein neues item an
    def put(self,name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        #data = request.get_json() #uebergibt python payolad an variable data
        if item is None:
            item = ItemModel(name, data['price']) # da nichts gefunden wurde, wird ein neues item kreiert
        else:
            item.price = data['price']

        item.save_to_db()

        return item.json()

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

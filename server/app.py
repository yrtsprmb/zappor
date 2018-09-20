from flask import Flask, request
from flask_restful import Resource, Api, reqparse

from flask_jwt import JWT, jwt_required
from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'zappor'

api = Api(app)


jwt = JWT(app, authenticate, identity)

items = []
umfragen = []
umfrageids = ['helgassurvey']
offeneumfragen = []


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
    
    #@jwt_required()
    def get(self, name):
        item = next(filter(lambda x: x['name'] == item,items), None)
        return {'item': item}, 200 if item is not none else 404

    def post(self, name):
        if next(filter(lambda x: x['name'] == name,items), None):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400

        data = request.get_json()
        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201

    def delete(self,name):
        global items
        items = list(filter(lambda x: x['name'] !=name, items))
        return {'message': 'Item deleted'}

    def put(self,name):
        data = Item.parser.parse_args()

        data = request.get_json() #uebergibt python payolad an variable data
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        else:
            item.update(data)
        return item


class ItemList(Resource):
    def get(self):
        return {'items': items}

############################################
######## Ressourcen nach aussen fuer die Clients
############################################


class SurveyAvailable(Resource):
    def get(self):
        # check if there is a survey and send it back if yes

        return { 'umfragen': umfragen}
        #return {'survey': None}, 404


class ReceiveSurvey(Resource):
    # if survey exists, save it to the id in the database, if not discard
    def post(self, name):
        #if next(filter(lambda x: x['surveyid'] == item,items), none)


        data = request.get_json()
        survey = {'surveyid': data['surveyid'], 'service-provider': data['service-provider'], 'questions': data['questions']}
        umfragen.append(survey)
        return survey, 201

############################################
######## Ressourcen fur den Serviceprovider
############################################

class ManageReports(Resource):
    #Umfragen werden verwaltet
    pass


class CreateSurvey(Resource):
    #eine Umfragen wird generiert und in die DB Gespeichert
    def post(self,name):
        pass


class DeleteSurvey(Resource):
    #eine Umfrage wird anhand ihrer ID geloescht,
    def delete(self,name):
        #if id exists in db, delete it, otherwise error message
        pass

######## Ressourcen werden zur api hinzugefuegt

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
#######
api.add_resource(SurveyAvailable, '/surveyavailable')
api.add_resource(ReceiveSurvey, '/receivesurvey/<string:name>')


app.run(port=5000,debug=True)

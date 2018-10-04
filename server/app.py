from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity

# Import der Resourcen
from resources.user import UserRegister
from resources.item import Item, ItemList
# eigene Resourcen
from resources.survey import Survey, SurveyList, SurveyAvailable
from resources.report import Report

app = Flask(__name__)
app.secret_key = 'zappor'
api = Api(app)

jwt = JWT(app, authenticate, identity)

######## Ressourcen Tutorial
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

######## Ressourcen Login/Registrierung
api.add_resource(UserRegister, '/register')

####### Resourcen vom Server nach aussen zum Client
api.add_resource(Report, '/report/<string:surveyid>') # client -> server, sends an Report
api.add_resource(SurveyAvailable, '/surveyavailable') # server -> client, server answers with available Surveys


####### Resourcen vom Server nach innen zum Serviceprovider
api.add_resource(Survey, '/survey/<string:name>') #  create & delete surveys
api.add_resource(SurveyList, '/surveys') # lists all available surveys


####### Server wird nur gestartet, wenn app.py ausgefuehrt wird
if __name__ == '__main__':
    app.run(port=5000,debug=True)

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity

# Import der Resourcen
from resources.user import UserRegister
from resources.item import Item, ItemList
# eigene Resourcen
from resources.survey import SurveyAvailable, ReceiveSurvey, ManageReports, CreateSurvey, DeleteSurvey
from resources.survey import Survey
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
api.add_resource(SurveyAvailable, '/surveyavailable')
api.add_resource(ReceiveSurvey, '/receivesurvey/<string:name>')

api.add_resource(Report, '/receivereport/<string:surveyid>')

####### Resourcen vom Server nach innen zum Serviceprovider
api.add_resource(Survey, '/survey/<string:surveyname>')

api.add_resource(ManageReports, '/surveys')
api.add_resource(DeleteSurvey, '/delete/<string:name>')

####### Server wird nur gestartet, wenn app.py ausgefuehrt wird
if __name__ == '__main__':
    app.run(port=5000,debug=True)

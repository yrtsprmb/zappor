from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity

# Import der Resourcen
from resources.user import UserRegister
from resources.item import Item, ItemList
# eigene Resourcen
from resources.survey import Survey, SurveyList, SurveyAvailable
from resources.report import Report, ReportList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db' # tells sqlachemy where the database is
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # to save resources, sqlalchmey has its own modification tracker
app.secret_key = 'zappor'
api = Api(app)

jwt = JWT(app, authenticate, identity) # responsible for the /auth path

######## Ressourcen Tutorial
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

######## Ressourcen Login/Registrierung
api.add_resource(UserRegister, '/register')

####### Resourcen vom Server nach aussen zum Client
api.add_resource(Report, '/report/<string:surveyid>') # client -> server, sends an Report
api.add_resource(SurveyAvailable, '/surveyavailable') # server -> client, server answers with available Surveys

####### Internal apis - resourcen from server to the serviceprovider
api.add_resource(Survey, '/survey/<string:surveyid>') #  create & delete surveys
api.add_resource(SurveyList, '/surveys') # lists all available surveys

####### Resourcen for API tests
api.add_resource(ReportList, '/reports') # lists all reports in the db


####### Server wird nur gestartet, wenn app.py ausgefuehrt wird
####### Startet SQLAlchemy fuer den Server
if __name__ == '__main__':
    from db import db
    db.init_app(app)

    app.run(port=5000,debug=True)

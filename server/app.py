from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity

# Import der Resourcen
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList
# eigene Resourcen
from resources.survey import Survey, SurveyList, SurveyAvailable, SurveyStatus
from resources.report import Report, ReportList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db' # tells sqlachemy where the database is
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # to save resources, sqlalchmey has its own modification tracker
app.secret_key = 'zappor'
api = Api(app)

#creates tables on startup when first request ist made
@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWT(app, authenticate, identity) # responsible for the /auth path

#Ressources tutorial
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')

#Ressources login/registration
api.add_resource(UserRegister, '/register')

#Server resources for the client
api.add_resource(Report, '/report/<string:surveyid>') # client -> server, sends an Report
api.add_resource(SurveyAvailable, '/surveyavailable') # server -> client, server answers with available Surveys

####### Internal apis - resourcen from server to the serviceprovider
api.add_resource(Survey, '/survey/<string:surveyid>') #  create & delete surveys
api.add_resource(SurveyList, '/surveys') # lists all available surveys
api.add_resource(SurveyStatus, '/surveystatus/<string:surveyid>') # changes status of a survey

####### Resourcen for API tests
api.add_resource(ReportList, '/reports') # lists all reports in the db


####### Server only starts when it will be executed over the file app.py
####### Startet SQLAlchemy fuer den Server
if __name__ == '__main__':
    from db import db
    db.init_app(app)

    app.run(port=5000,debug=True)

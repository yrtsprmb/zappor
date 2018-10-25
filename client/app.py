from flask import Flask
from flask_restful import Api
from db import db
from flask_sqlalchemy import SQLAlchemy

#import of the resources

from resources.client_inquiries import ClientInquiries, ListClientInquiries
from resources.server_inquiries import ServerInquiries, ListServerInquiries

from resources.surveys import Survey, ListSurveys
from resources.clientconf import ClientConf

from resources.requestsurveys import RequestSurvey

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clientdata.db' # tells sqlachemy where the database is
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#db = SQLAlchemy(app)
app.secret_key = 'zappor'
api = Api(app)

#creates tables on startup when first request ist made
@app.before_first_request
def create_tables():
    db.create_all()


#Rest Resources for Client
api.add_resource(ClientInquiries, '/ci/<string:name>')
api.add_resource(ListClientInquiries, '/lci')

api.add_resource(ServerInquiries, '/si/<string:name>')
api.add_resource(ListServerInquiries, '/lsi')


api.add_resource(Survey, '/survey/<string:surveyid>')
api.add_resource(ListSurveys, '/surveys')

api.add_resource(ClientConf, '/configuration/<string:clientname>')

#test for requesting
api.add_resource(RequestSurvey, '/requestsurveys/')

####### Server only starts when it will be executed over the file app.py
if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5001,debug=True)

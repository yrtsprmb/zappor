from flask import Flask
from flask_restful import Api

# Import der Resourcen
from resources.questions import Question, ListQuestions
from resources.answers import Answer, ListAnswers
from resources.surveys import Survey, ListSurveys
#from resources.settings import Settings


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clientdata.db' # tells sqlachemy where the database is
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'zappor'
api = Api(app)

#creates tables on startup when first request ist made
@app.before_first_request
def create_tables():
    db.create_all()


#Rest Resources for Client
api.add_resource(Answer, '/answer/<string:name>')
api.add_resource(ListAnswers, '/answers')

api.add_resource(Question, '/question/<string:qname>')
api.add_resource(ListQuestions, '/questions')

api.add_resource(Survey, '/survey/<string:surveyid>')
api.add_resource(ListSurveys, '/surveys')

#api.add_resource(Settings, '/settings/<string:clientname>')


####### Server only starts when it will be executed over the file app.py
if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5001,debug=True)

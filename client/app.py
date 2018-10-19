from flask import Flask
from flask_restful import Api

# Import der Resourcen
from resources.questions import Question, ListQuestions
from resources.answers import Answer, ListAnswers
from resources.list import Liste, ListAll

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clientdata.db' # tells sqlachemy where the database is
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'zappor'
api = Api(app)

#creates tables on startup when first request ist made
@app.before_first_request
def create_tables():
    db.create_all()


#Ressources Testing
api.add_resource(Liste, '/liste/<string:name>')
api.add_resource(ListAll, '/listen')

#Rest Resources for Client
api.add_resource(Answer, '/answer/<string:name>')
api.add_resource(ListAnswers, '/answers')
api.add_resource(Question, '/question/<string:qname>')
api.add_resource(ListQuestions, '/questions')

####### Server only starts when it will be executed over the file app.py
if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5001,debug=True)

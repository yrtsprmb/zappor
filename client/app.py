from flask import Flask, render_template, url_for, redirect, flash
from flask_restful import Api
from db import db
from flask_sqlalchemy import SQLAlchemy

#import of the resources
from resources.client_inquiries import ClientInquiries, ListClientInquiries
from resources.server_inquiries import ServerInquiries, ListServerInquiries

from resources.surveys import Survey, ListSurveys
from resources.clientconf import ClientConf

### TEST ###############################################
## imports for testing
########################################################


#TEST formulare:
from forms import AddForm, DelForm, AddOwnerForm, RapporForm, PersonalForm
from web import Puppy, Owner, PersonalModel, RapporModel


from resources.requestsurveys import RequestSurvey
from resources.sendreports import SendReport

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


### REST ###############################################
## REST resources for the client
########################################################

api.add_resource(ClientInquiries, '/ci/<string:name>')
api.add_resource(ListClientInquiries, '/lci')

api.add_resource(ServerInquiries, '/si/<string:name>')
api.add_resource(ListServerInquiries, '/lsi')

api.add_resource(Survey, '/survey/<string:surveyid>')
api.add_resource(ListSurveys, '/surveys')

api.add_resource(ClientConf, '/configuration/<string:clientname>')

#test for requesting
api.add_resource(RequestSurvey, '/requestsurveys/')
api.add_resource(SendReport, '/sendreports/')

### views ##############################################
## routes for the web GUI
########################################################

@app.route('/')
@app.route('/index')
def index():
    return render_template('home.html', title='Home')

@app.route('/config')
def client_config():
    return render_template('client_config.html', title='Configuration')

@app.route('/show')
def show_inquiries():
    from models.server_inquiries import ServerInquiriesModel
    from models.client_inquiries import ClientInquiriesModel
    answers = ClientInquiriesModel.query.all()
    questions = ServerInquiriesModel.query.all()
    return render_template('show_inquiries.html', answers=answers, questions=questions, title='list of inquiries')

@app.route('/test')
def test():
    user = {'username': 'Miguel'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('test.html', title='Home of the Zepp', user=user, posts=posts)

@app.route('/privacy',methods=['GET','POST'])
def add_privacy():
    form = RapporForm()

    if form.validate_on_submit():
        p = form.p.data
        q = form.q.data
        r = form.r.data

        # Add new Puppy to database
        new_rap = RapporModel(p,q,r)
        db.session.add(new_rap)
        db.session.commit()

        return redirect(url_for('list_all'))

    return render_template('privacysettings_a.html',form=form, title='privacy settings')


@app.route('/listall')
def list_all():
    # Grab a list of puppies from database.
    puppies = Puppy.query.all()
    rapport = RapporModel.query.all()

    return render_template('listall.html', puppies=puppies, rapport=rapport)


####### Server only starts when it will be executed over the file app.py
if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5001,debug=True)

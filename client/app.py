from flask import Flask, render_template, url_for, redirect, flash, request
from flask_restful import Api
from db import db
from flask_sqlalchemy import SQLAlchemy

#import of the resources
from resources.client_inquiries import ClientInquiries, ListClientInquiries
from resources.server_inquiries import ServerInquiries, ListServerInquiries

from resources.surveys import Survey, ListSurveys
from resources.clientconf import ClientConf

### Threading ####################################################
## imports for autojobs
##################################################################
import threading
import time
import requests
from forms import RequestSurveyTestForm


### TEST #########################################################
## imports for testing
##################################################################

#TEST formulare:
#from forms import RapporForm
#from web import RapporModel

# for requests
from resources.request_surveys import RequestSurvey
from resources.send_reports import SendReport
from resources.match_inquiries import MatchInquiries


### app #########################################################
## app and db settings
##################################################################

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clientdata.db' # tells sqlachemy where the database is
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'zappor'
api = Api(app)

#creates tables on startup when first request ist made
@app.before_first_request
def create_tables():
    db.create_all()

#starts background jobs
#@app.before_first_request
def activate_job():
    def request_survey():
        while True:
            print("Request Survey")
            r = requests.get('http://127.0.0.1:5001/requestsurveys/')
            time.sleep(3)
    thread_survey = threading.Thread(target=request_survey)
    thread_survey.start()

    def send_report():
        while True:
            print("Send Report")
            r = requests.get('http://127.0.0.1:5001/sendreports/')
            time.sleep(6)
    thread_report = threading.Thread(target=send_report)
    thread_report.start()


### error pages ##################################################
## Register error pages
##################################################################

from handlers import error_pages
app.register_blueprint(error_pages)


### REST #########################################################
## REST resources for the client
## these are for testing, but can be also used for other
## ways to interact with the client
##################################################################

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
api.add_resource(MatchInquiries, '/match/')


### views ########################################################
## routes for the web GUI
## TODO: move them to an own py. file
##################################################################

@app.route('/')
@app.route('/index')
def index():
    return render_template('home.html', title='Home')


@app.route('/show')
def show_inquiries():
    from models.server_inquiries import ServerInquiriesModel
    from models.client_inquiries import ClientInquiriesModel
    from models.reports import ReportModel

    answers = ClientInquiriesModel.query.all()
    questions = ServerInquiriesModel.query.all()
    reports = ReportModel.query.all()
    return render_template('show_inquiries.html', answers=answers, questions=questions, reports=reports, title='list of inquiries')


@app.route('/privacy',methods=['GET','POST'])
def add_privacy():
    from models.rappor import RapporModel
    from forms import RapporForm

    form = RapporForm()

    if form.validate_on_submit():
        f = form.f.data
        p = form.p.data
        q = form.q.data

        # Add new Puppy to database
        new_rap = RapporModel(f,p,q)
        db.session.add(new_rap)
        db.session.commit()

        return redirect(url_for('list_all'))
    return render_template('privacysettings_a.html',form=form, title='privacy settings a')


@app.route('/privacy_b', methods=['GET','POST'])
def add_privacy_b():
    return render_template('privacysettings_b.html', title='privacy settings b')


@app.route('/config')
def client_config():
    return render_template('client_config.html', title='Configuration')


@app.route('/tests', methods=['GET','POST'])
def tests():
    import requests
    from forms import RequestSurveyTestForm

    form = RequestSurveyTestForm()
    flash("horst")
    if form.validate_on_submit():
        if 'submit_request' in request.form:
            print("Request Survey button pressed") #debug
            r = requests.get('http://127.0.0.1:5001/requestsurveys/')

        elif 'submit_report' in request.form:
            print("Send report button pressed") #debug
            r = requests.get('http://127.0.0.1:5001/sendreport/')

        elif 'submit_match' in request.form:
            print("Match inquiries button pressed") #debug
            r = requests.get('http://127.0.0.1:5001/match/')


    return render_template('tests.html', form=form, title='client tests')



### oldstuff ###########################################
## not needed in future
########################################################


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

####### Server only starts when it will be executed over the file app.py
if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5001,debug=True)

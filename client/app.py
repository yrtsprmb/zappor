from flask import Flask, render_template, url_for, redirect, flash, request, abort
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

# import of configurations:
from intern.config import repeat_send_reports, repeat_request_surveys, serviceprovider_reports, serviceprovider_surveys

# for requests
from resources.request_surveys import RequestSurvey
from resources.send_reports import SendReport
from resources.match_inquiries import MatchInquiries
from resources.reports import Report, ListReports



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
            r = requests.get(serviceprovider_surveys)
            time.sleep(repeat_request_surveys)
    thread_survey = threading.Thread(target=request_survey)
    thread_survey.start()

    def send_report():
        while True:
            print("Send Report")
            r = requests.get(serviceprovider_reports)
            time.sleep(repeat_send_reports)
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

api.add_resource(ListReports, '/listreports/')

api.add_resource(ClientConf, '/configuration/<string:clientname>')

#test for requesting
api.add_resource(RequestSurvey, '/requestsurveys/')
api.add_resource(SendReport, '/sendreports/')
api.add_resource(MatchInquiries, '/match/')
api.add_resource(Report, '/reports/<string:surveyid>')



#############################################################
# testing:
# allows full access to the values through the REST API
#############################################################

from resources.client_inquiries import TestClientInquiries
api.add_resource(TestClientInquiries, '/ci_test/<string:name>')

from resources.server_inquiries import TestServerInquiries
api.add_resource(TestServerInquiries, '/si_test/<string:name>')

### views ########################################################
## routes for the web GUI
## TODO: move them to an own py. file
##################################################################

@app.route('/')
@app.route('/index')
def index():
    return render_template('home.html', title='Home')


@app.route('/inquiries/')
def inquiries_list():
    from models.client_inquiries import ClientInquiriesModel
    from forms import ClientInquiryForm

    inqs = (db.session.query(ClientInquiriesModel).order_by(ClientInquiriesModel.id.desc()).all())
    return render_template('inquiries/inquiries.html', inqs=inqs, title='list of inquiries')


@app.route('/inquiries/<int:id>/', methods=['GET','POST'])
def inquiries_detail(id):
    from models.client_inquiries import ClientInquiriesModel
    from forms import ClientInquiryForm

    inq = db.session.query(ClientInquiriesModel).get(id)
    if inq is None:
        abort(404)

    form = ClientInquiryForm()

    if form.validate_on_submit():
        answer = form.answer.data
        locked = form.locked.data
        f = form.f.data
        p = form.p.data
        q = form.q.data

        inq.answer = answer

        inq.responded = True # if a answer was given, the anwer will set responded by the user
        inq.locked = locked
        inq.f = f
        inq.p = p
        inq.q = q
        db.session.commit()

    return render_template('inquiries/client_inquiry.html', inq=inq, form=form, title='question')

@app.route('/inquiries/create/')
def inquiries_create():
    from models.client_inquiries import ClientInquiriesModel
    from forms import InquiryForm

    #inqs = (db.session.query(ClientInquiriesMo
    #del).order_by(ClientInquiriesModel.id.desc()).all())
    return render_template('inquiries/inquiries.html', inqs=inqs, title='list of inquiries')
    #
    #
    # from forms import NewSurveyForm
    # from models.survey import SurveyModel

    # form = NewSurveyForm()
    # if form.validate_on_submit():
    #     newsurvey = SurveyModel(surveyid = form.surveyid.data,
    #                             serviceprovider = form.serviceprovider.data,
    #                             surveyname = form.surveyname.data,
    #                             status = form.status.data,
    #                             comment = form.comment.data,
    #                             questions = form.questions.data)
    #     newsurvey.save_to_db()
    #     flash("New survey created")
    #     return redirect('/index')
    # return render_template('create_survey.html', form=form, title='Create a new survey')


@app.route("/inquiries/<int:id>/delete", methods=['POST'])
def inquiries_delete(id):
    from models.client_inquiries import ClientInquiriesModel
    from forms import InquiryForm

    inq = ClientInquiriesModel.query.get_or_404(id)
    inq.delete_from_db()
    flash('inquiry has been deleted.')
    return redirect(url_for('inquiries_list'))




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
            r = requests.get('http://127.0.0.1:5001/sendreports/')

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

#app.py

from flask import Flask, render_template, url_for, redirect, flash, abort
from flask_restful import Api
from flask_jwt import JWT

#authorization (if needed)
from security import authenticate, identity

# import of resources
from resources.user import UserRegister
from resources.surveys import Survey, ListSurveys, AvailableSurveys
from resources.reports import Report, ListReports
from resources.summaries import Summary, ListSummaries, CreateSummaries

from internal.config import secretkey_config, serviceprovider_config



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///serverdata.db' # tells sqlachemy where the database is
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # to save resources, sqlalchmey has its own modification tracker
app.secret_key = secretkey_config
api = Api(app)

#creates tables on startup when first request ist made
@app.before_first_request
def create_tables():
    '''
    Creates all needed tables (if not already existing) after the first request was made.
    '''
    db.create_all()

#authentication (prepared but not fully implemented)
jwt = JWT(app, authenticate, identity) # responsible for the /auth path

### error pages ##################################################
## Register error pages
##################################################################

from handlers import error_pages
app.register_blueprint(error_pages)

##################################################################
## Client Ressources (external ressources)
##################################################################

#Ressources login/registration
api.add_resource(UserRegister, '/register')

#Server resources for the client
api.add_resource(Report, '/reports/<string:surveyid>') # client -> server, sends an Report
api.add_resource(ListReports, '/listreports') # lists all reports in the db

# server -> client, server answers with available Surveys
api.add_resource(AvailableSurveys, '/availablesurveys')

####### Internal apis - resourcen from server to the serviceprovider
api.add_resource(Survey, '/surveys/<string:surveyname>') # create & delete surveys
api.add_resource(ListSurveys, '/listsurveys') # lists all available surveys

api.add_resource(Summary, '/rest/smmrs/<string:surveyid>') # GET, POST & DELETE for summaries.
api.add_resource(ListSummaries, '/rest/listsummaries') # GET for listing all available summaries
api.add_resource(CreateSummaries, '/rest/smmrs/create/<string:surveyid>') # Creates summaries for a surveyid.


### views ########################################################
## routes for the web GUI
## TODO: move them to an own py. file
##################################################################

@app.route('/')
@app.route('/index')
def index():
    '''
    Homepage (web GUI).
    '''
    return render_template('home.html', title='Home')


@app.route('/srvys/')
def surveys_list():
    '''
    Lists all surveys (web GUI).
    '''
    from models.surveys import SurveyModel
    surveys = (db.session.query(SurveyModel).order_by(SurveyModel.id.desc()).all())
    return render_template('srvys/surveys.html', surveys=surveys, title='list of surveys')


@app.route('/srvys/<int:id>/', methods=['GET','POST'])
def survey_detail(id):
    '''
    Shows the details of a survey specified by its id (web GUI).
    '''
    from models.surveys import SurveyModel
    from forms import SurveyForm

    srvy = db.session.query(SurveyModel).get(id)
    if srvy is None:
        abort(404)

    form = SurveyForm()

    if form.validate_on_submit():
            if (srvy.status == 'created' or srvy.status == 'active') and (form.status.data == 'active' or form.status.data == 'done'):
                old_status = srvy.status
                srvy.status = form.status.data
                srvy.save_to_db()
                flash("Status changed")
                return redirect(url_for('surveys_list'))

    return render_template('srvys/survey.html', srvy=srvy, form=form, title='survey details')


@app.route('/srvys/create', methods=['GET','POST'])
def survey_create():
    '''
    Creates a survey (web GUI).
    '''
    from models.surveys import SurveyModel
    from forms import CreateSurveyForm

    form = CreateSurveyForm()
    if form.validate_on_submit():
        srvy = SurveyModel(surveyid = serviceprovider_config,
                                serviceprovider = serviceprovider_config,
                                surveyname = form.surveyname.data,
                                status = form.status.data,
                                sdescription = form.sdescription.data,
                                questions = form.questions.data)
        srvy.save_to_db()
        flash("Survey created")
        return redirect(url_for('surveys_list'))
    return render_template('srvys/create.html', form=form, title='create a new survey')


@app.route('/srvys/<int:id>/delete', methods=['POST'])
def survey_delete(id):
    '''
    Deletes a survey (web GUI).
    '''
    from models.surveys import SurveyModel
    from forms import SurveyForm

    srvy = SurveyModel.query.get_or_404(id)
    srvy.delete_from_db()
    flash('survey has been deleted.')
    return redirect(url_for('surveys_list'))


@app.route('/settings', methods=['GET','POST'])
def settings():
    '''
    TODO: Server setting (web GUI).
    '''
    from models.config import ConfigurationModel
    from forms import LoginForm
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('settings.html', form=form, title='settings')


@app.route('/internaldata')
def internaldata():
    '''
    This is for testing.
    It shows all client-, and server inquiries and reports which are stored in the client database.
    '''
    from models.reports import ReportModel
    from models.surveys import SurveyModel
    from models.summaries import SummaryModel

    rprts = ReportModel.query.all()
    smmrs = SummaryModel.query.all()
    srvys = SurveyModel.query.all()

    return render_template('internal_data.html', rprts=rprts, smmrs=smmrs, srvys=srvys, title='internal data')


@app.route('/tests', methods=['GET','POST'])
def tests():
    '''
    Testing options over the web GUI. Works only for hardcoded testsurvey at the moment.
    '''
    import requests
    from forms import TestForm

    form = TestForm()
    flash("test")
    if form.validate_on_submit():
            print("generate summary button pressed") #debug
            r = requests.get('http://localhost:5000/rest/smmrs/create/testsurvey')

    return render_template('tests.html', form=form, title='server tests')


@app.route('/info')
def info():
    '''
    Infomation page (web GUI).
    '''
    return render_template('info.html')


@app.route('/<string:id>/histograms', methods=['GET','POST'])
def histogram(id):
    '''
    Test: Histogram (web GUI).
    '''
    from forms import SummaryForm

    form = SummaryForm()
    if form.validate_on_submit():
        return redirect(url_for('surveys_list'))
    return render_template('smmrs/histograms.html', form=form, title='summaries', survey_id=id)


##################################################################
## Server only starts when it will be executed over the file app.py
##################################################################
if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000,debug=True)

from flask import Flask, render_template, url_for, redirect, flash
from flask_restful import Api
from flask_jwt import JWT

#authorization (if needed)
from security import authenticate, identity

# import of resources
from resources.user import UserRegister
from resources.survey import Survey, ListSurveys, AvailableSurveys, SurveyStatus
from resources.report import Report, ListReports



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///serverdata.db' # tells sqlachemy where the database is
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # to save resources, sqlalchmey has its own modification tracker
app.secret_key = 'zappor'
api = Api(app)

#creates tables on startup when first request ist made
@app.before_first_request
def create_tables():
    db.create_all()

#authentication (prepared but not fully implemented)
jwt = JWT(app, authenticate, identity) # responsible for the /auth path

#Register error pages
from handlers import error_pages
app.register_blueprint(error_pages)

##################################################################
######## Client Ressources (external ressources)
##################################################################


#Ressources login/registration
api.add_resource(UserRegister, '/register')

#Server resources for the client
api.add_resource(Report, '/reports/<string:surveyid>') # client -> server, sends an Report
api.add_resource(AvailableSurveys, '/availablesurveys') # server -> client, server answers with available Surveys

####### Internal apis - resourcen from server to the serviceprovider
api.add_resource(Survey, '/surveys/<string:surveyid>') #  create & delete surveys
api.add_resource(ListSurveys, '/listsurveys') # lists all available surveys
api.add_resource(SurveyStatus, '/surveystatus/<string:surveyid>') # changes status of a survey

####### Resources for API tests
api.add_resource(ListReports, '/listreports') # lists all reports in the db


### views ########################################################
## routes for the web GUI
## TODO: move them to an own py. file
##################################################################

@app.route('/')
@app.route('/index')
def index():
    return render_template('home.html', title='Home')

@app.route('/list', methods=['GET','POST'])
def list_surveys():
    from models.survey import SurveyModel

    surveys = SurveyModel.query.all()
    return render_template('list_surveys.html', surveys=surveys, title='list of surveys')


@app.route('/create', methods=['GET','POST'])
def create_survey():
    from forms import NewSurveyForm
    from models.survey import SurveyModel

    form = NewSurveyForm()
    if form.validate_on_submit():
        newsurvey = SurveyModel(surveyid = form.surveyid.data,
                                serviceprovider = form.serviceprovider.data,
                                surveyname = form.surveyname.data,
                                status = form.status.data,
                                comment = form.comment.data,
                                questions = form.questions.data)
        newsurvey.save_to_db()
        flash("New survey created")
        return redirect('/index')
    return render_template('create_survey.html', form=form, title='Create a new survey')


@app.route('/evaluate', methods=['GET','POST'])
def evaluate_survey():
    from forms import LoginForm

    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('evaluate_survey.html', form=form, title='Survey Evaluation')


####### Server only starts when it will be executed over the file app.py
####### Startet SQLAlchemy fuer den Server
if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000,debug=True)

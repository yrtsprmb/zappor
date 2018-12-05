from flask import Flask, render_template, url_for, redirect, flash, abort
from flask_restful import Api
from flask_jwt import JWT

#authorization (if needed)
from security import authenticate, identity

# import of resources
from resources.user import UserRegister
from resources.survey import Survey, ListSurveys, AvailableSurveys
from resources.report import Report, ListReports
from internal.config import secretkey_config, serviceprovider_config


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///serverdata.db' # tells sqlachemy where the database is
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # to save resources, sqlalchmey has its own modification tracker
app.secret_key = secretkey_config
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
## Client Ressources (external ressources)
##################################################################


#Ressources login/registration
api.add_resource(UserRegister, '/register')

#Server resources for the client
api.add_resource(Report, '/reports/<string:surveyid>') # client -> server, sends an Report
api.add_resource(ListReports, '/listreports') # lists all reports in the db

api.add_resource(AvailableSurveys, '/availablesurveys') # server -> client, server answers with available Surveys

####### Internal apis - resourcen from server to the serviceprovider
api.add_resource(Survey, '/surveys/<string:surveyname>') #  create & delete surveys
api.add_resource(ListSurveys, '/listsurveys') # lists all available surveys



### views ########################################################
## routes for the web GUI
## TODO: move them to an own py. file
##################################################################

@app.route('/')
@app.route('/index')
def index():
    return render_template('home.html', title='Home')


@app.route('/srvys/')
def surveys_list():
    from models.survey import SurveyModel
    surveys = (db.session.query(SurveyModel).order_by(SurveyModel.id.desc()).all())
    return render_template('srvys/surveys.html', surveys=surveys, title='list of surveys')


@app.route('/srvys/<int:id>/', methods=['GET','POST'])
def survey_detail(id):
    from models.survey import SurveyModel
    from forms import SurveyForm

    srvy = db.session.query(SurveyModel).get(id)
    if srvy is None:
        abort(404)

    form = SurveyForm()

    #if form.validate_on_submit():
        # answer = form.answer.data
        # locked = form.locked.data
        # f = form.f.data
        # p = form.p.data
        # q = form.q.data
        #
        # inq.answer = answer
        #
        # inq.responded = True # if a answer was given, the anwer will set responded by the user
        # inq.locked = locked
        # inq.f = f
        # inq.p = p
        # inq.q = q
        # db.session.commit()
    return render_template('srvys/survey.html', srvy=srvy, form=form, title='survey details')


@app.route('/srvys/<int:id>/delete', methods=['POST'])
def survey_delete(id):
    from models.survey import SurveyModel
    from forms import SurveyForm

    srvy = SurveyModel.query.get_or_404(id)
    srvy.delete_from_db()
    flash('survey has been deleted.')
    return redirect(url_for('surveys_list'))


@app.route('/srvys/create', methods=['GET','POST'])
def survey_create():
    from models.survey import SurveyModel
    from forms import CreateSurveyForm

    form = CreateSurveyForm()
    if form.validate_on_submit():
        srvy = SurveyModel(surveyid = serviceprovider_config,
                                serviceprovider = serviceprovider_config,
                                surveyname = form.surveyname.data,
                                status = form.status.data,
                                comment = form.comment.data,
                                questions = form.questions.data)
        srvy.save_to_db()
        flash("Survey created")
        return redirect('/index')
    return render_template('srvys/create.html', form=form, title='create a new survey')



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

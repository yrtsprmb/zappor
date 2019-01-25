#app.py
from flask import Flask, render_template, url_for, redirect, flash, request, abort
from flask_restful import Api
from db import db
from flask_sqlalchemy import SQLAlchemy

#import of the resources
from resources.client_inquiries import ClientInquiries, ListClientInquiries
from resources.server_inquiries import ServerInquiries, ListServerInquiries



### Threading ####################################################
## imports for autojobs
##################################################################
import threading
import time
import requests


### Requests and configunration ##################################
## imports for REST resources and config.py
##################################################################

# import of configurations:
from internal.config import secretkey_config, repeat_send_reports, repeat_request_surveys, serviceprovider_reports, serviceprovider_surveys
from internal.config import config_f, config_p, config_q, config_client
from resources.config import Configuration

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
app.secret_key = secretkey_config
api = Api(app)

#creates tables on startup when first request ist made
@app.before_first_request
def create_tables():
    '''
    Creates all tables (if not already existing) after the first request was made.
    '''
    db.create_all()


#@app.before_first_request
def activate_job():
    '''
    Starts threads with automatic background jobs.
    To activate this comment in the above decorator.
    '''
    def request_survey():
        '''
        Requests surveys from the server in a specified interval.
        '''
        while True:
            print("Request Survey")
            r = requests.get(serviceprovider_surveys)
            time.sleep(repeat_request_surveys)
    thread_survey = threading.Thread(target=request_survey)
    thread_survey.start()

    def send_report():
        '''
            Send reports to the server in a specified interval.
        '''
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
api.add_resource(ListServerInquiries, '/lsi')




api.add_resource(Configuration, '/configuration')


# API's for client/server communication
api.add_resource(RequestSurvey, '/requestsurveys/')
api.add_resource(SendReport, '/sendreports/')

api.add_resource(MatchInquiries, '/matchinquiries/')

api.add_resource(Report, '/reports/<string:surveyid>')
api.add_resource(ListReports, '/listreports/')

##################################################################
# testing:
# allows  access to server inquiries through the REST API
##################################################################
api.add_resource(ServerInquiries, '/si/<string:name>')


### views ########################################################
## routes for the web GUI
##################################################################
import json
import requests
from models.client_inquiries import ClientInquiriesModel
from models.server_inquiries import ServerInquiriesModel
from models.archive import ArchiveModel
from models.reports import ReportModel
from models.config import ConfigurationModel
from forms import InquiryCreateForm, InquiryDetailForm, PrivacyForm, SettingsForm, TestsForm
from wtforms import BooleanField
from internal.basicrappor import permanent_RandomizedResponse, instantaneous_RandomizedResponse
from resources.parsers import check_fpq, check_if_bits


@app.route('/')
@app.route('/index')
def index():
    '''
    Homepage (web GUI).
    '''
    return render_template('home.html', title='Home')


@app.route('/inquiries/')
def inquiries_list():
    '''
    List all client inquiries (web GUI).
    '''
    #access is only allowed if gdpr is set to true
    cnfg = ConfigurationModel.find()
    if cnfg is None:
        abort(404)
    if cnfg.dsgvo != 1:
        print("info works")
        return redirect(url_for('gdpr'))

    inqs = (db.session.query(ClientInquiriesModel).order_by(ClientInquiriesModel.id.desc()).all())
    return render_template('inquiries/inquiries.html', inqs=inqs, title='list of inquiries')


@app.route('/privacy/<int:id>/', methods=['GET','POST'])
def inquiries_privacy(id):
    '''
    This is for privacy settings.
    '''
    #access is only allowed if gdpr is set to true
    cnfg = ConfigurationModel.find()
    if cnfg is None:
        abort(404)
    if cnfg.dsgvo != 1:
        print("info works")
        return redirect(url_for('gdpr'))

    inq = ClientInquiriesModel.find_by_id(id)
    if inq is None:
        abort(404)

    form = PrivacyForm()

    if form.validate_on_submit():
        #answer = form.answer.data
        locked = form.locked.data
        f = form.f.data
        p = convert_range(form.p.data)
        q = convert_range(form.q.data)

        if not check_fpq(f,p,q):
            print("Only values between 0 and 1 allowed for f,p,q!") #debug
            flash("Only values between 0 and 1 allowed for f,p,q!")
            return render_template('inquiries/privacy.html', inq=inq, form=form, title='privacy settings')

        inq.f = f
        inq.p = p
        inq.q = q
        try:
            inq.save_to_db()
        except:
            return render_template('/error_pages/500.html', title='error while trying to save inquiries.')

    return render_template('inquiries/privacy.html', inq=inq, form=form, title='privacy')

def convert_range(value):
    '''
    Convert from the range [-1;1] of chernoff-faces to the rappor-range [0;1]
    https://stackoverflow.com/questions/929103/convert-a-number-range-to-another-range-maintaining-ratio
    '''
    old_range = 1 - (-1)
    new_range = 1 - 0

    return ((value - (-1)) * new_range) / old_range

@app.route('/inquiries/<int:id>/', methods=['GET','POST'])
def inquiries_detail(id):
    '''
    Detailed view of an inquiry (web GUI).
    '''
    #access is only allowed if gdpr is set to true
    cnfg = ConfigurationModel.find()
    if cnfg is None:
        abort(404)
    if cnfg.dsgvo != 1:
        print("info works")
        return redirect(url_for('gdpr'))

    inq = ClientInquiriesModel.find_by_id(id)
    if inq is None:
        abort(404)

    # if the user changes a client inquiry, responded will be set to TRUE
    # and a PRR will be made with the answer value
    form = InquiryDetailForm()

    if inq.type == 'mc':
        form.radio_elem.description = inq.qdescription
        form.radio_elem.choices = [('_'.join(o.lower().split(' ')), o) for o in json.loads(inq.options)]
        form.radio_elem.name = inq.name

    elif inq.type == 'cbx':
        form.checkbox_elem.description = inq.qdescription
        form.checkbox_elem.name = inq.name
        form.checkbox_elem.choices = [('_'.join(o.lower().split(' ')), o) for o in json.loads(inq.options)]
    elif inq.type == 'bool':
        form.boolean_elem.description = inq.qdescription
        form.boolean_elem.name = inq.name
        form.boolean_elem.choices = [('_'.join(o.lower().split(' ')), o) for o in json.loads(inq.options)]
    else:
        abort(400, "Unknown question type {}".format(inq.type))

    if form.validate_on_submit():
        answer = form.answer.data
        locked = form.locked.data
        f = inq.f
        p = inq.p
        q = inq.q

        # check length of answer
        if not (len(json.loads(answer)) == len(json.loads(inq.answer))):
            print("answer must have the same ordinal values!") #debug
            flash("answer must have the same ordinal values!")
            return render_template('inquiries/inquiry.html', inq=inq, form=form, title='question')

        # if bits are zero and one
        if not check_if_bits(json.loads(answer)):
            print("only 0s and 1s allowed in the answer list") #debug
            flash("only 0s and 1s allowed in the answer list")
            return render_template('inquiries/inquiry.html', inq=inq, form=form, title='question')

        # a PRR and IRR will be set after a answer is was changed
        if(inq.answer != answer):
            prr = permanent_RandomizedResponse(float(f),json.loads(answer))
            inq.prr_answer = json.dumps(prr)
            irr = instantaneous_RandomizedResponse(float(p),float(q),prr)
            inq.irr_answer = json.dumps(irr)

        inq.answer = answer
        inq.responded = True # if a answer was given by the user, responed will be set to TRUE
        inq.locked = locked
        inq.f = config_f
        inq.p = config_p
        inq.q = config_q
        try:
            inq.save_to_db()
        except:
            return render_template('/error_pages/500.html', title='error while trying to save inquiries.')

    return render_template('inquiries/inquiry.html', inq=inq, form=form, title='question')


@app.route('/inquiries/create', methods=['GET','POST'])
def inquiries_create():
    '''
    Create new inquiries (web GUI).
    '''
    form = InquiryCreateForm()

    if form.validate_on_submit():

        inquiries = json.loads(form.questions.data)
        # print("client inquiries")
        # print(type(inquiries))
        # print(inquiries)
        for inquiry in inquiries:
            #length_options_list = len(json.loads(inquiry['options']))
            length_options_list = len(inquiry['options'])
            print("inquiry")
            print(inquiry)
            print("liste laenge")
            print(length_options_list)
            options = inquiry['options']
            print("options")
            print(options)

            inq = ClientInquiriesModel(name = inquiry['name'],
                                        type = inquiry['type'],
                                        options = json.dumps(inquiry['options']),
                                        answer = json.dumps([0]* length_options_list),
                                        prr_answer = json.dumps([0]* length_options_list),
                                        irr_answer = json.dumps([0]* length_options_list),
                                        qdescription = inquiry['description'],
                                        responded = False,
                                        locked = True,
                                        f = config_f,
                                        p = config_p,
                                        q = config_q)
            print("inq test")
            print(inq)
            print(type(inq))
            try:
                inq.save_to_db()
            except:
                return render_template('/error_pages/500.html', title='error while creating inquiry.')

        return redirect('inquiries/')
    return render_template('inquiries/create.html', form=form, title='create new inquiries')


@app.route("/inquiries/<int:id>/delete", methods=['POST'])
def inquiries_delete(id):
    '''
    Deleting a (client) inquiry (web GUI).
    '''
    inq = ClientInquiriesModel.query.get_or_404(id)
    try:
        inq.delete_from_db()
    except:
        return render_template('/error_pages/500.html', title='error while trying to delete inquiry.')

    flash('inquiry has been deleted.')
    return redirect(url_for('inquiries_list'))


@app.route('/internal_data')
def internal_data():
    '''
    This is for testing (web GUI).
    It shows all client-, and server inquiries and reports which are stored in the client database.
    '''
    answers = ClientInquiriesModel.query.all()
    questions = ServerInquiriesModel.query.all()
    reports = ReportModel.query.all()
    stats = ArchiveModel.query.all()
    cnfg = ConfigurationModel.query.first()
    return render_template('internal_data.html', answers=answers, questions=questions, reports=reports, stats=stats, cnfg=cnfg, title='internal data: inquiries, reports & archive')


@app.route('/settings', methods=['GET','POST'])
def settings():
    '''
    Configuration page (web GUI).
    '''
    cnfg = ConfigurationModel.find()
    if cnfg is None:
        abort(404)
    form = SettingsForm()

    #sets the values in the form
    if request.method != 'POST':
        form.dsgvo.default = cnfg.dsgvo
        form.quiz.default = cnfg.quizmode
        form.f.default = cnfg.global_f
        form.p.default = cnfg.global_p
        form.q.default = cnfg.global_q
        form.process()

    if form.validate_on_submit():
            dsgvo = form.dsgvo.data
            quiz = form.quiz.data
            f = form.f.data
            p = form.p.data
            q = form.q.data
            if not check_fpq(f,p,q):
                print("Only values between 0 and 1 allowed for f,p,q!") #debug
                flash("Only values between 0 and 1 allowed for f,p,q!")
                return render_template('settings.html', form=form, title='client settings')

            cnfg.dsgvo = dsgvo
            cnfg.quizmode = quiz
            cnfg.global_f = f
            cnfg.global_p = p
            cnfg.global_q = q
            try:
                cnfg.save_to_db()
            except:
                return render_template('/error_pages/500.html', title='error while trying to save inquiries.')


    return render_template('settings.html', form=form, cnfg=cnfg, title='client settings')


@app.route('/tests', methods=['GET','POST'])
def tests():
    '''
    Options for client testing (web GUI).
    '''
    form = TestsForm()
    flash("horst")
    if form.validate_on_submit():
        if 'submit_request' in request.form:
            print("Request Survey button pressed") #debug
            r = requests.get(config_client + '/requestsurveys/')

        elif 'submit_report' in request.form:
            print("Send report button pressed") #debug
            r = requests.get(config_client + '/sendreports/')

        elif 'submit_match' in request.form:
            print("Match inquiries button pressed") #debug
            r = requests.get(config_client + '/matchinquiries/')

        elif 'clean_archive' in request.form:
            print("Match inquiries button pressed") #debug
            try:
                ArchiveModel.delete_archive()
            except:
                return render_template('/error_pages/500.html', title='error while trying to delete inquiry.')

    return render_template('tests.html', form=form, title='client tests')

@app.route('/info')
def info():
    '''
    Infomation page (web GUI).
    '''
    return render_template('info.html')

@app.route('/gdpr')
def gdpr():
    '''
    DSGVO/GDPR info (web GUI).
    '''
    return render_template('gdpr.html')


'''
Ensures that settings will be created at first startup.
'''
@app.before_first_request
def create_configuration():
    cnfg = ConfigurationModel.find()
    if cnfg is None:
        client = ConfigurationModel()
        client.save_to_db()


##################################################################
## Client only starts when it will be executed over the file app.py
##################################################################
if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5001,debug=True)

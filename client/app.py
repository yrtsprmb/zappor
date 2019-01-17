#app.py
from flask import Flask, render_template, url_for, redirect, flash, request, abort
from flask_restful import Api
from db import db
from flask_sqlalchemy import SQLAlchemy

#import of the resources
from resources.client_inquiries import ClientInquiries, ListClientInquiries
from resources.server_inquiries import ServerInquiries, ListServerInquiries

from resources.clientconf import ClientConf

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
from internal.config import configfile_f, configfile_p, configfile_q

# for requests
from resources.request_surveys import RequestSurvey
from resources.send_reports import SendReport
from resources.match_inquiries import MatchInquiries
from resources.reports import Report, ListReports

from forms import RequestSurveyTestForm


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
    Creates all needed tables (if not already existing) after the first request was made.
    '''
    db.create_all()


#@app.before_first_request
def activate_job():
    '''
    Starts threads with automatic background jobs.
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


api.add_resource(ListReports, '/listreports/')

api.add_resource(ClientConf, '/configuration/<string:clientname>')


# API's for client/server communication
api.add_resource(RequestSurvey, '/requestsurveys/')
api.add_resource(SendReport, '/sendreports/')
api.add_resource(MatchInquiries, '/match/')
api.add_resource(Report, '/reports/<string:surveyid>')

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
from forms import CreateClientInquiryForm, EditClientInquiryForm, RequestSurveyTestForm, TestClientInquiryForm
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
    inqs = (db.session.query(ClientInquiriesModel).order_by(ClientInquiriesModel.id.desc()).all())
    return render_template('inquiries/inquiries.html', inqs=inqs, title='list of inquiries')


@app.route('/privacy/<int:id>/', methods=['GET','POST'])
def inquiries_privacy(id):
    '''
    This is for privacy settings.
    '''
    from forms import PrivacyForm

    #inq = db.session.query(ClientInquiriesModel).get(id)
    inq = ClientInquiriesModel.find_by_id(id)
    if inq is None:
        abort(404)

    form = PrivacyForm()
    if form.validate_on_submit():
        #answer = form.answer.data
        locked = form.locked.data
        f = form.f.data
        p = form.p.data
        q = form.q.data

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


@app.route('/inquiries/<int:id>/', methods=['GET','POST'])
def inquiries_detail(id):
    '''
    Detailed view of an inquiry (web GUI).
    '''
    inq = ClientInquiriesModel.find_by_id(id)
    #inq = db.session.query(ClientInquiriesModel).get(id)
    if inq is None:
        abort(404)

    # if the user changes a client inquiry, responded will be set to TRUE
    # and a PRR will be made with the answer value
    # form = EditClientInquiryForm()
    form = TestClientInquiryForm()

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
        # f = form.f.data
        # p = form.p.data
        # q = form.q.data

        #print("answer")
        #print((answer))
        # print(len(json.loads(answer)))
        # print(len(json.loads(inq.answer)))

        #validation checks:
        #print(len(json.loads(answer)))
        # if fpq is between 0 and 1
        # if not check_fpq(f,p,q):
        #     print("Only values between 0 and 1 allowed for f,p,q!") #debug
        #     flash("Only values between 0 and 1 allowed for f,p,q!")
        #     return render_template('inquiries/inquiry.html', inq=inq, form=form, title='question')
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
        inq.f = configfile_f
        inq.p = configfile_p
        inq.q = configfile_q
        try:
            inq.save_to_db()
        except:
            return render_template('/error_pages/500.html', title='error while trying to save inquiries.')

    return render_template('inquiries/inquiry.html', inq=inq, form=form, title='question')


@app.route('/inquiries/create', methods=['GET','POST'])
def inquiries_create():
    '''
    Creation of a (client) inquiry (web GUI).
    '''
    form = CreateClientInquiryForm()
    if ClientInquiriesModel.find_by_name(form.inq_name.data):
        print("name already in db") #debug
        flash("name already in db")
        return render_template('inquiries/create.html', form=form, title='create a new inquiry')

    if form.validate_on_submit():
        length_options_list = len(json.loads(form.inq_options.data))
        inq = ClientInquiriesModel(name = form.inq_name.data,
                                    type = form.inq_type.data,
                                    options = form.inq_options.data,
                                    answer = json.dumps([0]* length_options_list),
                                    prr_answer = json.dumps([0]* length_options_list),
                                    irr_answer = json.dumps([0]* length_options_list),
                                    qdescription = form.inq_qdescription.data,
                                    responded = False,
                                    locked = True,
                                    f = configfile_f,
                                    p = configfile_p,
                                    q = configfile_q)
        try:
            inq.save_to_db()
        except:
            return render_template('/error_pages/500.html', title='error while creating inquiry.')

        flash("Inquiry created")
        return redirect('inquiries/')
    return render_template('inquiries/create.html', form=form, title='create a new inquiry')


###### BEGINN TEST
@app.route('/create', methods=['GET','POST'])
def inq_create():
    '''
    Creates a survey (web GUI).
    '''
    from forms import CreateInquiryForm
    import json
    form = CreateInquiryForm()

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
                                        f = configfile_f,
                                        p = configfile_p,
                                        q = configfile_q)
            print("inq test")
            print(inq)
            print(type(inq))
            #try:
            inq.save_to_db()
            #except:
            #    return render_template('/error_pages/500.html', title='error while creating inquiry.')

        return redirect(url_for('inquiries_list'))
    return render_template('create.html', form=form, title='create a new inquiry')

###### ENDE TEST

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
    return render_template('internal_data.html', answers=answers, questions=questions, reports=reports, stats=stats, title='internal data: inquiries, reports & archive')


@app.route('/config')
def client_config():
    '''
    Configuration page (web GUI).
    '''
    return render_template('client_config.html', title='Configuration')


@app.route('/tests', methods=['GET','POST'])
def tests():
    '''
    Options for client testing (web GUI).
    '''
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

##################################################################
## Client only starts when it will be executed over the file app.py
##################################################################
if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5001,debug=True)

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



### TEST #########################################################
## imports for testing
##################################################################

# import of configurations:
from internal.config import secretkey_config, repeat_send_reports, repeat_request_surveys, serviceprovider_reports, serviceprovider_surveys
from internal.config import global_f, global_p,global_q

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
    from forms import EditClientInquiryForm
    import json
    from internal.basicrappor import permanent_RandomizedResponse, instantaneous_RandomizedResponse
    from resources.parsers import check_fpq, check_if_bits

    inq = db.session.query(ClientInquiriesModel).get(id)
    if inq is None:
        abort(404)

    # if the user changes a client inquiry, responded will be set to TRUE
    # and a PRR will be made with the answer value
    form = EditClientInquiryForm()
    if form.validate_on_submit():
        answer = form.answer.data
        locked = form.locked.data
        f = form.f.data
        p = form.p.data
        q = form.q.data

        # print("answer")
        # #print(json.loads(answer))
        # print(len(json.loads(answer)))
        # print(len(json.loads(inq.answer)))

        #validation checks:
        print(len(json.loads(answer)))
        # if fpq is between 0 and 1
        if not check_fpq(f,p,q):
            print("Only values between 0 and 1 allowed for f,p,q!") #debug
            flash("Only values between 0 and 1 allowed for f,p,q!")
            return render_template('inquiries/client_inquiry.html', inq=inq, form=form, title='question')


        # check length of answer
        if not (len(json.loads(answer)) == len(json.loads(inq.answer))):
            print("answer must have the same ordinal values!") #debug
            flash("answer must have the same ordinal values!")
            return render_template('inquiries/client_inquiry.html', inq=inq, form=form, title='question')

        # if bits are zero and one
        if not check_if_bits(json.loads(answer)):
            print("only 0s and 1s allowed in the answer list") #debug
            flash("only 0s and 1s allowed in the answer list")
            return render_template('inquiries/client_inquiry.html', inq=inq, form=form, title='question')

        # a PRR and IRR will be set after a answer is was changed
        if(inq.answer != answer):
            prr = permanent_RandomizedResponse(float(f),json.loads(answer))
            inq.prr_answer = json.dumps(prr)
            irr = instantaneous_RandomizedResponse(float(p),float(q),prr)
            inq.irr_answer = json.dumps(irr)

        inq.answer = answer
        # if a answer was given by the user, responed will be set to TRUE
        inq.responded = True
        inq.locked = locked
        inq.f = f
        inq.p = p
        inq.q = q
        db.session.commit()

    return render_template('inquiries/client_inquiry.html', inq=inq, form=form, title='question')


@app.route('/inquiries/create', methods=['GET','POST'])
def inquiries_create():
    from models.client_inquiries import ClientInquiriesModel
    from forms import CreateClientInquiryForm
    import json

    form = CreateClientInquiryForm()
    if ClientInquiriesModel.find_by_name(form.inq_name.data):
        print("name already in db")
        flash("name already in db")
        return render_template('inquiries/create.html', form=form, title='create a new inquiry')


    if form.validate_on_submit():

        length_options_list = len(json.loads(form.inq_options.data))
        print('mega')
        print(length_options_list)
        inq = ClientInquiriesModel(name = form.inq_name.data,
                                    type = form.inq_type.data,
                                    options = form.inq_options.data,
                                    answer = json.dumps([0]* length_options_list),
                                    prr_answer = json.dumps([0]* length_options_list),
                                    irr_answer = json.dumps([0]* length_options_list),
                                    responded = True,
                                    locked = True,
                                    f = global_f,
                                    p = global_p,
                                    q = global_q)
        inq.save_to_db()

        flash("Survey created")
        return redirect('inquiries/')
    return render_template('inquiries/create.html', form=form, title='create a new inquiry')


@app.route("/inquiries/<int:id>/delete", methods=['POST'])
def inquiries_delete(id):
    from models.client_inquiries import ClientInquiriesModel

    inq = ClientInquiriesModel.query.get_or_404(id)
    inq.delete_from_db()
    flash('inquiry has been deleted.')
    return redirect(url_for('inquiries_list'))


#testing
@app.route('/show')
def show_inquiries():
    from models.server_inquiries import ServerInquiriesModel
    from models.client_inquiries import ClientInquiriesModel
    from models.reports import ReportModel

    answers = ClientInquiriesModel.query.all()
    questions = ServerInquiriesModel.query.all()
    reports = ReportModel.query.all()
    return render_template('show_inquiries.html', answers=answers, questions=questions, reports=reports, title='list of inquiries')


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


####### Server only starts when it will be executed over the file app.py
if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5001,debug=True)

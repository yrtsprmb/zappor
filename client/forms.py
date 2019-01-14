#forms.py
from flask_wtf import FlaskForm
from wtforms import TextAreaField, BooleanField, DecimalField, FloatField, StringField, IntegerField, SubmitField, SelectField, TextField, validators
from wtforms.validators import DataRequired, Length


#tests
class PrivacyForm(FlaskForm):
    '''
    Form for editing privacy setings (web GUI).
    '''
    # name = TextField('name')
    # options = TextField('name')
    # answer = TextField('your answer', validators=[DataRequired()])
    locked = BooleanField("lock question?")
    # qdescription = TextField('Descpription')
    #locked = TextField("p", [validators.Length(min=0,max=5)])
    #f = TextField('f', validators=[DataRequired(message="value must be between 0 and 1")])
    #p = TextField("p", [validators.Length(min=0,max=5)])
    f = DecimalField('f')
    p = DecimalField('p')
    q = DecimalField('q')
    submit = SubmitField('Save')


class CreateInquiryForm(FlaskForm):
    '''
    Form for creating a client inquiry (web GUI).
    '''
    # surveyname = StringField('Surveyname:', validators=[DataRequired()])
    # status = SelectField('Status:', choices=[('created','created'),('active','active')], validators=[DataRequired()])
    # sdescription = StringField('Description of the survey:')
    questions = TextAreaField('Questions:')
    submit = SubmitField('Create Inquiry')


# ende test

class CreateClientInquiryForm(FlaskForm):
    '''
    Form for creating a client inquiry (web GUI).
    '''
    inq_name = StringField('Name:', validators=[DataRequired()])
    inq_type = SelectField('Type:', choices=[('bool','boolean'),('mc','multiple choice (1 option)'),('cbx','checkbox (n options)')], validators=[DataRequired()])
    inq_options = TextAreaField('Options:', validators=[DataRequired()])
    inq_qdescription = StringField('Description of the inquiry:')
    submit = SubmitField('Create inquiry')



#purpose of forms: render a input form in html and validate submitted data
class EditClientInquiryForm(FlaskForm):
    '''
    Form for editing a client inquiry (web GUI).
    Detail view of an inquiry.
    '''
    name = TextField('name')
    options = TextField('name')
    answer = TextField('your answer', validators=[DataRequired()])
    locked = BooleanField("lock question?")
    qdescription = TextField('Descpription')
    #locked = TextField("p", [validators.Length(min=0,max=5)])
    #f = TextField('f', validators=[DataRequired(message="value must be between 0 and 1")])
    #p = TextField("p", [validators.Length(min=0,max=5)])
    f = DecimalField('f')
    p = DecimalField('p')
    q = DecimalField('q')
    submit = SubmitField('Save')






class RequestSurveyTestForm(FlaskForm):
    '''
    Form for the tests page (web GUI).
    '''
    submit_request_survey = SubmitField('Request Survey')
    submit_send_reports = SubmitField('Send Reports')
    submit_match_inquiries = SubmitField('Match Inquiries')


# class ClientInquiryForm(FlaskForm):
#     name = TextField('name')
#     options = TextField('name')
#     answer = TextField('your answer', validators=[DataRequired()])
#     locked = BooleanField("lock question?")
#     #locked = TextField("p", [validators.Length(min=0,max=5)])
#     #f = TextField('f', validators=[DataRequired(message="value must be between 0 and 1")])
#     #p = TextField("p", [validators.Length(min=0,max=5)])
#     f = DecimalField('f')
#     p = DecimalField('p')
#     q = DecimalField('q')
#     submit = SubmitField('Edit inquiry')

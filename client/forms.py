from flask_wtf import FlaskForm
from wtforms import BooleanField, DecimalField, FloatField, StringField, IntegerField, SubmitField, SelectField, TextField, validators
from wtforms.validators import DataRequired, Length


#purpose of forms: render a input form in html and validate submitted data

class RequestSurveyTestForm(FlaskForm):
    submit_request_survey = SubmitField('Request Survey')
    submit_send_reports = SubmitField('Send Reports')
    submit_match_inquiries = SubmitField('Match Inquiries')


class RapporForm(FlaskForm):
    f = IntegerField('Insert f value:', validators=[DataRequired()])
    p = IntegerField('Insert p value:')
    q = IntegerField('Insert q wert:')
    submit = SubmitField('Add Rappor')


#class InquiryForm(Form):
class ClientInquiryForm(FlaskForm):
    name = TextField('name')
    options = TextField('name')
    answer = TextField('your answer', validators=[DataRequired()])
    locked = BooleanField("lock question?")
    #locked = TextField("p", [validators.Length(min=0,max=5)])
    #f = TextField('f', validators=[DataRequired(message="value must be between 0 and 1")])
    #p = TextField("p", [validators.Length(min=0,max=5)])
    f = DecimalField('f')
    p = DecimalField('p')
    q = DecimalField('q')
    submit = SubmitField('Edit inquiry')

from flask_wtf import FlaskForm
from wtforms import BooleanField, FloatField, StringField, IntegerField, SubmitField, SelectField, TextField
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
class InquiryForm(FlaskForm):
    name = TextField('name')
    options = TextField('name')
    answer = TextField("horst")
    locked = BooleanField("")
    f = TextField("f")
    p = TextField("p")
    q = TextField("q")
    submit = SubmitField('Edit inquiry')

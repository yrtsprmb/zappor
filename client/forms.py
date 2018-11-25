from flask_wtf import FlaskForm
from wtforms import BooleanField, FloatField, StringField, IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length



class RequestSurveyTestForm(FlaskForm):
    submit_request_survey = SubmitField('Request Survey')
    submit_send_reports = SubmitField('Send Reports')
    submit_match_inquiries = SubmitField('Match Inquiries')


class RapporForm(FlaskForm):
    f = IntegerField('Insert f value:', validators=[DataRequired()])
    p = IntegerField('Insert p value:')
    q = IntegerField('Insert q wert:')
    submit = SubmitField('Add Rappor')
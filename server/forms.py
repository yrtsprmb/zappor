from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, SubmitField, SelectField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length
from models.survey import SurveyModel


class NewSurveyForm(FlaskForm):
    surveyid = StringField('Surveyid', validators=[DataRequired()]) #TODO: autogenerate this value
    serviceprovider = StringField('Serviceprovider', validators=[DataRequired()])
    surveyname = StringField('Surveyname', validators=[DataRequired()])
    status = SelectField('Status', choices=[('created','created'),
                                            ('active','active'),
                                             ('done','done')], validators=[DataRequired()])
    comment = StringField('Description of the survey:', validators=[Length(max=300, message='max length %(max) characters')])
    questions = TextAreaField('Questions', validators=[DataRequired()])
    submit = SubmitField('Submit Survey')

    def validate_surveyid(self,surveyid):
        surveyid = SurveyModel.query.filter_by(surveyid=surveyid.data).first()
        if surveyid is not None:
            raise ValidationError('Please use a different surveyid')



class QuestionForm(FlaskForm):
    qid = IntegerField('qid', validators=[DataRequired()]) #TODO: autogenerate this value
    name = StringField('Name', validators=[DataRequired()])
    typ = StringField('typ', validators=[DataRequired()])
    options = StringField('Options', validators=[DataRequired()])
    submit = SubmitField('Submit Question')


######### Testing
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
#,Length(max=2000, message='max length %(max) characters'

from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, SubmitField, SelectField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length
from models.survey import SurveyModel


class SurveyForm(FlaskForm):
    submit = SubmitField('Submit Survey')



class CreateSurveyForm(FlaskForm):
    surveyname = StringField('Surveyname:', validators=[DataRequired()])
    status = SelectField('Status:', choices=[('created','created'),('active','active')], validators=[DataRequired()])
    comment = StringField('Description:')
    questions = TextAreaField('Questions:', validators=[DataRequired()])
    submit = SubmitField('Create Survey')

    def validate_surveyname(self,surveyname):
        srvy = SurveyModel.query.filter_by(surveyname=surveyname.data).first()
        if srvy is not None:
            raise ValidationError('Please use a different surveyname')


class EditSurveyForm(FlaskForm):
    surveyname = StringField('Surveyname:', validators=[DataRequired()])
    status = SelectField('Status:', choices=[('created','created'),('active','active')], validators=[DataRequired()])
    comment = StringField('Description:')
    questions = TextAreaField('Questions:', validators=[DataRequired()])
    submit = SubmitField('Create Survey')

    def validate_surveyname(self,surveyname):
        srvy = SurveyModel.query.filter_by(surveyname=surveyname.data).first()
        if srvy is not None:
            raise ValidationError('Please use a different surveyname')


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

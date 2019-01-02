#forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, SubmitField, SelectField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length
from models.surveys import SurveyModel


class TestForm(FlaskForm):
    '''
    TODO: This is for testing page in the web GUI.
    '''
    submit_evaluation = SubmitField('Generate Summary')
    submit_summary = SubmitField('Generate Summary')


class SummaryForm(FlaskForm):
    '''
    TODO: Back button for the histogram page in the web GUI.
    '''
    submit = SubmitField('Back to survey overview.')


class SurveyForm(FlaskForm):
    '''
    Form for changing the status of a survey. Is used for display the details of a survey.
    '''
    status = SelectField('Status:', choices=[('created','created'),('active','active'),('done','done')], validators=[DataRequired()])
    mychoices = [('created','created'),('active','active'),('done','done')]
    submit = SubmitField('Change Status:')


class CreateSurveyForm(FlaskForm):
    '''
    Form for creating a new survey.
    '''
    surveyname = StringField('Surveyname:', validators=[DataRequired()])
    status = SelectField('Status:', choices=[('created','created'),('active','active')], validators=[DataRequired()])
    sdescription = StringField('Description of the survey:')
    questions = TextAreaField('Questions:', validators=[DataRequired()])
    submit = SubmitField('Create Survey')

    def validate_surveyname(self,surveyname):
        '''
        Checks if surveyname is already in use.
        '''
        srvy = SurveyModel.query.filter_by(surveyname=surveyname.data).first()
        if srvy is not None:
            raise ValidationError('Please use a different surveyname')


class EditSurveyForm(FlaskForm):
    '''
    TODO
    '''
    surveyname = StringField('Surveyname:', validators=[DataRequired()])
    status = SelectField('Status:', choices=[('created','created'),('active','active')], validators=[DataRequired()])
    comment = StringField('Description:')
    questions = TextAreaField('Questions:', validators=[DataRequired()])
    submit = SubmitField('Create Survey')

    def validate_surveyname(self,surveyname):
        '''
        Checks if surveyname is already in use.
        '''
        srvy = SurveyModel.query.filter_by(surveyname=surveyname.data).first()
        if srvy is not None:
            raise ValidationError('Please use a different surveyname')


class QuestionForm(FlaskForm):
    '''
    TODO: not implemented yet.
    '''
    qid = IntegerField('qid', validators=[DataRequired()]) #TODO: autogenerate this value
    name = StringField('Name', validators=[DataRequired()])
    typ = StringField('typ', validators=[DataRequired()])
    options = StringField('Options', validators=[DataRequired()])
    submit = SubmitField('Submit Question')


class LoginForm(FlaskForm):
    '''
    TODO: if a login should be implemented, this form will be used.
    '''
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

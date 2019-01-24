#forms.py
#purpose of forms: render a input form in html and validate submitted data
from flask_wtf import FlaskForm
from wtforms import FieldList, SelectMultipleField, TextAreaField, BooleanField, DecimalField, FloatField, StringField, IntegerField, SubmitField, SelectField, TextField, RadioField, HiddenField, validators
from wtforms.validators import DataRequired, Length
from wtforms.widgets import ListWidget, CheckboxInput

#TODO: privacy
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


class MultiCheckboxField(SelectMultipleField):
    """
    A multiple-select, except displays a list of checkboxes.

    Iterating the field will produce subfields, allowing custom rendering of
    the enclosed checkbox fields.
    """
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()


class InquiryCreateForm(FlaskForm):
    '''
    Form for creating a client inquiry (web GUI).
    '''
    questions = TextAreaField('Questions:')
    submit = SubmitField('Create Inquiries')


class InquiryDetailForm(FlaskForm):
    '''
    Form for creating a client inquiry (web GUI).
    '''
    radio_elem = RadioField(choices=[()], validators=[validators.optional()])
    checkbox_elem = MultiCheckboxField(choices=[()], validators=[validators.optional()])
    boolean_elem = RadioField(choices=[()], validators=[validators.optional()])
    answer = HiddenField('answer')
    locked = BooleanField("lock question?")
    f = DecimalField('f')
    p = DecimalField('p')
    q = DecimalField('q')
    submit = SubmitField('Save')


class SettingsForm(FlaskForm):
    '''
    Form for client settings (web GUI).
    '''
    # name = TextField('name')
    # options = TextField('name')
    # answer = TextField('your answer', validators=[DataRequired()])
    # qdescription = TextField('Descpription')
    #locked = TextField("p", [validators.Length(min=0,max=5)])
    #f = TextField('f', validators=[DataRequired(message="value must be between 0 and 1")])
    #p = TextField("p", [validators.Length(min=0,max=5)])
    dsgvo = BooleanField("dsgvo")
    quiz = BooleanField("quizmode")
    f = DecimalField('f')
    p = DecimalField('p')
    q = DecimalField('q')
    submit = SubmitField('Save')


class TestsForm(FlaskForm):
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

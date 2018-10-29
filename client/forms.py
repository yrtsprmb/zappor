from flask_wtf import FlaskForm
from wtforms import BooleanField, FloatField, StringField, IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length


class QuestionForm(FlaskForm):
    name = StringField('Name of Puppy:')
    submit = SubmitField('Add Puppy')

    #privacy settings
    locked = BooleanField('lock question', validators=[DataRequired()])
    #RAPPOR values
    f = FloatField('Insert f value:', validators=[DataRequired(), Length(min=0, max=1.0, message='value must between 0 and 1')])
    p = FloatField('Insert p value:', validators=[DataRequired(), Length(min=0, max=1.0, message='value must between 0 and 1')])
    q = FloatField('Insert q value:', validators=[DataRequired(), Length(min=0, max=1.0, message='value must between 0 and 1')])
    submit = SubmitField('Add Rappor')

### old stuff ##########################################
## altes zeugs
########################################################

class AddForm(FlaskForm):
    name = StringField('Name of Puppy:')
    submit = SubmitField('Add Puppy')

class AddOwnerForm(FlaskForm):
    name = StringField('Name of Owner:')
    pup_id = IntegerField("Id of Puppy: ")
    submit = SubmitField('Add Owner')

class DelForm(FlaskForm):
    id = IntegerField('Id Number of Puppy to Remove:')
    submit = SubmitField('Remove Puppy')

##### Helgazone

class RapporForm(FlaskForm):
    p = IntegerField('Insert p value:', validators=[DataRequired()])
    q = IntegerField('Insert q value:')
    r = IntegerField('Insert r wert:')
    submit = SubmitField('Add Rappor')

class PersonalForm(FlaskForm):
    name = StringField('Insert your name:', validators=[DataRequired()])
    surname = StringField('Insert your surname:')
    education = SelectField(u'Choose your education grade:',
                            choices=[('no','without degree'),
                                     ('ps','primary school'),
                                     ('mm','medium maturity'),
                                     ('vt','vocational training'),
                                     ('abi','abitur/high school'),
                                     ('ba','Bachelor'),
                                     ('ma','Master'),
                                     ('doc','postdoc')])
    submit = SubmitField('Add/Update Personal Data')

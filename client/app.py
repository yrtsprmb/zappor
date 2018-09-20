from flask import Flask, render_template, request
from forms import InfoForm, RapporForm

#Formularzeugs
from flask_wtf import FlaskForm
from wtforms import (StringField,IntegerField,BooleanField,
                     DateTimeField,RadioField,SelectField,
                     TextField,TextAreaField,SubmitField)
from wtforms.validators import DataRequired


from flask import session,redirect,url_for
from flask import flash # for flashing messages


app = Flask(__name__)
#todo: als umgebungsvariable verwenden
app.config['SECRET_KEY'] = 'geheimnis'



@app.route('/test', methods=['GET','POST'])
def test():
    form = InfoForm()
    if form.validate_on_submit():
        session['breed'] = form.breed.data
        session['neutered'] = form.neutered.data
        session['mood'] = form.mood.data
        session['food'] = form.food_choice.data
        session['feedback'] = form.feedback.data
        return redirect(url_for('thankyouinfoform'))

    return render_template('test.html', form=form)

@app.route('/thankyouinfoform')
def thankyouinfoform():
    return render_template('thankyoutest.html')

### ende testarea

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/personal')
def personal_page():
    return render_template('personal.html')

@app.route('/privacy',methods=['GET','POST'])
def privacy_page():
    p = False
    q = False
    r = False
    form = RapporForm()
    if form.validate_on_submit():
        flash('You just clicked the button')
        p = form.p.data
        q = form.q.data
        r = form.r.data
        form.p.data = ''
        return redirect(url_for('privacy_page'))
    return render_template('privacy.html',form=form,p=p,q=q,r=r)

@app.route('/radio')
def radio_page():
    return render_template('radio.html')

@app.route('/about')
def about_page():
    return render_template('about.html')

@app.route('/signup_form')
def signup_form():
    return render_template('signup.html')

@app.route('/thankyou')
def thankyou():
    radioname = request.args.get('radioname')
    programmname = request.args.get('programmname')
    return render_template('thankyou.html', radioname=radioname, programmname=programmname)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(port=5001,debug=True)

from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/personal')
def personal_page():
    return render_template('personal.html')

@app.route('/privacy')
def privacy_page():
    return render_template('privacy.html')

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
    first = request.args.get('first')
    last = request.args.get('last')
    return render_template('thankyou.html', first=first, last=last)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(port=5001,debug=True)

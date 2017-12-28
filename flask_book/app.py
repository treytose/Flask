from flask import Flask, request, session, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap

from flask_moment import Moment
from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import Required, Email

from flask_sqlalchemy import SQLAlchemy

from flask_mail import Mail, Message
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

#SQLAlchemy config options
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////root/Flask/flask_book/data.db'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True #set automatic commits of db changes
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

#Flask-Mail config options
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASSWORD')

mail = Mail(app)


bootstrap = Bootstrap(app)
moment = Moment(app)

@app.errorhandler(404)
def page_not_found(e):
    print(e.code)
    return render_template('404.html'), 404

@app.route('/momentExample')
def momentExample():
    return render_template('momentExample.html', current_time=datetime.utcnow())

@app.route('/flask_wtf_example', methods=['POST', 'GET'])
def flask_wtf_example():
    form = NameForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        return redirect(url_for('flask_wtf_example'))

    return render_template('flask_wtf_example.html', name=session.get('name'), form=form)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


# ------------------ Flask-WTF -----------------------
class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')

#------------------- Flask SQLAlchemy -----------------
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %s>' % self.name

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)

    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %s>' % self.username

@app.route('/sqlAlchemy_example', methods=['GET', 'POST'])
def sqlAlchemy_example():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if not user:
            user = User(username=form.name.data)
            db.session.add(user)
            session['known'] = False
        else:
            session['known'] = True

        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('sqlAlchemy_example'))

    return render_template('sqlAlchemy_example.html', form=form,
                            name=session.get('name'), known = session.get('known', False))



# --------------------------- Flask-Mail -------------------------------
class MailForm(FlaskForm):
        recipients = StringField('Recipient', validators=[Required(), Email()])
        subject = StringField('Subject', validators=[Required()])
        body = TextAreaField('Message', validators=[Required()])
        submit = SubmitField('Send')



@app.route('/flask_mail_example', methods=['GET', 'POST'])
def flask_mail_example():
    form = MailForm()
    if form.validate_on_submit():
        msg = Message(form.subject.data, sender='treytose@gmail.com',
                      recipients=[form.recipients.data])
        msg.body = form.body.data
        try:
            with app.app_context():
                mail.send(msg)
            flash('Successfully sent!', 'success')
        except Exception as e:
            flash('Error sending message!', 'danger')
        return redirect(url_for('flask_mail_example'))

    return render_template('flask_mail_example.html', form=form)

if __name__ == '__main__':
    app.run(port=80, host='0.0.0.0', debug=True)

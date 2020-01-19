from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from flask_bootstrap import Bootstrap

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////root/Flask/flask_book/SQLAlchemy/data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret'
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)

class QueryForm(FlaskForm):
    query = StringField('Database Query')
    submit = SubmitField('Submit')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = QueryForm()

    if form.validate_on_submit():
        query = form.query.data
        answer = Student.query.filter_by(query).all()
        return redirect(url_for('.index'), answer=answer)

    return render_template('index.html', form=form)

@app.route('/create_tables')
def create_tables():
    db.create_all()
    return 'Created'

@app.route('/drop_tables')
def drop_tables():
    db.drop_all()
    return 'Dropped'

registrations = db.Table('registrations',
                db.Column('student_id', db.Integer, db.ForeignKey('students.id')),
                db.Column('class_id', db.Integer, db.ForeignKey('classes.id')))


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    classes = db.relationship('Class', secondary=registrations, backref=db.backref('students', lazy='dynamic'), lazy='dynamic')

class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)



if __name__ == '__main__':
    app.run(port=80, host='0.0.0.0', debug=True)

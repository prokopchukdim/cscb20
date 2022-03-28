from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

class RegisteredUsers(db.Model):
    __tablename__ = 'RegisteredUsers'
    utorid = db.Column(db.String(20), nullable=False, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(20), nullable = False)
    """ usertype = db.Column(db.String(20)) """
    student = db.relationship('Student', backref='author', lazy=True)
    instructor = db.relationship('Instructor', backref='author', lazy=True)

    def __repr__(self):
        return f"RegisteredUsers('{self.utorid}', '{self.password}')"

class Student(db.Model):
    __tablename__ = 'Student'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique=True, nullable = False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable = False)
    s_id = db.Column(db.Integer, db.ForeignKey('RegisteredUsers.utorid'), nullable=False)
    
    def __repr__(self):
        return f"Student('{self.username}', '{self.email}')"

class Instructor(db.Model):
    __tablename__ = 'Instructor'
    id = db.Column(db.Integer, primary_key = True)
    username= db.Column(db.String(20), nullable = False)
    """ person_id = db.Column(db.Integer, db.ForeignKey('Person.id'), nullable = False) """
    i_id = db.Column(db.Integer, db.ForeignKey('RegisteredUsers.utorid'), nullable=False)
    
    def __repr__(self):
        return f"Instructor('{self.username}')"


@app.route('/')
@app.route('/home')
def home():
    pagename = 'home'
    return render_template('template.html', pagename=pagename)

@app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        note_details =(
            request.form['Utorid'],
            request.form['Email'],
            bcrypt.generate_password_hash(request.form['Password']),
        )
        utorid = request.form['Utorid']
        user = RegisteredUsers.query.filter_by(utorid=utorid).first()
        if user:
            flash('This account already exists', 'error')
            return render_template('register.html')
        add_notes(note_details)
        return render_template('signup_success.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        utorid = request.form['utorid']
        pswd = bcrypt.generate_password_hash(request.form['pswd'])
        user = RegisteredUsers.query.filter_by(utorid=utorid).first()
        userall = RegisteredUsers.query.all()
        print(userall)
        if user is None:
            flash('Please check your login details and try again.', 'error')
            return render_template('login.html')
        else:
            if not bcrypt.check_password_hash(bcrypt.generate_password_hash(user.password).decode('utf-8'), pswd.decode('utf-8')):
                flash('Please check your login details and try again.', 'error')
                return render_template('login.html')
            else:
                return redirect(url_for('login_success', name=utorid))
    else:
        return render_template('login.html')

@app.route('/login_success/<name>')
def login_success(name):
    return render_template('login_success.html', name=name)

def add_notes(note_details):
    note = RegisteredUsers(utorid = note_details[0], email = note_details[1], password = note_details[2])
    db.session.add(note)
    db.session.commit()

def query_users():
    query_users = RegisteredUsers.query.all()
    return query_users

@app.route('/announcements')
def announcements():
    pagename = 'announcements'
    return render_template('announcements.html', pagename=pagename)

@app.route('/syllabus')
def syllabus():
    pagename = 'syllabus'
    return render_template('syllabus.html', pagename=pagename)

@app.route('/courseteam')
def courseteam():
    pagename = 'courseteam'
    return render_template('courseteam.html', pagename=pagename)

@app.route('/feedback')
def feedback():
    pagename = 'feedback'
    return render_template('feedback.html', pagename=pagename)

@app.route('/lectut')
def lectut():
    pagename = 'lectut'
    return render_template('lectut.html', pagename=pagename)

@app.route('/assignments')
def assignments():
    pagename = 'assignments'
    return render_template('assignments.html', pagename=pagename)

@app.route('/resources')
def resources():
    pagename = 'resources'
    return render_template('resources.html', pagename=pagename)

@app.route('/signuphome')
def signuphome():
    pagename = 'signuphome'
    return render_template('home.html', pagename=pagename)

if __name__ == '__main__':
    app.run(debug=True)
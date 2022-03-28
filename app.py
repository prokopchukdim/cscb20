from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


app = Flask(__name__)
app.config['SECRET_KEY'] = '#\xc8Wj\xa4\xe8\x9a\x88\x18\x88\xd0\x91\xf3\xa0\xea'
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
    utorid = db.Column(db.String(20), primary_key=True)
    coursecomponent = db.Column(db.String(100), nullable=False)
    mark = db.Column(db.Integer, nullable = False)
    s_id = db.Column(db.String(20), db.ForeignKey('RegisteredUsers.utorid'))
    def __repr__(self):
        return f"Student('{self.utorid}', '{self.coursecomponent}', '{self.mark}')"

class Instructor(db.Model):
    __tablename__ = 'Instructor'
    utorid = db.Column(db.String(20), primary_key = True)
    s_id = db.Column(db.String(20), db.ForeignKey('Student.utorid'), nullable=False)
    s_coursecomponent = db.Column(db.String(20), db.ForeignKey('Student.coursecomponent'), nullable=False)
    s_mark = db.Column(db.Integer, db.ForeignKey('Student.mark'), nullable=False)

    """ person_id = db.Column(db.Integer, db.ForeignKey('Person.id'), nullable = False) """
    i_id = db.Column(db.Integer, db.ForeignKey('RegisteredUsers.utorid'), nullable=False)
    
    def __repr__(self):
        return f"Instructor('{self.utorid}', '{self.s_id}', '{self.s_coursecomponent}', '{self.s_mark}')"


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
        utorid = request.form['Utorid']
        email = request.form['Email']
        hashed_pswd = bcrypt.generate_password_hash(request.form['Password'])
        user_details =(
            utorid,
            email,
            hashed_pswd,
        )
        add_users(user_details)
        return redirect(url_for('login'))

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        utorid = request.form['utorid']
        pswd = request.form['pswd']
        user = RegisteredUsers.query.filter_by(utorid=utorid).first()
        if not user or not bcrypt.check_password_hash(user.password, pswd):
            flash('Please check your login details and try again', 'error')
            return render_template('login.html')
        else:
            session['name'] = utorid
            return redirect(url_for('login_success', name=utorid))
    else:
        if 'name' in session:
            print('im here lol')
            flash('already logged in!')
            return redirect(url_for('home'))
        else:
            return render_template('login.html')

@app.route('/login_success/<name>')
def login_success(name):
    return render_template('login_success.html', name=name)

@app.route('/logout')
def logout():
    session.pop('name', default = None)
    return redirect(url_for('home'))


@app.route('/marks')
def marks():
    return render_template('marks.html')


def add_users(user_details):
    user = RegisteredUsers(utorid = user_details[0], email = user_details[1], password = user_details[2])
    db.session.add(user)
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

@app.route('/remark')
def remark():
    return render_template('remark.html')
    
if __name__ == '__main__':
    app.run(debug=True)
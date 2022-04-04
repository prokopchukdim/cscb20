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
    usertype = db.Column(db.String(20))
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(20), nullable = False)

    student = db.relationship('Student', backref='author', lazy=True)
    remark = db.relationship('Remark', backref='author', lazy=True)

    def __repr__(self):
        return f"RegisteredUsers('{self.usertype}','{self.utorid}', '{self.password}')"

class Student(db.Model):
    __tablename__ = 'Student'
    utorid = db.Column(db.String(20), db.ForeignKey('RegisteredUsers.utorid'), primary_key=True, nullable=False)
    coursecomponent = db.Column(db.String(100), nullable=False, primary_key=True)
    mark = db.Column(db.Integer, nullable = False)
    

    def __repr__(self):
        return f"Student('{self.utorid}', '{self.coursecomponent}', '{self.mark}')"

class Remark(db.Model):
    __tablename__ = 'Remark'
    utorid = db.Column(db.String(20), db.ForeignKey('RegisteredUsers.utorid'), primary_key=True, nullable=False)
    coursecomponent = db.Column(db.String(100), nullable=False, primary_key=True)
    mark = db.Column(db.Integer, nullable = False)
    remark = db.Column(db.String(300), primary_key=True, nullable=False)
    remarkstatus = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"Remark('{self.utorid}', '{self.coursecomponent}', '{self.mark}', '{self.remark}', '{self.remarkstatus})"

class Feedback(db.Model):
    __tablename__ = 'Feedback'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    q1 = db.Column(db.String(300), nullable = False)
    q2 = db.Column(db.String(300), nullable = False)
    q3 = db.Column(db.String(300), nullable = False)
    q4 = db.Column(db.String(300), nullable = False)
    date_sent = db.Column(db.DateTime, nullable = False, default = datetime.now())
    instructor_id = db.Column(db.String(20), db.ForeignKey('RegisteredUsers.utorid'), nullable = False)

    def __repr__(self):
        return f"Feedback('{self.id}', '{self.q1}', '{self.q2}', '{self.q3}', '{self.q4}', '{self.date_sent}', '{self.instructor_id}')"

@app.route('/')
@app.route('/home')
def home():
    pagename = 'home'
    return render_template('unsignedhome.html', pagename=pagename)

@app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        utorid = request.form['Utorid']
        email = request.form['Email']
        hashed_pswd = bcrypt.generate_password_hash(request.form['Password'])
        
        #Parse user type
        if request.form.get('Instructor'):
            usertype = 'instructor'
        elif request.form.get('Student'):
            usertype = 'student'
        else:
            flash('Please select a user type and try again', 'error')
            return redirect(url_for('register'))

        #Parse if user already exists
        if (RegisteredUsers.query.filter_by(utorid=utorid).first()):
            flash('User already exists. Please use a different utorid', 'error')
            return redirect(url_for('register'))

        user_details =(
            utorid,
            usertype,
            email,
            hashed_pswd
            )
        add_users(user_details)
        return redirect(url_for('login'))

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        utorid = request.form['utorid']
        pswd = request.form['pswd']
        
        if request.form.get('Instructor'):
            usertype = 'instructor'
        elif request.form.get('Student'):
            usertype = 'student'
        else:
            flash('Please select a user type and try again', 'error')
            return redirect(url_for('login'))
        
        # user = RegisteredUsers.query.filter_by(utorid=utorid).first()
        user = db.engine.execute("select * from RegisteredUsers where utorid = :utorid and usertype = :usertype", {'utorid':utorid, 'usertype':usertype}).first()
        # if user:
        #     print("There is a user!")

        if not user or not bcrypt.check_password_hash(user['password'], pswd):
            flash('Please check your login details and try again', 'error')
            return render_template('login.html')
        else:
            session['name'] = utorid
            session['type'] = usertype
            return redirect(url_for('login_success')) #, name=utorid))
    else:
        if 'name' in session:
            flash('already logged in!')
            return redirect(url_for('login_success')) #, name=session['name']))
        else:
            return render_template('login.html')

@app.route('/login_success') #/<name>')
def login_success(): #name):
    return render_template('login_success.html') #, name=name)

@app.route('/logout')
def logout():
    session.pop('name', default = None)
    session.pop('type', default = None)
    return redirect(url_for('home'))

@app.route('/entermarks', methods =['GET', 'POST'])
def entermarks():
    if request.method == 'GET':
        return render_template('entermarks.html')
    else:
        utorid = request.form['utorid']
        coursecomponent = request.form['coursecomp']
        mark = request.form['mark']
        student_mark_details = (
            utorid,
            coursecomponent, 
            mark
        )
        add_marks(student_mark_details)
        return redirect(url_for('entermarks'))

@app.route('/viewmarks', methods = ['GET', 'POST'])
def viewmarks():
    if request.method == 'GET':
        user = db.engine.execute("select * from Student ORDER BY utorid, coursecomponent").all()
        return render_template('viewmarks.html', user=user)
    else:
        utorid = request.form['utorid']
        coursecomponent = request.form['coursecomp']
        mark = request.form['remark']
        remarkstatus = 'closed'
        student_mark_details = (
            utorid,
            coursecomponent, 
            mark,
            remarkstatus
        )
        change_marks(student_mark_details)
        return redirect(url_for('viewmarks'))

@app.route('/remark', methods = ['GET', 'POST'])
def remark():
    if request.method == 'GET':
        user = db.engine.execute("select * from Remark").all()
        return render_template('remark.html', user=user)
    else:
        utorid = request.form['utorid']
        coursecomponent = request.form['coursecomp']
        mark = request.form['remark']
        remarkstatus = 'closed'
        student_mark_details = (
            utorid,
            coursecomponent, 
            mark,
            remarkstatus
        )
        change_marks(student_mark_details)
        return redirect(url_for('remark'))

@app.route('/marks')
def marks():
    if session['type'] == 'instructor':
       return render_template('marks.html')
    else:
        utorid = session['name']
        user = db.engine.execute("select * from Student where utorid = :utorid", {'utorid':utorid}).all()
        return render_template('marks.html', user=user)


@app.route('/remarkstatus')
def remarkstatus():
    utorid = session['name']
    user = db.engine.execute("select * from Remark where utorid = :utorid", {'utorid' :utorid}).all()
    return render_template('remarkstatus.html', user=user)

@app.route('/studentremark', methods = ['GET', 'POST'])
def studentremark():
    if request.method == 'GET':
        return render_template('studentremark.html')
    else:
        utorid = session['name']
        coursecomponent = request.form['remark-input-1'] 
        mark = request.form['remark-input-2'] 
        remark = request.form['remark']
        remarkstatus = request.form['remark-input-3']
        remarkexists = db.engine.execute("select * from Remark where utorid = :utorid and coursecomponent = :coursecomponent", {'utorid':utorid, 'coursecomponent':coursecomponent}).first()
        if remarkexists:
            db.engine.execute("UPDATE Remark SET remark = :remark WHERE utorid = :utorid AND coursecomponent = :coursecomp", {'mark':remarkexists[2], 'utorid':remarkexists[0], 'coursecomp':remarkexists[1], 'remarkstatus': remarkexists[4], 'remark': remark})
            
        else:
            student_mark_details = (
                utorid,
                coursecomponent, 
                mark,
                remark, 
                remarkstatus
            )
            add_remarks(student_mark_details)
        return redirect(url_for('studentremark'))

def add_users(user_details):
    user = RegisteredUsers(utorid = user_details[0], usertype = user_details[1], email = user_details[2], password = user_details[3])
    db.session.add(user)
    db.session.commit()

def add_marks(student_mark_details):
    student = Student(utorid = student_mark_details[0], coursecomponent = student_mark_details[1], mark = student_mark_details[2])
    db.session.add(student)
    db.session.commit()

def add_remarks(student_remark_details):
    student = Remark(utorid = student_remark_details[0], coursecomponent = student_remark_details[1], mark = student_remark_details[2], remark = student_remark_details[3], remarkstatus = student_remark_details[4])
    db.session.add(student)
    db.session.commit()

def change_marks(student_mark_details):
    db.engine.execute("UPDATE Student SET mark = :mark WHERE utorid = :utorid AND coursecomponent = :coursecomp", {'mark':student_mark_details[2], 'utorid':student_mark_details[0], 'coursecomp':student_mark_details[1]})
    db.engine.execute("UPDATE Remark SET mark = :mark WHERE utorid = :utorid AND coursecomponent = :coursecomp", {'mark':student_mark_details[2], 'utorid':student_mark_details[0], 'coursecomp':student_mark_details[1], 'remarkstatus': student_mark_details[3]})
    db.engine.execute("UPDATE Remark SET remarkstatus = :remarkstatus WHERE utorid = :utorid AND coursecomponent = :coursecomp", {'mark':student_mark_details[2], 'utorid':student_mark_details[0], 'coursecomp':student_mark_details[1], 'remarkstatus': student_mark_details[3]})

def query_users():
    query_users = RegisteredUsers.query.all()
    return query_users

def query_instructors():
    query_instructors = RegisteredUsers.query.filter_by(usertype = 'instructor')
    query_instructors = enumerate(query_instructors)
    return query_instructors

def add_feedback(feedback_details):
    feedback = Feedback(q1 = feedback_details[0], q2 = feedback_details[1], q3 = feedback_details[2], q4 = feedback_details[3], instructor_id = feedback_details[4])
    db.session.add(feedback)
    db.session.commit()

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

@app.route('/feedback', methods = ['GET', 'POST'])
def feedback():
    pagename = 'feedback'
    query_instructors_result = query_instructors()
    if request.method == 'GET':
        return render_template('feedback.html', pagename=pagename, query_instructors_result = query_instructors_result)
    else:
        instructor = request.form['instructor']
        q1 = request.form['q1']
        q2 = request.form['q2']
        q3 = request.form['q3']
        q4 = request.form['q4']
        feedback_details =(
            q1,
            q2,
            q3,
            q4,
            instructor
        )
        add_feedback(feedback_details)
        return render_template('feedback.html', pagename=pagename, query_instructors_result = query_instructors_result)

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


@app.route('/unsignedhome')
def unsignedhome():
    pagename = 'home'
    return render_template('unsignedhome.html', pagename=pagename)

if __name__ == '__main__':
    app.run(debug=True)


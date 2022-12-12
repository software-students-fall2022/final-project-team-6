from flask_login import UserMixin, login_user, logout_user, login_required, current_user, LoginManager
from models.user import User

from flask import Blueprint, render_template, request, redirect, url_for, make_response, session, flash
from models.database import db
import json
import models.database as database

login_page = Blueprint("login", __name__)


def get_current_user():#pragma: no cover
    if current_user.is_authenticated:
        return User(id = current_user.id, username = current_user.username, school = current_user.school, subject = current_user.subject)
    return None


@login_page.route('/logout', methods = ['GET', 'POST'])
def logout(): #pragma: no cover
    logout_user()
    return redirect(url_for('index_page.home'))

def add_user_to_db(name, password, school, subject, database):
    user = database.Users.find_one({"username:": name})
    
    if(user == None):
        doc={
            "username": name,
            "password": password,
            'school': school,
            "subject": subject,
        }
        id = database.Users.insert_one(doc).inserted_id
        print(id)
        return User(id = id, username = name, school = school, subject = subject)
    else:
        return User(id = user['_id'], username = user['username'], school = user['school'], subject = user['subject'])

def get_user_object_in_db(username, database):
    user = database.Users.find_one({"username": username})
    if(user) == None:
        return None
    return User(id = user['_id'], username = user['username'], school = user['school'], subject = user['subject'])

def check_can_login(username, password, database):
    if(username == "" or password == ""):
        return False
    user = database.Users.find_one({"username": username})
    if(user):
        if(user['password'] == password):
            return True
    return False

def check_can_sign_up(username, password, school, subject, database):
    if(username == "" or password == "" or school == "" or subject == ""):
        return False
    user = get_user_object_in_db(username, database)
    if(user == None):
        return True
    return False


                                    
@login_page.route('/login', methods = ['POST'])
def login(): 
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.home'))
    
    name = request.form.get('username')
    password = request.form.get('password')
    if(check_can_login(name, password, db)):
        user_obj = get_user_object_in_db(name, db)
        login_user(user_obj)
        return redirect(url_for('dashboard.home'))
    else:
         return render_template('login.html', opac=1, msg="Invalid username and/or password")
 
@login_page.route('/sign_up_page', methods = ['GET'])
def sign_up_page():
    schools = database.fetch_all_schools(db)
    subjects = database.fetch_all_subjects(db)
    return render_template('sign_up.html', opac=1, msg="", schools=schools, subjects=subjects)
 
@login_page.route('/sign_up', methods = ['POST'])
def sign_up():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.home'))
    
    #print("sign_up called")
    #data = request.form.get
    #data= json.loads(request.data, strict=False)
    #print("data: ", data)
    #school = data["school"]
    school = request.form.get('school')
    subject = request.form.get('subject')
    name = request.form.get('username')
    password = request.form.get('password')
    #print("school: ", school) 
    #subject = data["subject"]
    #name = data["username"]
    #print("name: ", name)
    #password = data["password"]
    print("password: ", password)
   
    
    if(check_can_sign_up(name, password, school, subject, db)):
        user_obj = add_user_to_db(name, password, school, subject, db)
        login_user(user_obj)
        return redirect(url_for('dashboard.home'))
    else:
        schools = database.fetch_all_schools(db)
        subjects = database.fetch_all_subjects(db)
        if(name == "" or password == "" or school == "" or subject == ""):
            return render_template('sign_up.html', opac=1, msg="Please fill in all the fields", schools=schools, subjects=subjects)
        return render_template('sign_up.html', opac=1, msg="Username already exists", schools=schools, subjects=subjects)

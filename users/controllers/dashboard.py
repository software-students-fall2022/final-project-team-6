from flask import Blueprint, render_template, request, redirect, url_for, make_response, session, flash
from flask_login import current_user
from os.path import dirname, join, abspath
import sys
sys.path.append(dirname(dirname(abspath(__file__))))
import models.database as database
from models.database import db
from . import login
from bson.json_util import dumps

dashboard_page = Blueprint( "dashboard", __name__ )

@dashboard_page.route("/home", methods = ['GET', 'POST'])
def home():
    if not current_user.is_authenticated: 
        return redirect(url_for('index.home'))
  
    school = request.args.get('school')
    subject = request.args.get('subject')
    
    
    if school is None or subject is None:
        user = login.get_current_user()
        selectedSchool = user.school
        selectedSubject = user.subject
    else:
        selectedSchool = school
        selectedSubject = subject
    

    print("Selected school: " + selectedSchool)
    print("Selected subject: " + selectedSubject)
    schools = database.fetch_all_schools(db)
    subjects = database.fetch_all_subjects(db)
    
    courses = database.get_all_courses_by_school_subject_fullname(selectedSchool,selectedSubject, db)
    
    return render_template('courses/dashboard.html', schools=schools, subjects=subjects, selectedSchool=selectedSchool, selectedSubject=selectedSubject, courses=courses)
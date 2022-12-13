from flask import Blueprint, render_template, request, redirect, url_for, make_response, session, flash
from flask_login import current_user
from os.path import dirname, join, abspath
import sys
sys.path.append(dirname(dirname(abspath(__file__))))
import models.database as database
from models.database import db
from . import login
from bson.json_util import dumps

course_page = Blueprint( "course", __name__ )

@course_page.route("/details", methods = ['GET'])
def details():
    if not current_user.is_authenticated: 
        return redirect(url_for('index.home'))

    courseID = request.args.get('courseID')
    course = database.get_course_info_by_course_id(courseID, db)
    
    print("course: " + str(course))
    print("course instructors: " + course["instructors"])
    
    comments = database.get_course_comments(courseID, db)
    for comment in comments:
        print("commenter: " + comment.username + " comment: " + comment.comment)
    
    
    return render_template('courses/course_details.html', details = course, comments = comments)

@course_page.route("/submit_comment", methods = ['POST'])
def submit_comment():
    if not current_user.is_authenticated: 
        return redirect(url_for('index.home'))
    rating = request.form.get('rating')
    comment = request.form.get('comment')
    course_id = request.form.get('course_id')
    
    username = login.get_current_user().username
    database.add_comment(course_id= course_id, username = username, rating = rating, comment = comment, database=db)
    return redirect(url_for('course.details', courseID = course_id))
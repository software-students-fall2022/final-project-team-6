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

    courseName = request.args.get('courseFullname')
    course = database.get_course_info_by_course_name(courseName, db)
    
    print("course: " + str(course))
    print("course instructors: " + course["instructors"])
    
    comments = database.get_course_comments(courseName, db)
    for comment in comments:
        print("commenter: " + comment.username + " comment: " + comment.comment)
    
    overall_rating = database.calculate_ratings(comments)
    return render_template('courses/course_details.html', details = course, comments = comments, overall_rating = overall_rating)

@course_page.route("/submit_comment", methods = ['POST'])
def submit_comment():
    if not current_user.is_authenticated: 
        return redirect(url_for('index.home'))
    rating = request.form.get('rating')
    comment = request.form.get('comment')
    course_name = request.form.get('course_name')
    
    username = login.get_current_user().username
    database.add_comment(course_name= course_name, username = username, rating = rating, comment = comment, database=db)
    return redirect(url_for('course.details', courseFullname = course_name))
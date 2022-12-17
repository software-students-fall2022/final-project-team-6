from flask import Blueprint, render_template, request, redirect, url_for, make_response, session, flash
from os.path import dirname, join, abspath
import sys
sys.path.append(dirname(dirname(abspath(__file__))))
from . import database
from .database import db
from bson.json_util import dumps

course_page = Blueprint("course", __name__ )

@course_page.route("/details", methods = ['GET'])
def details():
    courseID = request.args.get('courseID')
    course = database.get_course_info_by_course_id(courseID, db)  
    comments = database.get_course_comments(courseID, db)
    return render_template('courses/course_details.html', details = course, comments = comments)

@course_page.route("/delete_course", methods = ['POST'])
def delete_course():
    commentID = request.form.get('comment_id')
    courseID = request.form.get('course_id')
    database.delete_course_comment(courseID,commentID, db)  
    
    return redirect(url_for('course.details', courseID = courseID))
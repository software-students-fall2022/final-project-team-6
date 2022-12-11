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

    course = request.args.get('courseFullname')
    
    return "Course details" + course
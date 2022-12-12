import os
from os.path import dirname, join
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bson.objectid import ObjectId
from flask import Flask, render_template, request, Blueprint, redirect, url_for, make_response, session, flash
import datetime
import os
import sys
from flask_login import current_user
from models.database import db



index_page = Blueprint( "index_page", __name__ )
app = Flask(__name__)
app.secret_key = "secret key"


@index_page.route('/')
def home():
    print("Authentification: " + str(current_user.is_authenticated))
    if current_user.is_authenticated: 
        return redirect(url_for('dashboard.home'))
    return render_template('login.html')

@index_page.route('/signup', methods = ['GET', 'POST'])
def signup():
     return redirect(url_for('login.sign_up_page'))


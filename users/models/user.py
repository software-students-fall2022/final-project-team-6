#reference: https://stackoverflow.com/questions/54992412/flask-login-usermixin-class-with-a-mongodb
from distutils.log import debug
from flask_login import UserMixin, current_user, login_user, logout_user, login_required
from flask import render_template, request, redirect, url_for, make_response, session, flash
from flask import Flask
from bson.objectid import ObjectId



class User(UserMixin):
    def __init__(self, id, username: str, school: str, subject: str):
        self.username = username
        if(isinstance(id, ObjectId)):
            id = str(id)
        self.id = id
        self.school = school
        self.subject = subject
    
    @staticmethod
    def is_authenticated():
        return True
    
    @staticmethod
    def is_active():
        return True
    
    @staticmethod
    def is_anonymous():
        return False
    
    
    def get_id(self):
        return self.id
    
   
    
   
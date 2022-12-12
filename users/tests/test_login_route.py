import os
from os.path import dirname, join, abspath
import sys
from flask import url_for
sys.path.append(dirname(dirname(abspath(__file__))))

from models.user import User
from controllers import login
from controllers import index

import pymongo
import ssl
from models.comment import Comment
from app import app

def test_login(): 
    #get 用 app.test_client().get()
    response = app.test_client().post("/login/login", data = {"username": "test", "password": "12345"}, follow_redirects=True)
    
    assert response.status_code == 200, "failed login test"

def test_signup_page():
    response = app.test_client().get("/login/sign_up_page")
    assert response.status_code == 200, "failed signup test"
    assert "User Sign-up" in str(response.data), "failed signup test"
    
def test_sign_up_route():
    response = app.test_client().post("/login/sign_up", data = {"username": "test", "password": "12345",
                                                              "school" : "test", "subject": "test"}, follow_redirects=True)
    
    assert response.status_code == 200, "failed signup test"
    
    
    
def test_comment():
    comment = Comment(username= "Danzai", comment= "This is a comment", rating= 5)
    assert comment.username == "Danzai", "failed comment test"
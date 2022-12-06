import pymongo
from bson.objectid import ObjectId
from flask import Flask, render_template, request, Blueprint, redirect, url_for, make_response, session, flash
import os
from io import BytesIO
import base64
import re
import datetime

def is_docker():
    path = '/proc/self/cgroup'
    return (
        os.path.exists('/.dockerenv') or
        os.path.isfile(path) and any('docker' in line for line in open(path))
    )

index_page = Blueprint( "index_page", __name__ )
app = Flask(__name__)
app.secret_key = "secret key"

if(is_docker()):
    client = pymongo.MongoClient("db", 27017)
else:
    client = pymongo.MongoClient("127.0.0.1", 27017)
   
   
db=client["Team6"]


@index_page.route('/')
def home():
    return render_template('/courses/hello_world.html')
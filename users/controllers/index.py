import pymongo
from bson.objectid import ObjectId
from flask import Flask, render_template, request, Blueprint, redirect, url_for, make_response, session, flash
import datetime
import os
import sys

index_page = Blueprint( "index_page", __name__ )

app = Flask(__name__)
app.secret_key = "secret key"

def is_docker():
    path = '/proc/self/cgroup'
    return (
        os.path.exists('/.dockerenv') or
        os.path.isfile(path) and any('docker' in line for line in open(path))
    )
if(is_docker()):
    client = pymongo.MongoClient("db", 27017)
else:
    client = pymongo.MongoClient("mongodb+srv://okkiris:F3iQz3hSCxOwhhOu@cluster0.ubegai3.mongodb.net/?retryWrites=true&w=majority")
    

db=client["Team6"]

@index_page.route('/')
def home():
    return render_template('/courses/hello_world.html')
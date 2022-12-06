import pymongo
from bson.objectid import ObjectId
from flask import Flask, render_template, request, Blueprint, redirect, url_for, make_response, session, flash
import datetime
import os
import sys
from dotenv import dotenv_values
config = dotenv_values(".env")
index_page = Blueprint( "index_page", __name__ )

app = Flask(__name__)
app.secret_key = "secret key"

client = pymongo.MongoClient(config["DB_CONNECTION_STRING"])   
db=client[config["DB_NAME"]]

@index_page.route('/')
def home():
    db.Test.insert_one({"emotion":"test2"})
    return render_template('/courses/hello_world.html')
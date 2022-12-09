import pymongo
from bson.objectid import ObjectId
from flask import Flask, render_template, request, Blueprint, redirect, url_for, make_response, session, flash
import os
from io import BytesIO
import base64
import re
import datetime
from dotenv import dotenv_values
import requests
import json

config = dotenv_values(".env")

index_page = Blueprint("index_page", __name__ )
app = Flask(__name__)
app.secret_key = "secret key"


client = pymongo.MongoClient(config["DB_CONNECTION_STRING"])   
db=client[config["DB_NAME"]]

url = 'https://schedge.a1liu.com/'

schoolDict = {}

def createSubjectsCollection():
    schoolsAPI = requests.get(url+"schools")
    schoolsAPI.encoding = 'utf-8'
    schools  = json.loads(str(schoolsAPI.text))

    subjectsAPI = requests.get(url+"subjects")
    subjectsAPI.encoding = 'utf-8'
    subjects  = json.loads(str(subjectsAPI.text))

    for abbr in schools.keys():
        key = {"schoolAbbr": abbr}
        data = {
            "$set":{"schoolFullname": schools[abbr]["name"]}
        }
        if abbr != "NT" and abbr != "ND":
            db.Schools.update_one(key, data, upsert=True)
            schoolDict[abbr] = schools[abbr]["name"]

    for school in subjects.keys():
        for abbr in subjects[school].keys():
            if school in schoolDict.keys():
                db.Schools.update_one({'schoolAbbr': school}, {'$push': {'subjects': {"subjectAbbr":abbr,"subjectFullname":subjects[school][abbr]["name"]}}},upsert=True)

@index_page.route('/')
def school():
    #only demonstrate school name 
    docs = db.Schools.find({},{ "_id":0, "schoolAbbr": 0, "subjects":0})
    
    #docs is list eg.  [{'schoolFullname': 'Tandon School of Engineering - Graduate'}, {'schoolFullname': 'School of Professional Studies'}]
    return render_template('/courses/school.html',docs=docs)

@index_page.route('/subject',methods = ["GET"])
def subject():
    school = request.args.get('schoolFullname')
    school = "Tandon School of Engineering"
    docs = db.Schools.find_one({"schoolFullname":school}, {"_id":0})

    docs = docs["subjects"]
    #docs is list eg. [{'subjectAbbr': 'VIP', 'subjectFullname': 'Vertically Integrated Projects'}]
    return render_template('/courses/subjects.html',docs=docs)


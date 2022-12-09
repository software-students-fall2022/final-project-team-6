import pymongo
from bson.objectid import ObjectId
from flask import Flask, render_template, request, Blueprint, redirect, url_for, make_response, session, flash
import os
from io import BytesIO
import base64
import re
import datetime
import requests
import json
from dotenv import dotenv_values


config = dotenv_values(".env")

index_page = Blueprint("index_page", __name__ )
app = Flask(__name__)
app.secret_key = "secret key"

   
client = pymongo.MongoClient(config["DB_CONNECTION_STRING"])   
db=client[config["DB_NAME"]]


@index_page.route('/')
def home():
    print(config["DB_CONNECTION_STRING"])
    db.Test.insert_one({"emotion":"test"})
    return render_template('/courses/hello_world.html')


@index_page.route('/course', methods=['GET'])
def course():
    school_name = request.args.get("school")
    subject_name = request.args.get("subject")

    school_name = "ua"
    subject_name = "csci"

    coursesAPI = requests.get("https://schedge.a1liu.com/current/current/"+school_name + "/" +subject_name )
    coursesAPI.encoding = 'utf-8'
    courses = json.loads(str(coursesAPI.text))

    docs = []
    for course in courses:
        course_name = course["name"]
        if (len(course["sections"])==1):
            docs.append(course_name)
        else:
            for section in course["sections"]:
                docs.append(course_name+" "+section["code"])
    for each in docs:
        print(each)
    return render_template('/courses/hello_world.html',docs=docs)


"""
{
    "name":"Undergraduate Research",
    "deptCourseId":"520",
    "subjectCode":{
        "code":"CSCI",
        "school":"UA"
        },
    "sections":[
        {
            "registrationNumber":7463,
            "code":"001",
            "instructors":["Staff"],
            "type":"Independent Study",
            "status":"Open",
            "meetings":null,
            "name":"Undergraduate Research",
            "minUnits":0.0,
            "maxUnits":4.0,
            "location":"TBA"
        }
    ]
}
"""
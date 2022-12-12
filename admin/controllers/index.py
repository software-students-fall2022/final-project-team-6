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
            doc = {}
            doc["name"] = course_name
            doc["deptCourseId"] = course["deptCourseId"]
            doc["code"] = course["subjectCode"]["code"]
            doc["school"] = course["subjectCode"]["school"]
            doc["registrationNumber"] = course["sections"][0]["registrationNumber"]
            doc["section_code"] = course["sections"][0]["code"]
            if len(course["sections"][0]["instructors"])==1:
                doc["instructors"] = course["sections"][0]["instructors"][0]
            else:
                instructors = ""
                for instructor in course["sections"][0]["instructors"]:
                    instructors += instructor
                    instructors += ","
                instructors = instructors[0:-1]
                doc["instructors"] = instructors
            doc["type"] = course["sections"][0]["type"]
            doc["status"] = course["sections"][0]["status"]
            # doc["section_code"] = course["sections"][0]["instructionMode"]
            doc["Units"] = course["sections"][0]["maxUnits"]
            doc["location"] = course["sections"][0]["location"]
            docs.append(doc)
        else:
            for section in course["sections"]:
                doc = {}
                doc["name"] = course_name+" "+section["code"]
                doc["deptCourseId"] = course["deptCourseId"]
                doc["code"] = course["subjectCode"]["code"]
                doc["school"] = course["subjectCode"]["school"]
                doc["registrationNumber"] = section["registrationNumber"]
                doc["section_code"] = section["code"]
                if len(section["instructors"])==1:
                    doc["instructors"] = section["instructors"][0]
                else:
                    instructors = ""
                    for instructor in section["instructors"]:
                        instructors += instructor
                        instructors += ","
                    instructors = instructors[0:-1]
                    doc["instructors"] = instructors
                doc["type"] = section["type"]
                doc["status"] = section["status"]
                # doc["section_code"] = section["instructionMode"]
                doc["Units"] = section["maxUnits"]
                doc["location"] = course["sections"][0]["location"]
                docs.append(doc)
                
    for each in docs:
        print(each)
    return render_template('/courses/hello_world.html',docs=docs)


"""
Left here for reference
Original Schema:
{
    "name":"Realtime and Big Data Analytics",
    "deptCourseId":"2436",
    "subjectCode":
    {
        "code":"CSCI",
        "school":"GA"
    },
    "sections":
    [
        {
            "registrationNumber":3539,
            "code":"001",
            "instructors":
            [
                "Yang Tang"
            ],
            "type":"Lecture",
            "status":"Closed",
            "meetings":
            [
                {
                    "beginDate":"2021-09-02 19:10:00",
                    "minutesDuration":110,
                    "endDate":"2021-12-14 23:59:00"
                }
            ],
            "instructionMode":"In-Person",
            "name":"Realtime and Big Data Analytics",
            "minUnits":0.0,
            "maxUnits":3.0,
            "location":"GCASL - Room: 461"
        }
    ]
}
Target Schema:
{
    "name" : "Ethics",
    "deptCourseId" : "40",
    "code" : "PHIL",
    "school" : "UA",
   "registrationNumber" : 23262.0,
    "code" : "001",
    "instructors" : "Sanford Laurence Diehl",
    "type" : "Lecture",
    "status" : "Open",
    "instructionMode" : "In-Person",
    "name" : "Ethics",
    "minUnits" : 0.0,
    "maxUnits" : 4.0,
    "location" : "Meyer Hall - Room: 122"    
}
"""


@index_page.route('/course', methods=['GET'])
def add_one_course_to_database():
    """
    get one course form frontend
    db.courses
    """
    pass
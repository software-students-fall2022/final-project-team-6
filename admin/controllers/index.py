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
        if abbr != "NT" and abbr != "ND" and abbr != "US" and abbr != "DC":
            db.Schools.update_one(key, data, upsert=True)
            schoolDict[abbr] = schools[abbr]["name"]

    for school in subjects.keys():
        for abbr in subjects[school].keys():
            if school in schoolDict.keys():
                db.Schools.update_one({'schoolAbbr': school}, {'$push': {'subjects': {"subjectAbbr":abbr,"subjectFullname":subjects[school][abbr]["name"]}}},upsert=True)

@index_page.route('/')
def home():
    #only demonstrate school name 
    docs = db.Schools.find({},{ "_id":0, "schoolAbbr": 0, "subjects":0})
    
    #docs is list eg.  [{'schoolFullname': 'Tandon School of Engineering - Graduate'}, {'schoolFullname': 'School of Professional Studies'}]
    return render_template('/courses/school.html',docs=docs)

@index_page.route('/course', methods=['GET'])
def course():
    schoolAbbr = request.args.get("school").upper()
    subjectAbbr = request.args.get("subject").upper()

    schoolAbbr = "UA"
    subjectAbbr = "CSCI"

    schoolFullname = db.Schools.find_one({"schoolAbbr":schoolAbbr},{"_id":0,"schoolFullname":1})["schoolFullname"]
    subjectFullname = db.Schools.find_one({"schoolAbbr":schoolAbbr},{"_id":0,"subjects":{"$elemMatch":{"subjectAbbr":subjectAbbr}}})["subjects"][0]["subjectFullname"]

    print(schoolFullname)
    print(subjectFullname)

    coursesAPI = requests.get("https://schedge.a1liu.com/current/current/"+schoolAbbr + "/" +subjectAbbr )
    coursesAPI.encoding = 'utf-8'
    courses = json.loads(str(coursesAPI.text))

    docs = []
    for course in courses:
        course_name = course["name"]
        if (len(course["sections"])==1):
            doc = {}
            doc["courseName"] = course_name
            doc["deptCourseId"] = course["deptCourseId"]
            doc["subjectAbbr"] = course["subjectCode"]["code"]
            doc["subjectFullname"] = subjectFullname
            doc["schoolAbbr"] = course["subjectCode"]["school"]
            doc["schoolFullname"] = schoolFullname
            doc["registrationNumber"] = course["sections"][0]["registrationNumber"]
            doc["section_code"] = course["sections"][0]["code"]
            #for adding ratemyprofessor url
            professor = course["sections"][0]["instructors"][0]
            rmpURL = "https://www.ratemyprofessors.com/"
            if professor != "Staff":
                query = professor.split(' ')
                rmpURL = "https://www.ratemyprofessors.com/search/teachers?query=" + query[0] + "%20" + query[1] + "&sid=U2Nob29sLTY3NQ=="
            doc["url"] = rmpURL
            ####
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
            if "instructionMode" in course["sections"][0].keys():
                doc["instructionMode"] = course["sections"][0]["instructionMode"]
            else:
                doc["instructionMode"] = "TBA"
            doc["units"] = course["sections"][0]["maxUnits"]
            doc["location"] = course["sections"][0]["location"]
            doc["display"] = False
            db.Courses.update_one({'courseName':doc["courseName"],  'schoolFullname':schoolFullname},{"$set":doc},upsert=True)
            obj = db.Courses.find_one({'courseName':doc["courseName"],  'schoolFullname':schoolFullname})
            doc["id"] = str(obj["_id"])
            doc["overallRating"] = 1
            docs.append(doc)
        else:
            for section in course["sections"]:
                doc = {}
                doc["courseName"] = course_name+" "+section["code"]
                doc["deptCourseId"] = course["deptCourseId"]
                doc["subjectAbbr"] = course["subjectCode"]["code"]
                doc["subjectFullname"] = subjectFullname
                doc["schoolAbbr"] = course["subjectCode"]["school"]
                doc["schoolFullname"] = schoolFullname
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
                #for adding ratemyprofessor url
                professor = section["instructors"][0]
                rmpURL = "https://www.ratemyprofessors.com/"
                if professor != "Staff":
                    query = professor.split(' ')
                    rmpURL = "https://www.ratemyprofessors.com/search/teachers?query=" + query[0] + "%20" + query[1] + "&sid=U2Nob29sLTY3NQ=="
                doc["url"] = rmpURL
                ####
                doc["type"] = section["type"]
                doc["status"] = section["status"]
                if "instructionMode" in section.keys():
                    doc["instructionMode"] = section["instructionMode"]
                else:
                    doc["instructionMode"] = "TBA"
                doc["units"] = section["maxUnits"]
                doc["location"] = section["location"]
                doc["display"] = False
                obj = db.Courses.update_one({'courseName':doc["courseName"], 'schoolFullname':schoolFullname},{"$set":doc},upsert=True)
                obj = db.Courses.find_one({'courseName':doc["courseName"],  'schoolFullname':schoolFullname})
                doc["id"] = str(obj["_id"])
                doc["overallRating"] = 1
                docs.append(doc)
    print(docs[0])
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
    "courseName" : "Ethics",
    "deptCourseId" : "40",
    "subjectAbbr" : "PHIL",
    "schoolAbbr" : "UA",
   "registrationNumber" : 23262.0,
    "code" : "001",
    "instructors" : "Sanford Laurence Diehl",
    "type" : "Lecture",
    "status" : "Open",
    "instructionMode" : "In-Person",
    "units" : 4.0,
    "location" : "Meyer Hall - Room: 122",
    "display" : False,
    "url" : "https://www.ratemyprofessors.com/search/teachers?query=Sanford%20Laurence%20Diehl&sid=U2Nob29sLTY3NQ=="
    "id" : '6397d5499cbb8d66ff9ade0f'，
    "overallRating" : 1
}
"""


@index_page.route('/course', methods=['POST'])
def displayCourse():
    courseID = request.form.get('courseID')
    db.Courses.update_one({'_id':ObjectId(courseID)},{'$set':{'display':True}}) #update the display field to True
    


@index_page.route('/subject',methods = ["GET"])
def subject():
    school = request.args.get('schoolFullname')
    school = "Tandon School of Engineering"
    docs = db.Schools.find_one({"schoolFullname":school}, {"_id":0})

    docs = docs["subjects"]
    #docs is list eg. [{'subjectAbbr': 'VIP', 'subjectFullname': 'Vertically Integrated Projects'}]
    return render_template('/courses/subjects.html',docs=docs)




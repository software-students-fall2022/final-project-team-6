import os
import sys
from os.path import dirname, join
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import pymongo
import requests
from dotenv import dotenv_values
from modules.requestCourses import getCourses

client = pymongo.MongoClient("mongodb+srv://doadmin:fj70nM43lo9I15S2@db-mongodb-nyc1-17689-274bdc70.mongo.ondigitalocean.com/admin?tls=true&authSource=admin&replicaSet=db-mongodb-nyc1-17689")   
db=client["Test"]

class Tests:
    def test_getCourses_csci_ua(self):
        schoolAbbr = "UA"
        subjectAbbr = "CSCI"

        coursesAPI = requests.get("https://schedge.a1liu.com/current/current/"+schoolAbbr + "/" +subjectAbbr + "?full=true" )
        coursesAPI.encoding = 'utf-8'
        courses = json.loads(str(coursesAPI.text))

        docs = []

        schoolFullname = db.Schools.find_one({"schoolAbbr":schoolAbbr},{"_id":0,"schoolFullname":1})["schoolFullname"]
        subjectFullname = db.Schools.find_one({"schoolAbbr":schoolAbbr},{"_id":0,"subjects":{"$elemMatch":{"subjectAbbr":subjectAbbr}}})["subjects"][0]["subjectFullname"]     
    
        for course in courses:
            course_name = course["name"]
            for section in course["sections"]:
                doc = {}
                doc["sectionName"] = section["name"]
                doc["courseName"] = course_name+" "+section["code"]
                doc["rawCourseName"] = course["name"]
                doc["deptCourseId"] = course["deptCourseId"]
                doc["subjectAbbr"] = course["subjectCode"]["code"]
                doc["subjectFullname"] = subjectFullname
                doc["schoolAbbr"] = course["subjectCode"]["school"]
                doc["schoolFullname"] = schoolFullname
                doc["registrationNumber"] = section["registrationNumber"]
                doc["section_code"] = section["code"]
                doc["type"] = section["type"]
                doc["status"] = section["status"]
                doc["location"] = section["location"]
                doc["grading"] = section["grading"]
                doc["campus"] = section["campus"]
                
                if "description" in course.keys():
                    doc["description"] = course["description"]
                else:
                    doc["description"] = ""

                if "notes" in section.keys():
                    doc["notes"] = section["notes"]
                else:
                    doc["notes"] = ""

                if "instructionMode" in section.keys():
                    doc["instructionMode"] = section["instructionMode"]
                else:
                    doc["instructionMode"] = "TBA"

                doc["units"] = section["maxUnits"]
                doc["location"] = section["location"]
                doc["display"] = False
                doc["rmpURLs"] = []
                doc["instructors"] = []
                doc["overallRating"] = -1

                obj = db.Courses.find_one({'courseName':doc["courseName"],  'schoolFullname':schoolFullname})
                doc["id"] = str(obj["_id"])
                docs.append(doc)
        assert docs == getCourses(db, schoolAbbr, subjectAbbr)

    def test_getCourses_math_ga(self):
        schoolAbbr = "GA"
        subjectAbbr = "MATH"

        coursesAPI = requests.get("https://schedge.a1liu.com/current/current/"+schoolAbbr + "/" +subjectAbbr + "?full=true" )
        coursesAPI.encoding = 'utf-8'
        courses = json.loads(str(coursesAPI.text))

        docs = []

        schoolFullname = db.Schools.find_one({"schoolAbbr":schoolAbbr},{"_id":0,"schoolFullname":1})["schoolFullname"]
        subjectFullname = db.Schools.find_one({"schoolAbbr":schoolAbbr},{"_id":0,"subjects":{"$elemMatch":{"subjectAbbr":subjectAbbr}}})["subjects"][0]["subjectFullname"]     
    
        for course in courses:
            course_name = course["name"]
            for section in course["sections"]:
                doc = {}
                doc["sectionName"] = section["name"]
                doc["courseName"] = course_name+" "+section["code"]
                doc["rawCourseName"] = course["name"]
                doc["deptCourseId"] = course["deptCourseId"]
                doc["subjectAbbr"] = course["subjectCode"]["code"]
                doc["subjectFullname"] = subjectFullname
                doc["schoolAbbr"] = course["subjectCode"]["school"]
                doc["schoolFullname"] = schoolFullname
                doc["registrationNumber"] = section["registrationNumber"]
                doc["section_code"] = section["code"]
                doc["type"] = section["type"]
                doc["status"] = section["status"]
                doc["location"] = section["location"]
                doc["grading"] = section["grading"]
                doc["campus"] = section["campus"]
                
                if "description" in course.keys():
                    doc["description"] = course["description"]
                else:
                    doc["description"] = ""

                if "notes" in section.keys():
                    doc["notes"] = section["notes"]
                else:
                    doc["notes"] = ""

                if "instructionMode" in section.keys():
                    doc["instructionMode"] = section["instructionMode"]
                else:
                    doc["instructionMode"] = "TBA"

                doc["units"] = section["maxUnits"]
                doc["location"] = section["location"]
                doc["display"] = False
                doc["rmpURLs"] = []
                doc["instructors"] = []
                doc["overallRating"] = -1

                obj = db.Courses.find_one({'courseName':doc["courseName"],  'schoolFullname':schoolFullname})
                doc["id"] = str(obj["_id"])
                docs.append(doc)
        assert docs == getCourses(db, schoolAbbr, subjectAbbr)
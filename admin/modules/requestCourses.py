import json
import requests

def getCourses(db,schoolAbbr,subjectAbbr):

    schoolAbbr = schoolAbbr.upper()
    subjectAbbr = subjectAbbr.upper()
    
    schoolFullname = db.Schools.find_one({"schoolAbbr":schoolAbbr},{"_id":0,"schoolFullname":1})["schoolFullname"]
    subjectFullname = db.Schools.find_one({"schoolAbbr":schoolAbbr},{"_id":0,"subjects":{"$elemMatch":{"subjectAbbr":subjectAbbr}}})["subjects"][0]["subjectFullname"]

    coursesAPI = requests.get("https://schedge.a1liu.com/current/current/"+schoolAbbr + "/" +subjectAbbr + "?full=true" )
    coursesAPI.encoding = 'utf-8'
    courses = json.loads(str(coursesAPI.text))

    docs = []
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
            db.Courses.update_one({'courseName':doc["courseName"], 'schoolFullname':schoolFullname},{"$set":doc},upsert=True)
            for professor in section["instructors"]:
                rmpURL = "https://www.ratemyprofessors.com/"
                if professor != "Staff":
                    query = professor.split(' ')
                    rmpURL = "https://www.ratemyprofessors.com/search/teachers?query=" + query[0] + "%20" + query[1] + "&sid=U2Nob29sLTY3NQ=="
                db.Courses.update_one({'courseName':doc["courseName"],  'schoolFullname':schoolFullname}, {'$pull': {'rmpURLs':rmpURL, 'instructors': professor}})
                db.Courses.update_one({'courseName':doc["courseName"],  'schoolFullname':schoolFullname}, {'$push': {'rmpURLs':rmpURL, 'instructors': professor}})

            obj = db.Courses.find_one({'courseName':doc["courseName"],  'schoolFullname':schoolFullname})
            doc["id"] = str(obj["_id"])
            docs.append(doc)
    return docs
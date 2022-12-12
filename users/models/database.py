import pymongo
from dotenv import dotenv_values
from .comment import Comment
from bson import json_util

config = dotenv_values(".env")

client = pymongo.MongoClient(config["DB_CONNECTION_STRING"])   
db=client[config["DB_NAME"]]


def fetch_all_schools(database):
    all_schools_in_db = database.Schools.find()

    all_schools = []
    all_schools = [school['schoolFullname'] for school in all_schools_in_db]
    return all_schools

def fetch_all_subjects(database):
    all_subjects_in_db = database.Schools.find()

    all_subjects = []
    all_subjects = [subject['subjects'] for subject in all_subjects_in_db]
    return all_subjects

def get_all_courses_by_subject_fullname(subject_fullname, database):
    all_courses_in_db = database.Courses.find({"subjectFullname": subject_fullname})
    return list(all_courses_in_db)

def get_course_info_by_course_name(course_name, database):
    course_info = database.Courses.find_one({"courseName": course_name})
    course_info = json_util.loads(json_util.dumps(course_info))
    return course_info

def get_course_comments(course_name, database):
    course_comments = database.Comments.find_one({"courseName": course_name})
    if(course_comments == None):
        return []
    
    comments = course_comments["comments"]
    comments_list = []
    if(comments != None):
        for comment in comments:
            comments_list.append(Comment(username = comment["username"], comment = comment["comment"], rating = int(comment["rating"])))
    return comments_list

def calculate_ratings(comments_list):
    if(len(comments_list) == 0):
        return -1
    total = 0
    for comment in comments_list:
        total += comment.rating
    return round(total / len(comments_list),1)

def add_comment(course_name, username, comment, rating, database):
    # check if course exists in comments collection
    if database.Comments.find_one({"courseName": course_name}) == None:
        database.Comments.insert_one({"courseName": course_name, "comments": []})
    
    #add a comment to the beginning of the comments list
    database.Comments.update_one({"courseName": course_name}, {"$push": {"comments": {"$each": [{"username": username, "comment": comment, "rating": rating}], "$position": 0}}})
    return
    
    
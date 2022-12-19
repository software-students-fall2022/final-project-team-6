import pymongo
from dotenv import dotenv_values
from .comment import Comment
from bson import json_util
from bson import ObjectId
config = dotenv_values(".env")

client = pymongo.MongoClient(config["DB_CONNECTION_STRING"])   
db=client[config["DB_NAME"]]


def fetch_all_schools(database):
    all_schools_in_db = database.Schools.find()

    all_schools = []
    all_schools = [school['schoolFullname'] for school in all_schools_in_db]
    return all_schools

def sortFunc(e):
  return e['subjectFullname']

def fetch_all_subjects(database):
    all_subjects_in_db = database.Schools.find()

    all_subjects = []
    all_subjects = [subject['subjects'] for subject in all_subjects_in_db]
    
    for subs in all_subjects:
        subs.sort(key=sortFunc)
        
    return all_subjects

def get_all_courses_by_school_subject_fullname(school_fullname, subject_fullname, database):
    all_courses_in_db = database.Courses.find({"subjectFullname": subject_fullname, "schoolFullname": school_fullname})
    if(all_courses_in_db == None):
        return []
    return list(all_courses_in_db)

def get_course_info_by_course_id(course_id, database):
    print("course id: " + course_id)
    course_info = database.Courses.find_one({"_id": ObjectId(course_id)})
    if(course_info == None):
        return None
    course_info = json_util.loads(json_util.dumps(course_info))
    return course_info

def get_course_comments(course_id, database):
    course_comments = database.Comments.find_one({"course_id": ObjectId(course_id)})
    if(course_comments == None):
        return []
    
    comments = course_comments["comments"]
    comments_list = []
    if(comments != None):
        for comment in comments:
            comments_list.append(Comment(username = comment["username"], comment = comment["comment"], rating = int(comment["rating"])))
    return comments_list

def calculate_overall_ratings(comments_list):
    if(len(comments_list) == 0):
        return -1
    total = 0
    for comment in comments_list:
        total += comment.rating
    return round(total / len(comments_list),1)


def update_overall_rating(course_id, database):
    comments_list = get_course_comments(course_id, database)
    ratings = calculate_overall_ratings(comments_list)
    if database.Comments.find_one({"course_id": ObjectId(course_id)}) == None:
       return
    database.Comments.update_one({"course_id": ObjectId(course_id)}, {"$set": {"overall_rating": ratings}})
    database.Courses.update_one({"_id": ObjectId(course_id)}, {"$set": {"overallRating": ratings}})
    
    
def add_comment(course_id, username, comment, rating, database):
    # check if course exists in comments collection
    if database.Comments.find_one({"course_id": ObjectId(course_id)}) == None:
        database.Comments.insert_one({"course_id": ObjectId(course_id), "comments": [], "overall_rating": -1})
        
    #add a comment to the beginning of the comments list
    database.Comments.update_one({"course_id": ObjectId(course_id)}, {"$push": {"comments": {"$each": [{"username": username, "comment": comment, "rating": rating, "comment_id": ObjectId()}], "$position": 0}}})
    
    update_overall_rating(course_id, database)
    return
    
def search(search_string, database):
    courses = database.Courses.find({"$or": [{ 'courseName' : { '$regex' : search_string, '$options' : 'i' }},
                                   { 'schoolFullname' : { '$regex' : search_string, '$options' : 'i' }},
                                   { 'instructors' : { '$regex' : search_string, '$options' : 'i' }},
                                   { 'subjectFullname' : { '$regex' : search_string, '$options' : 'i' }},
                                   { 'subjectAbbr' : { '$regex' : search_string, '$options' : 'i' }},
                                   { 'schoolAbbr' : { '$regex' : search_string, '$options' : 'i' }}]})
    if(courses == None):
        return []
    return list(courses)


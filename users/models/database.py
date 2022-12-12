import pymongo
from dotenv import dotenv_values

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
    
import sys
from os.path import dirname, join, abspath
sys.path.append(dirname(dirname(abspath(__file__))))

from flask.testing import FlaskClient
from app import app

page_url = '/database'

import json
import pymongo
from dotenv import dotenv_values
from bson import ObjectId
from bson import json_util
import pytest
from modules.editDatabase import update,show,disable,addAllCourses
from controllers.database import get_course_info_by_course_id,get_course_comments,calculate_overall_ratings, update_overall_rating, delete_course_comment
from controllers.comment import Comment

client = pymongo.MongoClient("mongodb+srv://doadmin:fj70nM43lo9I15S2@db-mongodb-nyc1-17689-274bdc70.mongo.ondigitalocean.com/admin?tls=true&authSource=admin&replicaSet=db-mongodb-nyc1-17689")   
db=client["Test"]

# def reset(): 
#  db.Comments.insert_one({
#      "_id" : ObjectId("639e39ca310adfdaab47acc7"),
#      "course_id" : ObjectId("639ab2579cbb8d66ffd0980e"),
#      "comments" : [
#         {
#             "username" : "rwafff",
#             "comment" : "just so so",
#             "rating" : "3",
#             "comment_id" : ObjectId("639e39ca310adfdaab47acc8")
#         }
#      ],
#      "overall_rating" : 3.0
#  })
# @pytest.fixture(autouse=True)
# def reset_database(): #pragma: no cover
#     reset()

class Tests:
    
    def test_addAll(self):
        response = addAllCourses(db,test=True)
        assert response == ('{"success": true}', 200, {'ContentType': 'application/json'})

    def test_displayAlltrue(self):
        response = show(db)
        assert response == ('{"success": true}', 200, {'ContentType': 'application/json'})

    def test_displayAllfalse(self):
        response = disable(db)
        assert response == ('{"success": true}', 200, {'ContentType': 'application/json'})

    def test_displayUpdate_true(self):
        response = update(db,"639d0ad69cbb8d66ff07f51f",True)
        assert response == ('{"success": true}', 200, {'ContentType': 'application/json'})

    def test_displayUpdate_false(self):
        response = update(db,"639d0ad69cbb8d66ff07f51f",False)
        assert response == ('{"success": true}', 200, {'ContentType': 'application/json'})

    def test_createSchoolsCollection(self):
        response = app.test_client().get('/database/createSchool')
        assert response.status_code == 200
        assert response.data == json.dumps({'success':True}).encode("utf-8")

    def test_get_course_info_by_course_id(self):
        course_info = db.Courses.find_one({"_id": ObjectId("639d0ad69cbb8d66ff07f51f")})
        course_info = json_util.loads(json_util.dumps(course_info))
        assert course_info == get_course_info_by_course_id("639d0ad69cbb8d66ff07f51f", db)

    def test_get_course_info_by_course_id_fail(self):
        assert None == get_course_info_by_course_id("639d0ad69cbb8d66fe07f51e", db)

    def test_get_course_comments(self):
        course_comments = db.Comments.find_one({"course_id": ObjectId("639ab2579cbb8d66ffd0980e")})
        comments = course_comments["comments"]
        comments_list = []
        for comment in comments:
            comments_list.append(Comment(username = comment["username"], comment = comment["comment"], rating = int(comment["rating"]), comment_id=str(comment["comment_id"])))
        test_comments_list = get_course_comments("639ab2579cbb8d66ffd0980e", db)
        for i in range(0, len(comments_list)):
            assert comments_list[i].username == test_comments_list[i].username
            assert comments_list[i].comment == test_comments_list[i].comment
            assert comments_list[i].rating == test_comments_list[i].rating
            assert comments_list[i].comment_id == test_comments_list[i].comment_id


    def test_get_course_comments_fail(self):
        comments_list = []
        assert comments_list == get_course_comments("639d0ad69cbb8d66ff07f51f", db)

    def test_calculate_overall_ratings(self):
        pass

    def test_calculate_overall_ratings_fail(self):
        comments_list = get_course_comments("639d0ad69cbb8d66ff07f51f", db)
        if(len(comments_list) == 0):
            return -1
        total = 0
        for comment in comments_list:
            total += comment.rating
        assert -1 == calculate_overall_ratings(comments_list)

    def test_update_overall_rating(self):
        assert update_overall_rating("639ab2579cbb8d66ffd0980e",db) == 0

    def test_update_overall_rating_fail(self):
        assert -1 == update_overall_rating("639d0ad69cbb8d66ff07f51f", db)

    def test_delete_course_comment(self):
        pass

    def test_delete_course_comment_fail(self):
        assert False == delete_course_comment("639d0ad69cbb8d66ff07f51f", None, db)


"""
Instance to test:
{
    "_id" : ObjectId("639e39ca310adfdaab47acc7"),
    "course_id" : ObjectId("639ab2579cbb8d66ffd0980e"),
    "comments" : [
        {
            "username" : "rwafff",
            "comment" : "just so so",
            "rating" : "3",
            "comment_id" : ObjectId("639e39ca310adfdaab47acc8")
        }
    ],
    "overall_rating" : 3.0
}
"""
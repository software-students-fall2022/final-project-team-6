import sys
from os.path import dirname, join, abspath
sys.path.append(dirname(dirname(abspath(__file__))))

import json

from flask.testing import FlaskClient
from app import app

page_url = '/database'

class Tests:
    def test_addAll(self):
        pass
    
    def test_displayAlltrue(self):
        response = app.test_client().get('/database/displayAlltrue')
        assert response.status_code == 200
        assert response.data == json.dumps({'success':True}).encode("utf-8")

    def test_displayAllfalse(self):
        response = app.test_client().get('/database/displayAllfalse')
        assert response.status_code == 200
        assert response.data == json.dumps({'success':True}).encode("utf-8")
    
    def test_displayUpdate_true(self):
        response = app.test_client().post('/database/update', json={'courseID':'639aa34c9cbb8d66ffcf1a35', 'display':'true'})
        assert response.status_code == 200
        assert response.data == json.dumps({'success':True}).encode("utf-8")
    
    def test_displayUpdate_false(self):
        response = app.test_client().post('/database/update', json={'courseID':'639aa34c9cbb8d66ffcf1a35', 'display':'false'})
        assert response.status_code == 200
        assert response.data == json.dumps({'success':True}).encode("utf-8")

    def test_createSchoolsCollection(self):
        response = app.test_client().get('/database/createSchool')
        assert response.status_code == 200
        assert response.data == json.dumps({'success':True}).encode("utf-8")
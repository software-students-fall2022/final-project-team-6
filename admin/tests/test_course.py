import sys
from os.path import dirname, join, abspath
sys.path.append(dirname(dirname(abspath(__file__))))

from flask.testing import FlaskClient
from app import app

class Tests:
    def test_details(self):
        response = app.test_client().get('/course/details',  query_string={'courseID':'639aa34c9cbb8d66ffcf1a35'})
        assert response.status_code == 200

    def test_delete_course(self):
        # response = app.test_client().post('/delete_course', query_string={'schoolAbbr':'UA'})
        # assert response.status_code == 200
        pass
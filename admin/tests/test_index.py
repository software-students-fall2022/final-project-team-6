import sys
from os.path import dirname, abspath
sys.path.append(dirname(dirname(abspath(__file__))))

from flask.testing import FlaskClient
from app import app

class Tests:
    def test_school(self):
        response = app.test_client().get('/')
        assert response.status_code == 200

    def test_subject(self):
        response = app.test_client().get('/subjects', query_string={'schoolAbbr':'UA'})
        assert response.status_code == 200

    def test_course(self):
        response = app.test_client().get('/courses', query_string={'schoolAbbr':'UA', 'subjectAbbr':'DS'})
        assert response.status_code == 200

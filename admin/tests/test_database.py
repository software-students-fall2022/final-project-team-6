import sys
from os.path import dirname, join, abspath
sys.path.append(dirname(dirname(abspath(__file__))))

from flask.testing import FlaskClient
from app import app

page_url = '/database'

class Tests:
    def test_addAll(self):
        # response = app.test_client().get('/database/addAll')
        # assert response.status_code == 200
        # assert response.data == json.dumps({'success':True})

        pass
    
    def test_displayAlltrue(self):
        pass

    def test_displayAllfalse(self):
        pass
    
    def test_displayUpdate(self):
        pass

    def test_createSchoolsCollection(self):
        pass
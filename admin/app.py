from flask import Flask
from controllers.index import index_page
from controllers.database import database_page
from controllers.course import course_page

app = Flask(__name__)
app.secret_key = "secret key"
app.register_blueprint( database_page,url_prefix = "/database" )
app.register_blueprint( course_page,url_prefix = "/course")
app.register_blueprint( index_page )

if __name__ == '__main__':
     app.run(host='127.0.0.1', port=7001, debug=True)

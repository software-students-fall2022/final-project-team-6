from flask import Flask
from controllers.index import index_page
from controllers.dashboard import dashboard_page
from controllers.login import login_page
from controllers.course import course_page
from dotenv import dotenv_values
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from models.database import db
from models.user import User
from bson.objectid import ObjectId
from flask import Blueprint, render_template, request, redirect, url_for, make_response, session, flash

app = Flask(__name__)
app.secret_key = "secret key"
login_manager = LoginManager()
login_manager.init_app(app)

app.register_blueprint( dashboard_page,url_prefix = "/dashboard" )
app.register_blueprint(login_page, url_prefix = "/login")
app.register_blueprint(course_page, url_prefix = "/course" )
app.register_blueprint( index_page )

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=6001, debug=True)

@login_manager.user_loader
def load_user(id):
    print("Loading user " + str(id) + "Type of id: " + str(type(id)))
    user = db.Users.find_one({"_id": ObjectId(id) })
    if not user:
        return None
    return User(id = user['_id'], username = user['username'], school = user['school'], subject = user['subject'])
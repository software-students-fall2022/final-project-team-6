from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user


dashboard_page = Blueprint( "dashboard", __name__ )

@dashboard_page.route("/dashboard_main")
def dashboard_main():
    if not current_user.is_authenticated: 
        return redirect(url_for('index.home'))
    return render_template('hello_world.html')

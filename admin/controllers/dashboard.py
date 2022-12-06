from flask import Blueprint, render_template

dashboard_page = Blueprint( "dashboard", __name__ )

@dashboard_page.route("/")
def display():
    return "hello"

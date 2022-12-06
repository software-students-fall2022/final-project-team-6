from flask import Blueprint, render_template

gallery_page = Blueprint( "dashboard", __name__ )

@gallery_page.route("/")
def display():
    return "hello"

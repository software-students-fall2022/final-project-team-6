from flask import Flask, render_template, request, Blueprint, redirect, url_for, make_response, session, flash


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('/hello_world.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000, debug=True)


from flask import render_template
from http_server_pkg.app import app


@app.route('/')
@app.route('/index')
def index():

    return render_template('index.html')
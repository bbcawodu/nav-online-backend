from flask import render_template
from flask import flash
from flask import redirect
from patient_assist_admin.app import app


@app.route('/')
@app.route('/index')
def index():

    return render_template('index.html')

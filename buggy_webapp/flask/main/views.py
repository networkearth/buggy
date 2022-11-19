import requests

from flask import render_template, redirect, url_for, current_app
from flask_login import login_required, current_user
from . import main

@main.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@main.route('/submissions', methods=['GET'])
@login_required
def submissions_view():
    data = {
        'kobo_username': current_app.config['KOBO_USERNAME'],
        'kobo_password': current_app.config['KOBO_PASSWORD'],
        'kobo_uid': current_app.config['KOBO_UID'],
        'email': current_user.email,

    }
    api_url = '/'.join([
        current_app.config['API_URL'], 
        'submissions'
    ])
    response = requests.get(api_url, json=data)
    print(response.json())
    return render_template('submissions.html')

@main.route('/submissions', methods=['POST'])
@login_required
def submissions_post():
    return redirect(url_for('main.submissions_view'))
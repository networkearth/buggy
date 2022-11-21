import requests

from flask import render_template, redirect, url_for, current_app, make_response, request
from flask_login import login_required, current_user
from . import main

@main.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@main.route('/submissions', methods=['GET'])
@login_required
def submissions_view():
    payload = {
        'kobo_username': current_app.config['KOBO_USERNAME'],
        'kobo_password': current_app.config['KOBO_PASSWORD'],
        'kobo_uid': current_app.config['KOBO_UID'],
        'email': current_user.email,
    }
    api_url = '/'.join([
        current_app.config['API_URL'], 
        'submissions'
    ])
    response = requests.get(api_url, json=payload)
    submission_data = {}
    for submission in response.json():
        submission_data[submission['instance']] = {
            'uid': current_app.config['KOBO_UID'],
            'images': submission['images']
        }
    return render_template('submissions.html', submission_data=submission_data)

@main.route('/submissions', methods=['POST'])
@login_required
def submissions_post():
    # checked instances will show up in the keys
    payload = {
        'kobo_username': current_app.config['KOBO_USERNAME'],
        'kobo_password': current_app.config['KOBO_PASSWORD'],
        'kobo_uid': current_app.config['KOBO_UID'],
        'inaturalist_email': current_user.email,
        'inaturalist_password': current_user.password,
        'instances': ','.join(sorted(request.form))
    }
    api_url = '/'.join([
        current_app.config['API_URL'],
        'job'
    ])
    requests.post(api_url, json=payload)
    return redirect(url_for('main.submissions_view'))

@main.route('/image/<int:instance>/<int:id>', methods=['GET'])
@login_required
def image(instance, id):
    payload = {
        'kobo_username': current_app.config['KOBO_USERNAME'],
        'kobo_password': current_app.config['KOBO_PASSWORD'],
        'kobo_uid': current_app.config['KOBO_UID'],
        'instance': instance,
        'id': id
    }
    api_url = '/'.join([
        current_app.config['API_URL'],
        'image'
    ])
    image = requests.get(api_url, json=payload)
    response = make_response(image.content)
    response.headers.set('Content-Type', 'image/jpeg')
    response.headers.set('Cache-Control', 'private, max-age=7200')
    return response
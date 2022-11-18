from flask import render_template, redirect, url_for
from flask_login import login_required
from . import main

@main.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@main.route('/submissions', methods=['GET'])
@login_required
def submissions_view():
    return render_template('submissions.html')

@main.route('/submissions', methods=['POST'])
@login_required
def submissions_post():
    return redirect(url_for('main.submissions_view'))
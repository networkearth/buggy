from flask import redirect, render_template, url_for, request
from flask_login import login_user
from . import auth

from ..models import User

@auth.route('/login', methods=['GET'])
def login_get():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')

    user = User(f'{email} {password}')

    login_user(user, remember=True)

    return redirect(url_for('main.home'))
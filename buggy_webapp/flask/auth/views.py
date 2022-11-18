from flask import redirect, render_template, url_for, request
from flask_login import login_user, logout_user, login_required
from . import auth

from ..models import User

@auth.route('/login', methods=['GET'])
def login_view():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')

    user = User(f'{email} {password}')

    login_user(user, remember=True)

    return redirect(url_for('main.home'))

@auth.route('/logout', methods=['GET'])
@login_required
def logout_get():
    return render_template('logout.html')

@auth.route('/logout', methods=['POST'])
@login_required
def logout_post():
    logout_user()
    return redirect(url_for('main.home'))

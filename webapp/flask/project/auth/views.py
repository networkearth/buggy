"""
Auth views
"""

from gluon.inaturalist import client as inaturalist_client
from flask_login import login_user, logout_user, login_required
from flask import redirect, render_template, url_for, request, current_app, flash

from . import auth

from ..models import User

@auth.route('/login', methods=['GET'])
def login_view():
    """
    Login form
    """
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    """
    Attempts user login and redirects to page
    that requested login (if there is one)
    """
    email = request.form.get('email')
    password = request.form.get('password')

    login_succeeded = True
    try:
        client = inaturalist_client.iNaturalistClient(
            email,
            password,
            current_app.config['INATURALIST_APP_ID'],
            current_app.config['INATURALIST_APP_SECRET'],
            api_url=current_app.config['INATURALIST_API_URL'],
            app_url=current_app.config['INATURALIST_APP_URL']
        )
        # pylint: disable=protected-access
        client._get_new_token()
    # pylint: disable=broad-except
    except Exception:
        login_succeeded = False

    if login_succeeded:
        user = User(f'{email} {password}')

        login_user(user, remember=True)

        up_next = request.args.get('next')
        up_next = up_next if up_next else url_for('main.home')

        return redirect(up_next)

    flash('Incorrect credentials')
    return redirect(url_for('auth.login_view'))

@auth.route('/logout', methods=['GET'])
@login_required
def logout_get():
    """
    Logout form
    """
    return render_template('logout.html')

@auth.route('/logout', methods=['POST'])
@login_required
def logout_post():
    """
    Logs a user out and returns them to the
    splash page
    """
    logout_user()
    return redirect(url_for('main.home'))

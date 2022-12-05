from flask import redirect, render_template, url_for, request, current_app, flash
from flask_login import login_user, logout_user, login_required

from gluon.inaturalist import client as inaturalist_client

from . import auth

from ..models import User

@auth.route('/login', methods=['GET'])
def login_view():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
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
        client._get_new_token()
    except Exception:
        login_succeeded = False

    if login_succeeded:
        user = User(f'{email} {password}')

        login_user(user, remember=True)

        up_next = request.args.get('next')
        up_next = up_next if up_next else url_for('main.home')

        return redirect(up_next)
    else:
        flash('Incorrect credentials')
        return redirect(url_for('auth.login_view'))

@auth.route('/logout', methods=['GET'])
@login_required
def logout_get():
    return render_template('logout.html')

@auth.route('/logout', methods=['POST'])
@login_required
def logout_post():
    logout_user()
    return redirect(url_for('main.home'))

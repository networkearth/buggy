import os
import boto3
import json

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager

bootstrap = Bootstrap()

def create_app():
    app = Flask(__name__)

    app.config['ENVIRONMENT'] = os.environ['APP_ENVIRONMENT']
    app.config['NAMESPACE'] = os.environ['APP_NAMESPACE']
    app.config['ACCOUNT'] = os.environ['APP_ACCOUNT']
    app.config['REGION'] = os.environ['APP_REGION']

    SECRETS = {
        'INATURALIST_API_URL': {
            'secret_id': 'inaturalist',
            'key': 'api'
        },
        'INATURALIST_APP_URL': {
            'secret_id': 'inaturalist',
            'key': 'webapp'
        },
        'INATURALIST_APP_ID': {
            'secret_id': 'inaturalist',
            'key': 'app_id'
        },
        'INATURALIST_APP_SECRET': {
            'secret_id': 'inaturalist',
            'key': 'app_secret'
        },
        'SECRET_KEY': {
            'secret_id': 'secret-key',
            'key': 'secret_key'
        },
        'KOBO_UID': {
            'secret_id': 'kobo',
            'key': 'uid'
        },
        'KOBO_USERNAME': {
            'secret_id': 'kobo',
            'key': 'username'
        },
        'KOBO_PASSWORD': {
            'secret_id': 'kobo',
            'key': 'password'
        }
    }

    session = boto3.session.Session()
    client = session.client(
    service_name='secretsmanager',
    region_name=app.config['REGION']
    )
    for key, info in SECRETS.items():
        secret_id = f'{app.config["NAMESPACE"]}-{app.config["ENVIRONMENT"]}-{info["secret_id"]}'
        response = client.get_secret_value(
            SecretId=secret_id
        )
        app.config[key] = json.loads(response['SecretString'])[info['key']]

    app.config['API_URL'] = os.environ['API_URL']

    bootstrap.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login_view'
    login_manager.init_app(app)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .models import User

    @login_manager.user_loader
    def load_user(id):
        return User(id)

    return app

app = create_app()
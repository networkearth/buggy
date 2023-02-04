"""
App Factory
"""

import json
import boto3

from flask_restful import Api
from flask import Flask

from .resources.submissions import Submissions
from .resources.image import Image
from .resources.jobs import Job
from .resources.index import Index

def create_app(environment, namespace, account, region):
    """
    App Factory
    """
    app = Flask(__name__)
    api = Api(app)

    app.config['ENVIRONMENT'] = environment
    app.config['NAMESPACE'] = namespace
    app.config['ACCOUNT'] = account
    app.config['REGION'] = region

    assert environment in ('test', 'dev', 'prod')

    # pylint: disable=invalid-name
    SECRETS = {
        'INATURALIST_API': {
            'secret_id': 'inaturalist',
            'key': 'api'
        },
        'INATURALIST_WEBAPP': {
            'secret_id': 'inaturalist',
            'key': 'webapp'
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

    app.config['JOB_BUCKET'] = '-'.join([
        app.config['NAMESPACE'], app.config['ENVIRONMENT'], 'job'
    ])
    app.config['BACKUP_BUCKET'] = '-'.join([
        app.config['NAMESPACE'], app.config['ENVIRONMENT'], 'backup'
    ])

    api.add_resource(Submissions, '/submissions')
    api.add_resource(Image, '/image')
    api.add_resource(Job, '/job')
    api.add_resource(Index, '/') # this is for the ECS healthcheck

    return app

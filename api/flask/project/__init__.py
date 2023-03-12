"""
App Factory
"""

from flask_restful import Api
from flask import Flask

from .resources.submissions import Submissions
from .resources.image import Image
from .resources.jobs import Job
from .resources.index import Index

def create_app(api_uri, webapp_uri, backup_path):
    """
    App Factory
    """
    app = Flask(__name__)
    api = Api(app)

    app.config['INATURALIST_API'] = api_uri
    app.config['INATURALIST_WEBAPP'] = webapp_uri
    app.config['BACKUP_PATH'] = backup_path

    api.add_resource(Submissions, '/submissions')
    api.add_resource(Image, '/image')
    api.add_resource(Job, '/job')
    api.add_resource(Index, '/') # this is for the ECS healthcheck

    return app

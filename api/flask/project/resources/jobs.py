"""
/job endpoint
"""

from flask_restful import Resource, reqparse
from flask import current_app

from ..submissions import submissions
from ..uploaders import uploaders

class Job(Resource):
    """
    /job endpoint
    """
    parser = reqparse.RequestParser()
    parser.add_argument(
        'kobo_username',
        type=str,
        required=True,
        help='Kobo username'
    )
    parser.add_argument(
        'kobo_password',
        type=str,
        required=True,
        help='Kobo password'
    )
    parser.add_argument(
        'kobo_uid',
        type=str,
        required=True,
        help='uid of Kobo project'
    )
    parser.add_argument(
        'inaturalist_email',
        type=str,
        required=True,
        help='iNaturalist email'
    )
    parser.add_argument(
        'inaturalist_password',
        type=str,
        required=True,
        help='iNaturalist password'
    )
    parser.add_argument(
        'client_id',
        type=str,
        required=True,
        help='client_id'
    )
    parser.add_argument(
        'client_secret',
        type=str,
        required=True,
        help='client_secret'
    )
    parser.add_argument(
        'instances',
        type=str,
        required=True,
        help='instance ids'
    )

    def post(self):
        """
        POST /job
        """
        kwargs = Job.parser.parse_args()

        data = submissions.get_submissions(**kwargs)

        instances = [
            int(instance.strip())
            for instance in kwargs['instances'].split(',')
            if instance.strip()
        ]
        data = [
            submission for submission in data
            if submission['instance'] in instances
        ]

        uploaders.upload_submissions(
            data, current_app.config['BACKUP_PATH'],
            kwargs['kobo_username'], kwargs['kobo_password'],
            kwargs['kobo_uid'], kwargs['inaturalist_email'],
            kwargs['inaturalist_password'], kwargs['client_id'],
            kwargs['client_secret'], current_app.config['INATURALIST_API'],
            current_app.config['INATURALIST_WEBAPP']
        )

        return {}, 201

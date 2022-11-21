import json
import boto3

from flask import current_app
from flask_restful import Resource, reqparse
from time import time

class Job(Resource):
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
        'instances',
        type=str,
        required=True,
        help='instance ids'
    )

    def post(self):
        kwargs = Job.parser.parse_args()
        key = f'{kwargs["inaturalist_email"]}-{int(time())}.json'
        data = {
            'instances': [
                int(instance.strip()) 
                for instance in kwargs['instances'].split(',') 
                if instance.strip()
            ],
            'inaturalist_email': kwargs['inaturalist_email'],
            'inaturalist_password': kwargs['inaturalist_password'],
            'kobo_username': kwargs['kobo_username'],
            'kobo_password': kwargs['kobo_password'],
            'kobo_uid': kwargs['kobo_uid']
        }

        s3 = boto3.client('s3')
        s3.put_object(
            Body=json.dumps(data, indent=4, sort_keys=True),
            Bucket=current_app.config['JOB_BUCKET'],
            Key=key
        )
        return {}, 201
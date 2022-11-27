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
            'client_id': kwargs['client_id'],
            'client_secret': kwargs['client_secret'],
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

        email = kwargs['inaturalist_email']
        batch = boto3.client('batch')
        batch.submit_job(
            jobQueue='arn:aws:batch:us-east-1:575101084097:job-queue/buggy',
            jobName=f'pushtoinat',
            jobDefinition='arn:aws:batch:us-east-1:575101084097:job-definition/buggy-dev-push-to-inat',
            containerOverrides={
                'command': [
                    '-e',
                    email,
                    '-b',
                    current_app.config['JOB_BUCKET'],
                    '-bb',
                    current_app.config['BACKUP_BUCKET'],
                    '-a',
                    'http://buggy-api-service-1105356497.us-east-1.elb.amazonaws.com',
                    '-ia',
                    'http://44.212.148.112:4000/v1',
                    '-iw',
                    'http://44.212.148.112:3000',
                    '-r',
                    'us-east-1'
                ]
            }
        )

        return {}, 201

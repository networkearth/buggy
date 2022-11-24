import os
import click
import boto3
import json
import requests

from gluon.inaturalist.client import iNaturalistClient
from gluon.kobo.client import KoboClient

def get_submissions(api_url, username, password, uid, email):
    payload = {
        'kobo_username': username,
        'kobo_password': password,
        'kobo_uid': uid,
        'email': email,
    }
    api_url = '/'.join([
        api_url, 
        'submissions'
    ])
    response = requests.get(api_url, json=payload)
    return response.json()

@click.command()
@click.option('-e', '--email', required=True, help='email to do uploads for')
@click.option('-b', '--bucket', required=True, help='bucket to look for jobs in')
@click.option('-a', '--api_url', required=True, help='api endpoint')
@click.option('-ia', '--inat_api', required=True, help='inat api url')
@click.option('-iw', '--inat_webapp', required=True, help='inat webapp url')
@click.option('-r', '--region', required=True, help='aws region')
def main(email, bucket, api_url, inat_api, inat_webapp, region):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket)

    objects = list(bucket.objects.filter(Prefix=email))
    if not objects:
        return

    instances = set()

    for object in objects:
        content = json.loads(object.get()['Body'].read().decode('utf-8'))
        kobo_username = content['kobo_username']
        kobo_password = content['kobo_password']
        kobo_uid = content['kobo_uid']
        inat_username = content['inaturalist_email']
        inat_password = content['inaturalist_password']
        inat_client_id = content['client_id']
        inat_client_secret = content['client_secret']
        instances.update(content['instances'])

    overall_submissions = get_submissions(
        api_url,
        kobo_username,
        kobo_password,
        kobo_uid,
        email
    )
    submissions = [
        submission for submission in overall_submissions
        if submission['instance'] in instances
    ]

    kobo_client = KoboClient(kobo_username, kobo_password)
    inaturalist_client = iNaturalistClient(
        inat_username, inat_password, inat_client_id,
        inat_client_secret, api_url=inat_api,
        app_url=inat_webapp
    )

    for record in submissions:
        #if not record['is_valid']: continue

        # start by downloading the images
        image_paths = []
        instance = record['instance']
        for image in record['images']:
            image_path = f'{kobo_uid}_{instance}_{image}'
            kobo_client.pull_image(
                image_path, kobo_uid, instance, image
            )
            image_paths.append(image_path)
        
        # upload the base observation
        observation_id = inaturalist_client.upload_base_observation(
            record['taxa'], 
            record['longitude'], 
            record['latitude'], 
            record['ts'], 
            record['positional_accuracy'], 
            record['notes']
        )

        # attach the images
        for image_path in image_paths:
            inaturalist_client.attach_image(
                observation_id, image_path
            )
            os.remove(image_path)

        # attach the observation field values
        for field_id, value in record['observation_fields'].items():
            inaturalist_client.attach_observation_field(
                observation_id, int(field_id), value
            )

if __name__ == '__main__':
    main()
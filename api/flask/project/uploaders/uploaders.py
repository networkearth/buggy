"""
Code for uploading to iNaturalist and keeping a backup
"""

import os
import json
import boto3
import requests

from gluon.inaturalist import client as inaturalist_client
from gluon.kobo import client as kobo_client

def get_clients(
    kobo_username, kobo_password, inat_username,
    inat_password, inat_client_id, inat_client_secret,
    inat_api, inat_webapp
):
    """
    Builds the kobo and iNaturalist clients
    """
    kobo = kobo_client.KoboClient(kobo_username, kobo_password)
    inaturalist = inaturalist_client.iNaturalistClient(
        inat_username, inat_password, inat_client_id,
        inat_client_secret, api_url=inat_api,
        app_url=inat_webapp
    )
    return kobo, inaturalist

def pull_images(kobo, kobo_uid, record):
    """
    Pulls the image data for a specific submission
    and stores it to disc
    """
    image_paths = []
    instance = record['instance']
    for image in record['images']:
        image_path = f'{kobo_uid}_{instance}_{image}'
        kobo.pull_image(
            image_path, kobo_uid, instance, image
        )
        image_paths.append(image_path)
    return image_paths

# pylint: disable=invalid-name
def backup_record(kobo, kobo_uid, record, image_paths, backup_path):
    """
    Backs up the kobo record to s3
    """
    instance = record['instance']
    kobo_record = kobo.pull_instance(kobo_uid, instance)
    folder = ''
    for component in [backup_path, str(kobo_uid)]:
        folder = (folder + '/' + component) if folder else component
        if not os.path.exists(folder):
            os.mkdir(folder)

    
    with open('/'.join([folder, str(instance) + '.json']), 'w') as fh:
        json.dump(kobo_record, fh, indent=4, sort_keys=True)

    for image_path in image_paths:
        with open(image_path, 'rb') as rh:
            with open('/'.join([folder, str(instance) + '_' + image_path.split('_')[-1] + '.jpg']), 'wb') as wh:
                wh.write(rh.read())

def upload_to_inat(inaturalist, record, image_paths):
    """
    Runs the upload to iNaturalist
    """
    observation_id = inaturalist.upload_base_observation(
        record['taxa'],
        record['longitude'],
        record['latitude'],
        record['ts'],
        record['positional_accuracy'],
        record['notes']
    )

    # attach the images
    for image_path in image_paths:
        inaturalist.attach_image(
            observation_id, image_path
        )

    # attach the observation field values
    for field_id, value in record['observation_fields'].items():
        inaturalist.attach_observation_field(
            observation_id, int(field_id), value
        )


def upload_submissions(
    submissions, backup_path,
    kobo_username, kobo_password, kobo_uid,
    inat_username, inat_password, inat_client_id, 
    inat_client_secret, inat_api, inat_webapp
):
    kobo, inaturalist = get_clients(
        kobo_username, kobo_password, inat_username,
        inat_password, inat_client_id, inat_client_secret,
        inat_api, inat_webapp
    )

    for record in submissions:
        #if not record['is_valid']: continue

        # start by downloading the images
        image_paths = pull_images(
            kobo, kobo_uid, record
        )

        # backup the record
        backup_record(
            kobo, kobo_uid, record,
            image_paths, backup_path
        )

        # upload the record
        upload_to_inat(
            inaturalist, record, image_paths
        )

        # delete the record
        kobo.delete_instance(kobo_uid, record['instance'])

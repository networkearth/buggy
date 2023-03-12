"""
Tests for functions used in batch job
"""

import os
import json
import shutil

from project.uploaders.uploaders import (
    get_clients,
    pull_images,
    backup_record,
    upload_to_inat
)


class MockKoboClient():
    """
    Standin for the kobo client
    """
    def __init__(self, kobo_username, kobo_password):
        self.kobo_username = kobo_username
        self.kobo_password = kobo_password

    def __call__(self, kobo_username, kobo_password):
        """
        Called on instantiation within the code
        Checks creds are as expected
        """
        assert self.kobo_username == kobo_username
        assert self.kobo_password == kobo_password
        return self

class MockiNaturalistClient():
    """
    Standin for the iNaturalist client
    """
    def __init__(
        self, inat_username, inat_password, inat_client_id,
        inat_client_secret, api_url, app_url
    ):
        self.inat_username = inat_username
        self.inat_password = inat_password
        self.inat_client_id = inat_client_id
        self.inat_client_secret = inat_client_secret
        self.api_url = api_url
        self.app_url = app_url

    def __call__(
        self, inat_username, inat_password, inat_client_id,
        inat_client_secret, api_url, app_url
    ):
        """
        Called on instantiation within the code
        Checks creds are as expected
        """
        assert self.inat_username == inat_username
        assert self.inat_password == inat_password
        assert self.inat_client_id == inat_client_id
        assert self.inat_client_secret == inat_client_secret
        assert self.api_url == api_url
        assert self.app_url == app_url
        return self

def test_get_clients(mocker):
    """
    Test for the get_clients function
    """
    kobo_username = 'beetlebub'
    kobo_password = 'chitinisking'
    kobo = MockKoboClient(kobo_username, kobo_password)

    inat_username = 'dragon@bug.org'
    inat_password = 'sixlegsisbest'
    inat_client_id = 'iamanappid'
    inat_client_secret = 'iamanappsecret'
    api_url = 'https://api.fakeinaturalist.org/v1'
    app_url = 'https://www.fakeinaturalist.org'
    inaturalist = MockiNaturalistClient(
        inat_username, inat_password, inat_client_id,
        inat_client_secret, api_url, app_url
    )

    mocker.patch(
        'gluon.kobo.client.KoboClient', kobo
    )
    mocker.patch(
        'gluon.inaturalist.client.iNaturalistClient', inaturalist
    )

    r_kobo, r_inaturalist = get_clients(
        kobo_username, kobo_password, inat_username, inat_password,
        inat_client_id, inat_client_secret, api_url, app_url
    )

    assert r_kobo == kobo
    assert r_inaturalist == inaturalist

class MockImagePuller():
    """
    Standin for iNaturalist pull image
    """
    def __init__(self):
        self.image_store = {}

    def pull_image(self, image_path, kobo_uid, instance, image):
        """
        Stores what we asked for so we can
        check we asked for the right things
        """
        self.image_store[image_path] = {
            'kobo_uid': kobo_uid,
            'instance': instance,
            'image': image
        }

def test_pull_images():
    """
    Test for the pull images function
    """
    kobo_client = MockImagePuller()
    record = {
        'instance': 1,
        'images': [1, 4]
    }
    kobo_uid = 'iguessiamauid'
    image_paths = pull_images(kobo_client, kobo_uid, record)
    assert image_paths == [
        f'{kobo_uid}_1_1',
        f'{kobo_uid}_1_4'
    ]
    for path in image_paths:
        assert kobo_client.image_store[path] == {
            'kobo_uid': kobo_uid,
            'instance': 1,
            'image': int(path.split('_')[-1])
        }

class MockInstancePuller():
    """
    Standin for a kobo pull data
    """
    def __init__(self, kobo_uid, instance, instance_data):
        self.kobo_uid = kobo_uid
        self.instance = instance
        self.instance_data = instance_data

    def pull_instance(self, kobo_uid, instance):
        """
        Asserts we're requesting the pull
        in the correct fashion with the right data
        """
        assert self.kobo_uid == kobo_uid
        assert self.instance == instance
        return self.instance_data

def test_backup_record():
    """
    Test for the backup_record function
    """
    backup_path = 'tmp-backup-test'
    image_paths = ['test_image_1']
    for image_path in image_paths:
        with open(image_path, 'wb') as file:
            file.write(b'flowerpower')
    try:
        kobo_uid = 'iguessiamauid'
        record = {
            'instance': 1
        }
        instance_data = {'some': 'data'}
        kobo_client = MockInstancePuller(
            kobo_uid, record['instance'], instance_data
        )

        backup_record(
            kobo_client, kobo_uid, record, image_paths, backup_path
        )

        with open('tmp-backup-test/iguessiamauid/1.json', 'r') as fh:
            assert json.load(fh) == {'some': 'data'}
        with open('tmp-backup-test/iguessiamauid/1_1.jpg', 'rb') as fh:
            assert fh.read() == b'flowerpower'
        shutil.rmtree(backup_path)
        os.remove(image_path)
    except Exception as exception:
        for image_path in image_paths:
            os.remove(image_path)
        shutil.rmtree(backup_path)
        raise exception

class MockiNaturalistUploader():
    """
    Standing for the iNaturalist upload
    """
    def __init__(
        self, taxa, longitude, latitude, timestamp,
        positional_accuracy, notes, observation_id
    ):
        self.taxa = taxa
        self.longitude = longitude
        self.latitude = latitude
        self.timestamp = timestamp
        self.positional_accuracy = positional_accuracy
        self.notes = notes

        self.observation_id = observation_id

        self.image_calls = []
        self.field_calls = []

    def upload_base_observation(
        self, taxa, longitude, latitude, timestamp,
        positional_accuracy, notes
    ):
        """
        Checks data is passed correctly
        """
        assert self.taxa == taxa
        assert self.longitude == longitude
        assert self.latitude == latitude
        assert self.timestamp == timestamp
        assert self.positional_accuracy == positional_accuracy
        assert self.notes == notes
        return self.observation_id

    def attach_image(self, *args):
        """
        Captures the calls to upload images
        so we can check them later
        """
        self.image_calls.append(args)

    def attach_observation_field(self, *args):
        """
        Captures the calls to upload fields
        so we can check them later
        """
        self.field_calls.append(args)


def test_upload_to_inat():
    """
    Test for the upload_to_inat function
    """
    observation_id = 2
    record = {
        'taxa': 123847,
        'longitude': 44,
        'latitude': 54.2,
        'ts': '2022-02-02',
        'positional_accuracy': 5,
        'notes': 'hello there',
        'instance': 1,
        'observation_fields': {
            '12345': 'general kenobi'
        }
    }
    inaturalist_client = MockiNaturalistUploader(
        record['taxa'], record['longitude'], record['latitude'],
        record['ts'], record['positional_accuracy'], record['notes'],
        observation_id
    )

    image_paths = ['test_image_1']

    upload_to_inat(inaturalist_client, record, image_paths)

    expected_image_calls = [
        (observation_id, 'test_image_1')
    ]
    assert inaturalist_client.image_calls == expected_image_calls

    expected_field_calls = [
        (observation_id, 12345, 'general kenobi')
    ]
    assert inaturalist_client.field_calls == expected_field_calls

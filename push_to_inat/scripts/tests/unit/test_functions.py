"""
Tests for functions used in batch job
"""

import io
import os
import json
import httpretty

from main import (
    get_job_data,
    get_submissions,
    get_clients,
    pull_images,
    backup_record,
    upload_to_inat
)

class MockBotoS3Resource():
    """
    Standin for S3 Resource
    """
    def __init__(self, bucket, mock_bucket):
        self.bucket = bucket
        self.mock_bucket = mock_bucket

    # pylint: disable=invalid-name
    def Bucket(self, bucket):
        """
        Standin for grabbing a bucket
        Checks the bucket name is as expected
        """
        assert self.bucket == bucket
        return self.mock_bucket

class MockBucket():
    """
    Standin for a bucket
    """
    def __init__(self, email, objects):
        self.objects = self
        self.email = email
        self._objects = objects

    # pylint: disable=invalid-name
    def filter(self, Prefix):
        """
        Standin for the filter
        Checks our filter matches
        the input email
        """
        assert self.email == Prefix
        return self._objects

class MockObject():
    """
    Standin for an s3 object
    """
    def __init__(self, content):
        self.content = content

    def get(self):
        """
        Returns a bytes io object with
        the content we specified
        """
        return {'Body': io.BytesIO(self.content.encode('utf-8'))}


def test_get_job_data():
    """
    Test for the get_job_data function
    """
    email = 'dragon@bug.org'
    bucket = 'job-bucket'
    data1 = {
        'kobo_username': 'beetlebub', 'kobo_password': 'chitinisking',
        'kobo_uid': 'iguessiamauid', 'inaturalist_email': email,
        'inaturalist_password': 'sixlegsisbest', 'client_id': 'iamanappid',
        'client_secret': 'iamanappsecret', 'instances': [1, 2]
    }
    data2 = {
        'kobo_username': 'beetlebub', 'kobo_password': 'chitinisking',
        'kobo_uid': 'iguessiamauid', 'inaturalist_email': email,
        'inaturalist_password': 'sixlegsisbest', 'client_id': 'iamanappid',
        'client_secret': 'iamanappsecret', 'instances': [2, 4]
    }
    objects = [
        MockObject(json.dumps(data1)),
        MockObject(json.dumps(data2))
    ]
    # pylint: disable=invalid-name
    s3 = MockBotoS3Resource(
        bucket, MockBucket(
            email, objects
        )
    )
    (
        kobo_username, kobo_password, kobo_uid, inat_username, inat_password,
        inat_client_id, inat_client_secret, instances, objects_to_delete
    ) = get_job_data(email, s3, bucket)

    assert kobo_username == 'beetlebub'
    assert kobo_password == 'chitinisking'
    assert kobo_uid == 'iguessiamauid'
    assert inat_username == 'dragon@bug.org'
    assert inat_password == 'sixlegsisbest'
    assert inat_client_id == 'iamanappid'
    assert inat_client_secret == 'iamanappsecret'
    assert instances == set([1, 2, 4])
    assert objects_to_delete == objects

@httpretty.activate
def test_get_submissions():
    """
    Test for the get_submissions function
    """
    httpretty.register_uri(
        httpretty.GET, 'http://localhost:5002/submissions',
        body=json.dumps([
            {'instance': 1, 'some': 'data'},
            {'instance': 2, 'some': 'other data'},
            {'instance': 3, 'some': 'additional data'}
        ])
    )

    submissions = get_submissions(
        'http://localhost:5002', 'beetlebub', 'chitinisking',
        'iguessiamauid', 'dragon@bug.org', set([1, 2, 4])
    )

    assert submissions == [
        {'instance': 1, 'some': 'data'},
        {'instance': 2, 'some': 'other data'},
    ]
    assert json.loads(httpretty.last_request().body.decode('utf-8')) == {
        'kobo_username': 'beetlebub', 'kobo_password': 'chitinisking',
        'kobo_uid': 'iguessiamauid', 'email': 'dragon@bug.org'
    }

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

class MockBotoS3Client():
    """
    Standin for the s3 client
    """
    def __init__(self):
        self.puts = []

    # pylint: disable=invalid-name
    def put_object(self, Body, Bucket, Key):
        """
        Captures the puts we requested
        so we can check them later
        """
        self.puts.append(
            {
                'body': Body,
                'bucket': Bucket,
                'key': Key
            }
        )

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

        # pylint: disable=invalid-name
        s3 = MockBotoS3Client()
        backup_bucket = 'backup-bucket'

        backup_record(
            kobo_client, kobo_uid, record, image_paths, s3, backup_bucket
        )
    except Exception as exception:
        for image_path in image_paths:
            os.remove(image_path)
        raise exception

    expected_puts = [
        {
            'body': json.dumps(instance_data, indent=4, sort_keys=True),
            'bucket': 'backup-bucket',
            'key': '/'.join([kobo_uid, str(record['instance']) + '.json'])
        },
        {
            'body': b'flowerpower',
            'bucket': 'backup-bucket',
            'key': '/'.join([kobo_uid, str(record['instance']), '1.jpg'])
        }
    ]
    assert s3.puts == expected_puts

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

"""
Tests for the /job endpoint
"""

import json

class MockBotoSwitch():
    """
    Standin for the boto3.client
    """
    def __call__(self, service):
        """
        Called when the code grabs a client
        Returns the appropriate service
        """
        return self.services[service]

    def __init__(self, services):
        self.services = services

class MockBotoS3Client():
    """
    Standin for the S3 client
    """
    def __init__(self, body, bucket, email):
        self.body = body
        self.bucket = bucket
        self.email = email

    # pylint: disable=invalid-name
    def put_object(self, Body, Bucket, Key):
        """
        Standin for a put, checks the data
        passed
        """
        assert self.body == Body
        assert self.bucket == Bucket
        assert Key.endswith('.json')
        email, _time = '.'.join(Key.split('.')[:-1]).split('-')
        assert email == self.email
        # check this cast works
        int(_time)

class MockBotoBatchClient():
    """
    Standin for the batch client
    """
    def __init__(
        self, region, account, job_queue, job_definition,
        job_name, command
    ):
        self.region = region
        self.account = account
        self.job_queue = job_queue
        self.job_definition = job_definition
        self.job_name = job_name
        self.command = command

    # pylint: disable=invalid-name
    def submit_job(
        self, jobQueue, jobName, jobDefinition, containerOverrides
    ):
        """
        Standin for submitting a job,
        checks all the data passed
        """
        assert (
            jobQueue ==
            f'arn:aws:batch:{self.region}:{self.account}:job-queue/{self.job_queue}'
        )
        assert jobName == self.job_name
        assert (
            jobDefinition ==
            f'arn:aws:batch:{self.region}:{self.account}:job-definition/{self.job_definition}'
        )
        assert containerOverrides['command'] == self.command
        assert set(containerOverrides.keys()) == set(['command'])

def test_normal_post(client, mocker):
    """
    Check POST under normal conditions
    """
    email = 'beetle@bug.org'
    payload = {
        'kobo_username': 'beetlebub',
        'kobo_password': 'chitinisking',
        'kobo_uid': 'iguessiamauid',
        'inaturalist_email': email,
        'inaturalist_password': 'sixlegsdabest',
        'client_id': 'iamaclientid',
        'client_secret': 'iamasecret',
        'instances': '12,45,113'
    }
    # pylint: disable=unnecessary-comprehension
    data = {k:v for k, v in payload.items()}
    data['instances'] = [
        12, 45, 113
    ]
    data = json.dumps(data, indent=4, sort_keys=True)

    mocker.patch(
        'project.submissions.submissions.get_submissions',
        return_value=[
            {'instance': 13}, {'instance': 12}, {'instance': 45}
        ]
    )

    mocked_upload = mocker.patch(
        'project.uploaders.uploaders.upload_submissions'
    )

    response = client.post('/job', json=payload)
    assert response.status_code == 201
    mocked_upload.assert_called_once_with(
        [{'instance': 12}, {'instance': 45}], 
        'my-backup-path', 'beetlebub', 'chitinisking', 'iguessiamauid', 
        'beetle@bug.org', 'sixlegsdabest', 'iamaclientid', 'iamasecret', 
        'http://api', 'http://webapp'
    )

def test_bad_inputs_post(client):
    """
    Check POST under incorrect inputs
    """
    payload = {
        'kobo_username': 'beetlebub',
        'kobo_password': 'chitinisking',
        'kobo_uid': 'iguessiamauid',
        # missing email
        'inaturalist_password': 'sixlegsdabest',
        'client_id': 'iamaclientid',
        'client_secret': 'iamasecret',
        'instances': '12,45,113'
    }
    response = client.post('/job', json=payload)
    assert response.status_code == 400

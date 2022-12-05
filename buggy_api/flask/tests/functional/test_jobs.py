import json

class MockBotoSwitch(object):
    def __call__(self, service):
        return self.services[service]

    def __init__(self, services):
        self.services = services

class MockBotoS3Client(object):
    def __init__(self, body, bucket, email):
        self.body = body
        self.bucket = bucket
        self.email = email

    def put_object(self, Body, Bucket, Key):
        assert self.body == Body
        assert self.bucket == Bucket
        assert Key.endswith('.json')
        print(Key)
        email, _time = '.'.join(Key.split('.')[:-1]).split('-')
        assert email == self.email
        # check this cast works
        int(_time)

class MockBotoBatchClient(object):
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

    def submit_job(
        self, jobQueue, jobName, jobDefinition, containerOverrides
    ):
        assert jobQueue == f'arn:aws:batch:{self.region}:{self.account}:job-queue/{self.job_queue}'
        assert jobName == self.job_name
        assert jobDefinition == f'arn:aws:batch:{self.region}:{self.account}:job-definition/{self.job_definition}'
        assert containerOverrides['command'] == self.command
        assert set(containerOverrides.keys()) == set(['command'])

def test_normal_post(client, mocker):
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
    data = {k:v for k, v in payload.items()}
    data['instances'] = [
        12, 45, 113
    ]
    data = json.dumps(data, indent=4, sort_keys=True)
    bucket = 'buggy-test-job'

    switch = MockBotoSwitch(
        {
            's3': MockBotoS3Client(
                data, bucket, email
            ),
            'batch': MockBotoBatchClient(
                'us-east-1', '575101084097', 'buggy-test-push-to-inat',
                'buggy-test-push-to-inat', 'pushtoinat',
                [
                    '-e',
                    email,
                    '-b',
                    bucket,
                    '-bb',
                    'buggy-test-backup',
                    '-ia',
                    'https://api.fakeinaturalist.org/v1',
                    '-iw',
                    'https://www.fakeinaturalist.org'
                ]
            )
        }
    )

    mocker.patch(
        "boto3.client", 
        switch
    )

    response = client.post('/job', json=payload)
    assert response.status_code == 201

def test_bad_inputs_post(client):
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

class MockKoboClient(object):
    def __init__(self, username, password, uid):
        self.expected_username = username
        self.expected_password = password
        self.expected_uid = uid

    def __call__(self, username, password):
        assert username == self.expected_username
        assert password == self.expected_password

        return self
        
    def pull_data(self, uid):
        assert uid == self.expected_uid

        return [
            {'Bug': 'Beetle', 'Email': 'dragonfly@bug.org'},
            {'Bug': 'Dragonfly', 'Email': 'beetle@bug.org'},
            {'Bug': 'Fruitfly', 'Email': 'beetle@bug.org'},
            # this is here to make sure we can deal with
            # exceptions when the transformers are run
            {'Email': 'beetle@bug.org'}
        ]

MockTransformers = [
    lambda entry: ('bug', entry['Bug']),
    lambda entry: ('email', entry['Email'])
]

def test_normal_get(client, mocker):
    payload = {
        'kobo_username': 'beetlebub',
        'kobo_password': 'chitinisking',
        'kobo_uid': 'iguessthisisauid',
        'email': 'beetle@bug.org'
    }

    mocker.patch(
        'gluon.kobo.client.KoboClient', 
        MockKoboClient(
            payload['kobo_username'],
            payload['kobo_password'],
            payload['kobo_uid']
        )
    )

    mocker.patch(
        'project.transformers.transformers.BUGGY_TRANSFORMERS',
        MockTransformers
    )

    response = client.get('/submissions', json=payload)
    assert response.json == [{'bug': 'Dragonfly', 'email': 'beetle@bug.org'}, {'bug': 'Fruitfly', 'email': 'beetle@bug.org'}]
    assert response.status_code == 200

def test_kobo_fails(client, mocker):
    # we start by checking if kobo is fine this request will be fine
    payload = {
        'kobo_username': 'beetlebub',
        'kobo_password': 'chitinisking',
        'kobo_uid': 'iguessthisisauid',
        'email': 'beetle@bug.org'
    }

    mocker.patch(
        'gluon.kobo.client.KoboClient', 
        MockKoboClient(
            payload['kobo_username'],
            payload['kobo_password'],
            payload['kobo_uid']
        )
    )

    mocker.patch(
        'project.transformers.transformers.BUGGY_TRANSFORMERS',
        MockTransformers
    )

    response = client.get('/submissions', json=payload)

    assert response.status_code == 200

    def raise_exception(*args):
        raise Exception()

    # now we mess up kobo
    mocker.patch(
        'gluon.kobo.client.KoboClient', 
        raise_exception
    )

    response = client.get('/submissions', json=payload)

    assert response.status_code == 500

def test_bad_args(client):
    payload = {
        'kobo_username': 'beetlebub',
        'kobo_password': 'chitinisking',
        'kobo_uid': 'iguessthisisauid',
        # email is missing
    }

    response = client.get('/submissions', json=payload)

    assert response.status_code == 400

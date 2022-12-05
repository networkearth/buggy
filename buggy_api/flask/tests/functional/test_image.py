class MockKoboClient(object):
    def __init__(self, username, password, uid, instance, id):
        self.expected_username = username
        self.expected_password = password
        self.expected_uid = uid
        self.expected_instance = instance
        self.expected_id = id

    def __call__(self, username, password):
        assert username == self.expected_username
        assert password == self.expected_password

        return self

    def pull_image_bytes(self, uid, instance, id):
        assert uid == self.expected_uid
        assert instance == self.expected_instance
        assert id == self.expected_id

        return b'flowerpower'

def test_normal_get(client, mocker):
    payload = {
        'kobo_username': 'beetlebub',
        'kobo_password': 'chitinisking',
        'kobo_uid': 'iguessthisisauid',
        'instance': 12,
        'id': 453
    }

    mocker.patch(
        'gluon.kobo.client.KoboClient',
        MockKoboClient(
            payload['kobo_username'],
            payload['kobo_password'],
            payload['kobo_uid'],
            payload['instance'],
            payload['id']
        )
    )

    response = client.get('/image', json=payload)
    assert response.status_code == 200
    assert response.headers[0] == ('Content-Type', 'image/jpeg')
    assert response.data == b'flowerpower'

def test_bad_args(client):
    payload = {
        'kobo_username': 'beetlebub',
        'kobo_password': 'chitinisking',
        'kobo_uid': 'iguessthisisauid',
        'instance': 12,
        # id is missing
    }
    response = client.get('/image', json=payload)
    assert response.status_code == 400

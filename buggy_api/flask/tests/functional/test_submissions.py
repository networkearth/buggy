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

        return []

def test_get_submissions(client, mocker):
    payload = {
        'kobo_username': 'beetle@bugs.org',
        'kobo_password': 'chitinisking',
        'kobo_uid': 'iguessthisisauid',
        'email': 'hopper@bugs.org'
    }

    mocker.patch(
        'gluon.kobo.client.KoboClient', 
        MockKoboClient(
            payload['kobo_username'],
            payload['kobo_password'],
            payload['kobo_uid']
        )
    )

    print(client.get('/submissions', json=payload))
    assert False
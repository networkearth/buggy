import pytest
import json

from project import create_app

TEST_SECRETS = {
    'buggy-test-inaturalist': {
        'api': 'https://api.fakeinaturalist.org/v1',
        'webapp': 'https://www.fakeinaturalist.org'
    }
}

class MockSecretsManagerClient(object):
    @staticmethod
    def get_secret_value(SecretId):
        return {
            'SecretString': json.dumps(TEST_SECRETS[SecretId])
        }

MOCK_CLIENTS = {
    'secretsmanager': MockSecretsManagerClient
}

class MockBotoSession(object):
    @staticmethod
    def client(service_name, region_name=None):
        if service_name == 'secretsmanager':
            assert region_name is not None

        return MOCK_CLIENTS[service_name]()

@pytest.fixture()
def app(mocker):
    mocker.patch('boto3.session.Session', MockBotoSession)

    app = create_app('test', 'buggy', '575101084097', 'us-east-1', 'http://localhost:5002')

    # setup here
    
    yield app

@pytest.fixture()
def client(app):
    return app.test_client()

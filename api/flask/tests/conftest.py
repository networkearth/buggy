"""
Global Configuration for the API tests
"""

import json
import pytest

from project import create_app

TEST_SECRETS = {
    'buggy-test-inaturalist': {
        'api': 'https://api.fakeinaturalist.org/v1',
        'webapp': 'https://www.fakeinaturalist.org'
    }
}

class MockSecretsManagerClient():
    """
    Standin for the secrets manager client
    """

    @staticmethod
    # pylint: disable=invalid-name
    def get_secret_value(SecretId):
        """
        Returns the secret with the given SecretId
        """
        return {
            'SecretString': json.dumps(TEST_SECRETS[SecretId])
        }

MOCK_CLIENTS = {
    'secretsmanager': MockSecretsManagerClient
}

class MockBotoSession():
    """
    Standin for the boto session
    """

    @staticmethod
    def client(service_name, region_name=None):
        """
        Returns the appropriate client given the service
        name and region
        """
        if service_name == 'secretsmanager':
            assert region_name is not None

        return MOCK_CLIENTS[service_name]()

@pytest.fixture()
def app(mocker):
    """
    Builds a testing version of the app
    """
    mocker.patch('boto3.session.Session', MockBotoSession)

    application = create_app('test', 'buggy', '575101084097', 'us-east-1')

    # setup here

    yield application

@pytest.fixture()
# pylint: disable=redefined-outer-name
def client(app):
    """
    Gets the test client of the app
    """
    return app.test_client()

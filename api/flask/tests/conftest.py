"""
Global Configuration for the API tests
"""

import pytest

from project import create_app

@pytest.fixture()
def app(mocker):
    """
    Builds a testing version of the app
    """

    application = create_app('http://api', 'http://webapp', 'my-backup-path')

    # setup here

    yield application

@pytest.fixture()
# pylint: disable=redefined-outer-name
def client(app):
    """
    Gets the test client of the app
    """
    return app.test_client()

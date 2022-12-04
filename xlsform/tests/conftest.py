import pytest
import json

@pytest.fixture()
def choices():
    with open('xlsform/choices.json', 'r') as fh:
        return json.load(fh)

@pytest.fixture()
def settings():
    with open('xlsform/settings.json', 'r') as fh:
        return json.load(fh)

@pytest.fixture()
def survey():
    with open('xlsform/survey.json', 'r') as fh:
        return json.load(fh)
    
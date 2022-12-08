"""
Global Configuration for XLSForm Tests
"""

import json
import pytest

@pytest.fixture()
def choices():
    """
    Loads the choices json as a dict
    """
    with open('xlsform/choices.json', 'r', encoding="utf8") as file:
        return json.load(file)

@pytest.fixture()
def settings():
    """
    Loads the settings json as a dict
    """
    with open('xlsform/settings.json', 'r', encoding="utf8") as file:
        return json.load(file)

@pytest.fixture()
def survey():
    """
    Loads the survey json as a dict
    """
    with open('xlsform/survey.json', 'r', encoding="utf8") as file:
        return json.load(file)
   
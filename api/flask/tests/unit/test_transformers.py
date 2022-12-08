"""
Tests the transformers
"""

import unittest
from functools import partial
import json
import httpretty

from project.transformers.transformers import (
    notes_transform,
    mapping_transform,
    convert_key_transform,
    observation_field_transformer,
    image_transformer
)

def register_token_url():
    """
    Register the url used for grabbing tokens from kobo
    """
    httpretty.register_uri(
        httpretty.GET, "https://kf.kobotoolbox.org/token?format=json",
        body=json.dumps({"token": "what are you token about?"})
    )

class TestMappingTransform(unittest.TestCase):
    """
    Tests for the mapping transform
    """
    def setUp(self):
        """
        Setup a transformer
        """
        entry_key = "survey_field"
        output_key = "output_field"
        mapping = {
            "good_value": "good",
        }
        default = "missing"
        self.transformer = partial(
            mapping_transform, entry_key,
            output_key, mapping, default
        )

    def test_entry_key_present(self):
        """
        Tests case where the entry key is present
        """
        assert self.transformer({"survey_field": "good_value"}) == ("output_field", "good")

    def test_entry_key_missing(self):
        """
        Tests case where the entry key is not present
        """
        assert self.transformer({}) == ("output_field", "missing")

    def test_mapping_key_missing(self):
        """
        Tests case where the mapping key is not present
        """
        assert self.transformer({"survey_field": "bad_value"}) == ("output_field", "missing")

class TestConvertKeyTransform(unittest.TestCase):
    """
    Tests for the convert key transform
    """
    def setUp(self):
        """
        Setup a transformer
        """
        entry_key = "survey_field"
        output_key = "output_field"
        default = "missing"
        self.transformer = partial(
            convert_key_transform, entry_key,
            output_key, str, default
        )

    def test_entry_key_present(self):
        """
        Tests when then entry key is present
        """
        assert self.transformer({"survey_field": "good_value"}) == ("output_field", "good_value")

    def test_entry_key_missing(self):
        """
        Tests when then entry key is not present
        """
        assert self.transformer({}) == ("output_field", "missing")

class TestObservationFieldTransformer(unittest.TestCase):
    """
    Tests for the observation field transformer
    """
    def test_base_case(self):
        """
        Base case
        """
        observation_field_transformers = [
            partial(
                convert_key_transform,
                "survey_field",
                "output_field",
                str,
                None
            )
        ]
        entry = {
            "survey_field": "good_value"
        }
        result = observation_field_transformer(observation_field_transformers, entry)

        assert result == ('observation_fields', {"output_field": "good_value"})

    def test_kwargs_passed(self):
        """
        Tests kwargs are passed through the transformer
        correctly
        """
        # pylint: disable=unused-argument
        def transformer(entry: dict, **kwargs) -> tuple:
            return "field", kwargs["to_pass"]
        observation_field_transformers = [
            transformer
        ]
        entry = {
            "survey_field": "good_value"
        }
        result = observation_field_transformer(
            observation_field_transformers, entry, to_pass="check for me"
        )

        assert result == ('observation_fields', {"field": "check for me"})

class TestImageTransformer(unittest.TestCase):
    """
    Tests for the image transformer
    """
    def test_base_case(self):
        """
        Base case
        """
        entry = {
            "photo1": "bug.png",
            "photo3": "plant.png",
            "_attachments": [
                {
                    "filename": "a/long/url/bug.png",
                    "instance": 1,
                    "id": 2
                },
                {
                    "filename": "a/long/url/plant.png",
                    "instance": 3,
                    "id": 4
                },
                {
                    "filename": "a/long/url/other.txt",
                    "instance": 5,
                    "id": 6
                }
            ]
        }
        result = image_transformer(["photo3", "photo2", "photo1"], entry)
        expected = [
            4, 2
        ]
        assert result[0] == "images"
        assert result[1] == expected


NOTE = """
The Thing They Forgot:
I had a great time. :)

My Notes:
Hello there!
""".strip()
class TestNotesTransform(unittest.TestCase):
    """
    Tests for the notes transformer
    """
    def test_base_case(self):
        """
        Base case
        """
        entry = {
            "my note": "Hello there!",
            "postscript": "I had a great time. :)"
        }
        transformer = partial(
            notes_transform,
            {
                "my note": "My Notes:",
                "postscript": "The Thing They Forgot:",
                "other stuff": "Other:"
            },
            [
                "postscript",
                "other stuff",
                "my note"
            ]
        )
        key, transformed = transformer(entry)
        print(NOTE)
        print(transformed)
        assert key == "notes"
        assert transformed == NOTE

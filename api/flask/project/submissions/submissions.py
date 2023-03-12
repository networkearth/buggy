"""
Submissions retrieval logic
"""

from gluon.kobo import client
from ..transformers import transformers

def get_submissions(**kwargs):
    kobo = client.KoboClient(kwargs['kobo_username'], kwargs['kobo_password'])
    email = kwargs['inaturalist_email'].strip()
    data = kobo.pull_data(kwargs['kobo_uid'])
    transformed_data = []
    failed = 0
    for entry in data:
        try:
            transformed = {}
            for transformer in transformers.BUGGY_TRANSFORMERS:
                key, value = transformer(entry)
                transformed[key] = value
            transformed_data.append(transformed)
        # pylint: disable=broad-except
        except Exception:
            failed += 1
    transformed_data = list(filter(lambda x: x['email'] == email, transformed_data))
    return list(filter(lambda x: x['email'] == email, transformed_data))
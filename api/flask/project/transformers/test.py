from gluon.kobo.client import KoboClient
from getpass import getpass
import transformers
import traceback
import json


client = KoboClient('mgietzmann', getpass())
data = client.pull_data('aQ8wN2wgWtJzZphAkYD7eP')

email = 'claire.oneill@earthwiseaware.org'

print(json.dumps(data, indent=4, sort_keys=True))

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
    except Exception as e:
        print(traceback.format_exc())
        failed += 1
transformed_data = list(filter(lambda x: x['email'] == email, transformed_data))
print(transformed_data, len(transformed_data))
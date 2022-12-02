from flask_restful import Resource, reqparse
from gluon.kobo import client

from ..transformers.transformers import BUGGY_TRANSFORMERS

class Submissions(Resource):
    get_parser = reqparse.RequestParser()
    get_parser.add_argument(
        'kobo_username',
        type=str,
        required=True,
        help='Kobo username'
    )
    get_parser.add_argument(
        'kobo_password',
        type=str,
        required=True,
        help='Kobo password'
    )
    get_parser.add_argument(
        'kobo_uid',
        type=str,
        required=True,
        help='uid of Kobo project'
    )
    get_parser.add_argument(
        'email',
        type=str,
        required=True,
        help='email'
    )

    def get(self):
        kwargs = Submissions.get_parser.parse_args()
        kobo = client.KoboClient(kwargs['kobo_username'], kwargs['kobo_password'])
        email = kwargs['email'].strip()
        data = kobo.pull_data(kwargs['kobo_uid'])
        transformed_data = []
        failed = 0
        for entry in data:
            try:
                transformed = {}
                for transformer in BUGGY_TRANSFORMERS:
                    key, value = transformer(entry)
                    transformed[key] = value
                transformed_data.append(transformed)
            except Exception:
                failed += 1
        transformed_data = list(filter(lambda x: x['email'] == email, transformed_data))
        return list(filter(lambda x: x['email'] == email, transformed_data)), 200

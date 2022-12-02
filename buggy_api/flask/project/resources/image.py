from flask import make_response
from flask_restful import Resource, reqparse
from gluon.kobo.client import KoboClient

class Image(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'kobo_username',
        type=str,
        required=True,
        help='Kobo username'
    )
    parser.add_argument(
        'kobo_password',
        type=str,
        required=True,
        help='Kobo password'
    )
    parser.add_argument(
        'kobo_uid',
        type=str,
        required=True,
        help='uid of Kobo project'
    )
    parser.add_argument(
        'instance',
        type=int,
        required=True,
        help='instance id'
    )
    parser.add_argument(
        'id',
        type=int,
        required=True,
        help='image id'
    )

    def get(self):
        kwargs = Image.parser.parse_args()
        client = KoboClient(kwargs['kobo_username'], kwargs['kobo_password'])
        image_content = client.pull_image_bytes(
            kwargs['kobo_uid'], kwargs['instance'], kwargs['id']
        )
        response = make_response(image_content)
        response.headers.set('Content-Type', 'image/jpeg')
        return response
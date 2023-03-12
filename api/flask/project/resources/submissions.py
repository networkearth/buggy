"""
/submissions endpoint
"""

from flask_restful import Resource, reqparse

from ..submissions import submissions

class Submissions(Resource):
    """
    /submissions endpoint
    """
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
        'inaturalist_email',
        type=str,
        required=True,
        help='inaturalist email'
    )

    def get(self):
        """
        GET /submissions
        """
        kwargs = Submissions.get_parser.parse_args()
        data = submissions.get_submissions(**kwargs)
        return data, 200

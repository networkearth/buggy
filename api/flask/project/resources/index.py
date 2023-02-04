"""
/ endpoint
"""

from flask_restful import Resource

class Index(Resource):
    """
    / endpoint
    """
    def get(self):
        """
        GET /
        """
        return {"message": "Try /job /image or /submissions"}, 200

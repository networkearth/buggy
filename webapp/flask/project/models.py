"""
User model for flask_login
"""

from flask_login import UserMixin

# pylint: disable=redefined-builtin,invalid-name
class User(UserMixin):
    """
    User model for flask_login
    """

    def __init__(self, id):
        """
        Takes an id that should be email and password
        separated by a space
        """
        self.email, self.password = id.split(' ')
        self.id = id

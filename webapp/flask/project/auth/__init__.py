"""
auth blueprint
"""

from flask import Blueprint

auth = Blueprint('auth', __name__)

# pylint: disable=cyclic-import,wrong-import-position
from . import views

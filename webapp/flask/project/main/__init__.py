"""
main blueprint
"""

from flask import Blueprint

main = Blueprint('main', __name__)

# pylint: disable=cyclic-import,wrong-import-position
from . import views

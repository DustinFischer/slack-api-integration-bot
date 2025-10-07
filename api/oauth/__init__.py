from flask import Blueprint

oauth_api = Blueprint("oauth", __name__, url_prefix='/oauth')

from . import oauth  # noqa

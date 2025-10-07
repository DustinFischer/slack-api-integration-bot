from flask import Blueprint

events_api = Blueprint("events", __name__, url_prefix='/events')

from . import events  # noqa

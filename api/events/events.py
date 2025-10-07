from flask import request, current_app

import slack
from api.events import events_api


@events_api.route('/', methods=['POST'])
def events_handler():
    with current_app.app_context():
        return slack.handler.handle(request)

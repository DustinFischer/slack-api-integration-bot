from .app_home_opened import app_home_opened

from slack_bolt.app import App


def register(app: App):
    app.event('app_home_opened')(app_home_opened)
from listeners import events, commands

from slack_bolt.app import App


def register_listeners(app: App):
    events.register(app)
    commands.register(app)

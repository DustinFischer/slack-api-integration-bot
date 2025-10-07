from logging import Logger

from slack_bolt.context.context import BoltContext

import slack
from composition.views.home.home import HomeNoAuthView, UserHomeView


def is_authenticated(**kwargs):
    # should check if authed against ADSS
    return slack.app.installation_store.find_installation(**kwargs)


# allowed args: https://slack.dev/bolt-python/api-docs/slack_bolt/kwargs_injection/args.html
def app_home_opened(client, event, context: BoltContext, logger: Logger):
    # ignore the app_home_opened event for anything but the Home tab
    if event['tab'] != 'home':
        return

    # handle auth logic
    if is_authenticated(team_id=context.team_id, user_id=context.user_id, enterprise_id=context.enterprise_id):
        view = UserHomeView(event)
    else:
        view = HomeNoAuthView(event)

    try:
        client.views_publish(
            user_id=event['user'],
            view=view.view
        )
    except Exception as e:
        logger.error(f'Error publishing home tab: {e}')

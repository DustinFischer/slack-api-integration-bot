from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler

from config import settings
from oauth.oauth import get_oauth_flow

app = App(
    # token=settings.SLACK_BOT_TOKEN,
    signing_secret=settings.SLACK_SIGNING_SECRET,
    raise_error_for_unhandled_request=True,
    # authorize=AuthorizeResult(...) if you want to dynamically select bot or user token
    oauth_flow=get_oauth_flow()
)

handler = SlackRequestHandler(app)

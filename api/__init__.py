from flask import Blueprint, url_for

slack_api = Blueprint("slack", __name__, url_prefix='/slack')

from api.events import events_api  # noqa
from api.oauth import oauth_api  # noqa

slack_api.register_blueprint(events_api)
slack_api.register_blueprint(oauth_api)


@slack_api.route('/install-link', methods=['GET'])
def slack_app_installation_link():
    def _build_default_install_page_html(url: str) -> str:
        return f"""<html>
    <head>
    <link rel="icon" href="data:,">
    <style>
    body {{
      padding: 10px 15px;
      font-family: verdana;
      text-align: center;
    }}
    </style>
    </head>
    <body>
    <h2>Slack App Installation</h2>
    <p><a href="{url}"><img alt=""Add to Slack"" height="40" width="139" src="https://platform.slack-edge.com/img/add_to_slack.png" srcset="https://platform.slack-edge.com/img/add_to_slack.png 1x, https://platform.slack-edge.com/img/add_to_slack@2x.png 2x" /></a></p>
    </body>
    </html>
    """  # noqa: E501
    return _build_default_install_page_html(url_for('slack.oauth.slack_app_install'))

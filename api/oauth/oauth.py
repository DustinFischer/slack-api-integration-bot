import base64

from flask import request, Response, url_for
from slack_bolt.adapter.flask.handler import to_flask_response, to_bolt_request
from slack_bolt.response import BoltResponse

import slack
from api.oauth import oauth_api
from config import settings


@oauth_api.route('/', methods=['GET'])
def slack_app_install():
    # 1. Check if ADSS jwt in request cookies? (Won't be in this case since we are in different domain)
    # 2. if not, redirect to ADSS OAuth
    if settings.ADSS_OAUTH_TOKEN_NAME not in request.cookies:
        # redirect to adss
        redirect = url_for(".slack_app_install", _external=True)
        url = f'{settings.ADSS_OAUTH_URL}?redir={base64.b64encode(redirect.encode()).decode()}'
        return to_flask_response(
            BoltResponse(
                status=307,
                body="",
                headers={
                    "Content-Type": "text/html; charset=utf-8", "Location": url,
                    # This step is a hack to mimic having a token available on domain after authenticating with ADSS
                    "Set-Cookie": f"{settings.ADSS_OAUTH_TOKEN_NAME}={settings.ADSS_OAUTH_TOKEN}; " "Secure; " "HttpOnly; " "Path=/; " f"Max-Age={10 * 60 * 60}"
                }
            )
        )

    # Otherwise continue with installation -> redirect to Slack OAuth
    bolt_resp = slack.app.oauth_flow.handle_installation(to_bolt_request(request))
    return to_flask_response(bolt_resp)


@oauth_api.route('/redirect', methods=['GET'])
def slack_oauth_redirect():
    if not ('code' in request.args and 'state' in request.args):
        return Response('Missing state / code', status=400)

    try:
        # create and store user installation
        return slack.handler.handle(request)
    except Exception:
        raise

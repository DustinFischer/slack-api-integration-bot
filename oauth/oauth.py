from slack_bolt.oauth import OAuthFlow
from slack_bolt.oauth.callback_options import CallbackOptions, SuccessArgs, FailureArgs
from slack_bolt.oauth.oauth_settings import OAuthSettings
from slack_bolt.response.response import BoltResponse

from config import settings
from oauth import log
from oauth.installation_store import get_installation_store


class OauthCallbackOptions(CallbackOptions):

    def __init__(self, *, etc=None):
        self.success = self._handle_success
        self.failure = self._handle_failure

    def _handle_success(self, args: SuccessArgs) -> BoltResponse:
        """
        Define behaviour after slack oauth redirect callback has been successful
        """
        installation = args.installation
        app_id = installation.app_id
        is_enterprise_install = installation.is_enterprise_install
        team_id = installation.team_id
        enterprise_url = installation.enterprise_url

        # Ripped from slack_bolt.oauth.internals.CallbackResponseBuilder
        if is_enterprise_install is True and enterprise_url is not None and app_id is not None:
            url = f"{enterprise_url}manage/organization/apps/profile/{app_id}/workspaces/add"
        elif team_id is None or app_id is None:
            url = "slack://open"
        else:
            url = f"slack://app?team={team_id}&id={app_id}"
        browser_url = f"https://app.slack.com/client/{team_id}"

        html = f"""
            <html>
            <head>
            <meta http-equiv="refresh" content="0; URL={url}">
            <style>
            body {{
              padding: 10px 15px;
              font-family: verdana;
              text-align: center;
            }}
            </style>
            </head>
            <body>
            <h2>Thank you!</h2>
            <p>Redirecting to the Slack App... click <a href="{url}">here</a>. If you use the browser version of Slack, click <a href="{browser_url}" target="_blank">this link</a> instead.</p>
            </body>
            </html>
            """  # noqa: E501

        return BoltResponse(
            status=200,
            headers={
                "Content-Type": "text/html; charset=utf-8",
                "Set-Cookie": f"{settings.API_OAUTH_TOKEN_NAME}=deleted; " "Secure; " "HttpOnly; " "Path=/; " "Expires=Thu, 01 Jan 1970 00:00:00 GMT",
            },
            body=html,
        )

    def _handle_failure(self, args: FailureArgs) -> BoltResponse:
        """
        Define behaviour after slack oauth redirect callback has failed
        """
        # TODO: delete oauth state cookie
        log.debug(f'[OauthCallbackOptions._handle_failure]: request.context {args.request.context.to_copyable()}')
        return BoltResponse(status=args.suggested_status_code, body=f"Installation failed! reason: {args.reason}")


def get_oauth_settings(*, install_render=False):
    return OAuthSettings(
        client_id=settings.SLACK_CLIENT_ID,
        client_secret=settings.SLACK_CLIENT_SECRET,
        callback_options=OauthCallbackOptions(),
        install_path=settings.SLACK_INSTALL_PATH,
        # url will be used to generate an auth url that redirects to slack oauth
        redirect_uri=settings.SLACK_OAUTH_REDIRECT_URI,
        redirect_uri_path=settings.SLACK_REDIRECT_PATH,
        # callback path passed to slack oauth on success/failure (would ultimately be called )
        scopes=settings.SLACK_OAUTH_SCOPES,  # minimum required bot user scopes (oauth will request access with scopes)
        user_scopes=settings.SLACK_OAUTH_USER_SCOPES,  # minimum required user scopes (for org installs)
        installation_store=get_installation_store(),
        state_validation_enabled=True,
        state_store=None,  # can customise this, default is to use FileOAuthStateStore
        state_cookie_name=settings.SLACK_OAUTH_STATE_COOKIE_NAME,
        logger=log,
        install_page_rendering_enabled=install_render
    )


def get_oauth_flow(oauth_settings: OAuthSettings = None):
    return OAuthFlow(
        client=None,  # instance of WebClient to use (one will be created by default)
        settings=oauth_settings or get_oauth_settings(),
        logger=log
    )

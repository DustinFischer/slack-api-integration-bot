# https://wilhelmklopp.com/posts/slack-database-modelling/
from slack_sdk.oauth.installation_store.file import FileInstallationStore

from config import settings


def get_installation_store():
    return FileInstallationStore(
        base_dir='./db/.installations',
        client_id=settings.SLACK_CLIENT_ID
    )

from logging import Logger

from slack_bolt import Ack, Respond
from slack_bolt.context.context import BoltContext
from slack_sdk.models.blocks import HeaderBlock, ContextBlock, ImageElement, MarkdownTextObject, SectionBlock, \
    DividerBlock

import api_client.models
from api_client.service import ADSSService
from composition.commands.adss import ADSSCommandResponse
from config import settings
from utils.static import static
from utils.util import block_id


def adss_slash_command_handler(ack: Ack, command, respond: Respond, logger: Logger):
    try:
        ack()

        # parse command args
        import re
        options = '|'.join(v.value for v in api_client.models.ObjectCategory)
        command_match = re.match(f'({options}) (.*)', command['text'])
        if not command_match:
            raise ValueError()
        obj_cat, name = command_match.groups()
        name = name.strip()
        object_cat = api_client.models.ObjectCategory(obj_cat)

        # Fetch for the modelled system... will need some way of figuring how the modelled system is retrieved
        preview = ADSSService().get_object_by_name_preview(settings.ADSS_MODEL, name, object_cat)

        # respond to slash command
        respond(blocks=ADSSCommandResponse().blocks(preview))
    except Exception as e:
        logger.error(e)

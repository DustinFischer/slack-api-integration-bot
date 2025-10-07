from typing import Sequence

from slack_sdk.models.blocks import Block
from slack_sdk.models.blocks import HeaderBlock, ContextBlock, ImageElement, MarkdownTextObject, SectionBlock, \
    DividerBlock

from api_client.models import ObjectPreview
from composition.commands import AbstractCommandResponse
from utils.static import static
from utils.util import block_id


class ADSSCommandResponse(AbstractCommandResponse):

    def blocks(self, preview: ObjectPreview) -> Sequence[dict | Block]:
        # Fetch for the modelled system... will need some way of figuring how the modelled system is retrieved

        return [
            HeaderBlock(
                block_id=block_id(),
                text=preview.objectName
            ),
            ContextBlock(
                block_id=block_id(),
                elements=[
                    ImageElement(image_url=static.url_for('icons/icon_object_off.png'), alt_text='icon_object'),
                    MarkdownTextObject(text=preview.category.value)
                ]
            ),
            SectionBlock(
                block_id=block_id(),
                text=MarkdownTextObject(text=preview.objectDescription.replace('**', '*'))
            ),
            DividerBlock(),
            ContextBlock(
                block_id=block_id(),
                elements=[
                    ImageElement(image_url=static.url_for('icons/icon_people_person.png'),
                                 alt_text='icon_people_person'),
                    MarkdownTextObject(text='*Owner*\t'),
                    MarkdownTextObject(text=preview.owner)
                ]
            ),
            DividerBlock(),
            ContextBlock(
                block_id=block_id(),
                elements=[
                    ImageElement(image_url=static.url_for('icons/icon_technologies_off.png'),
                                 alt_text='icon_technologies_off'),
                    MarkdownTextObject(text='*Technologies*\t'),
                    *([ImageElement(image_url=tech.imageLink, alt_text=tech.name) for tech in
                       preview.technologies] or [MarkdownTextObject(text='_no data_')])
                ]
            ),
            DividerBlock(),
            ContextBlock(
                block_id=block_id(),
                elements=[
                    ImageElement(image_url=static.url_for('icons/icon_relationship_hover.png'),
                                 alt_text='icon_relationship_hover'),
                    MarkdownTextObject(text='*Relationships*\t'),
                    MarkdownTextObject(
                        text=f'Calls:{preview.relationships.calls}\nCalled By:{preview.relationships.calledBy}'),
                ]
            ),
            DividerBlock(),
            ContextBlock(
                block_id=block_id(),
                elements=[
                    ImageElement(image_url=static.url_for('icons/icon_data_source.png'),
                                 alt_text='icon_data_source'),
                    MarkdownTextObject(text='*Primary Data Sources*\t'),
                    *([MarkdownTextObject(text=(tech.imageKey.value) if tech.imageKey else tech.name) for tech in
                       preview.dataSources] or [MarkdownTextObject(text='_no data_')])

                ]
            ),
        ]

from abc import ABC, abstractmethod
from typing import Sequence
from slack_sdk.models.blocks import Block, TextObject, PlainTextObject, Option

from slack_sdk.models.views import View


class AbstractView(ABC):

    def __init__(self, event=None):
        self.event = event

    @property
    @abstractmethod
    def type(self):
        pass

    # TODO: add all other required args as asbtract

    @abstractmethod
    def blocks(self) -> Sequence[dict | Block]:
        raise NotImplementedError()

    @property
    def view(self) -> View:
        return View(
            type=self.type,
            blocks=self.blocks()
        )

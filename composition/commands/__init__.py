from abc import ABC, abstractmethod
from typing import Sequence

from slack_sdk.models.blocks import Block


class AbstractCommandResponse(ABC):
    """
    Purely representational ABC of abstracting message composition. This would need to be fleshed out heavily.
    """

    def __init__(self, event=None):
        self.event = event

    @abstractmethod
    def blocks(self, *args, **kwargs) -> Sequence[dict | Block]:
        raise NotImplementedError()

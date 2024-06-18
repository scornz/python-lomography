from __future__ import annotations

# Typing
from lomography.api.types import TagDict
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from lomography.base import BaseLomography, Lomography

# External
from abc import ABC, abstractmethod


class BaseLomoTag(ABC):

    lomo: BaseLomography

    id: int
    name: str

    def __init__(self, lomo: BaseLomography, data: TagDict):
        self.lomo = lomo

        self.id = data["id"]
        self.name = data["name"]


class LomoTag(BaseLomoTag):

    lomo: Lomography

    def __init__(self, lomo: Lomography, data: TagDict):
        super().__init__(lomo, data)

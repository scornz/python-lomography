from __future__ import annotations

# Typing
from lomography.api.types import FilmDict, UserDict
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from lomography.base import BaseLomography, Lomography

# External
from abc import ABC, abstractmethod

# Internal
from .image import LomoImage


class BaseLomoUser(ABC):

    lomo: BaseLomography

    username: str
    url: str
    avatar: Optional[LomoImage]

    def __init__(self, lomo: BaseLomography, data: UserDict):
        self.lomo = lomo

        self.username = data["username"]
        self.url = data["url"]
        self.avatar = LomoImage(data["avatar"]) if data["avatar"] else None


class LomoUser(BaseLomoUser):

    lomo: Lomography

    def __init__(self, lomo: Lomography, data: UserDict):
        super().__init__(lomo, data)

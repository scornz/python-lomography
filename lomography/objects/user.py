from __future__ import annotations

# Typing
from lomography.api.types import FilmDict, UserDict
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from lomography.base import BaseLomography

from .image import LomoImage


class LomoUser:

    lomo: BaseLomography

    username: str
    url: str
    avatar: Optional[LomoImage]

    def __init__(self, lomo: BaseLomography, data: UserDict):
        self.lomo = lomo

        self.username = data["username"]
        self.url = data["url"]
        self.avatar = LomoImage(data["avatar"]) if data["avatar"] else None

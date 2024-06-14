from __future__ import annotations

# Typing
from lomography.api.types import FilmDict, UserDict
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from lomography.base import Lomography

from lomography.objects import LomoImage


class LomoUser:

    lomo: Lomography

    username: str
    url: str
    avatar: LomoImage

    def __init__(self, lomo: Lomography, data: UserDict):
        self.lomo = lomo

        self.username = data["username"]
        self.url = data["url"]
        self.avatar = LomoImage(data["avatar"])

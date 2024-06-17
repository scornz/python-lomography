from __future__ import annotations

# Typing
from lomography.api.types import LensDict
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from lomography.base import BaseLomography


class LomoLens:

    lomo: BaseLomography

    id: int
    name: str

    def __init__(self, lomo: BaseLomography, data: LensDict):
        self.lomo = lomo

        self.id = data["id"]
        self.name = data["name"]

from __future__ import annotations

# Typing
from lomography.api.types import CameraDict
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from lomography.base import Lomography


class LomoCamera:

    lomo: Lomography

    id: int
    name: str

    def __init__(self, lomo: Lomography, data: CameraDict):
        self.lomo = lomo

        self.id = data["id"]
        self.name = data["name"]

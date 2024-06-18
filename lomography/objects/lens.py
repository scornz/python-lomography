from __future__ import annotations

# Typing
from lomography.api.types import LensDict
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from lomography.base import BaseLomography, Lomography, AsyncLomography

# External
from abc import ABC, abstractmethod


class BaseLomoLens(ABC):

    lomo: BaseLomography

    id: int
    name: str

    def __init__(self, lomo: BaseLomography, data: LensDict):
        self.lomo = lomo

        self.id = data["id"]
        self.name = data["name"]


class LomoLens(BaseLomoLens):

    lomo: Lomography

    def __init__(self, lomo: Lomography, data: LensDict):
        super().__init__(lomo, data)


class AsyncLomoLens(BaseLomoLens):

    lomo: AsyncLomography

    def __init__(self, lomo: AsyncLomography, data: LensDict):
        super().__init__(lomo, data)

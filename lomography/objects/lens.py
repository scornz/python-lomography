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
    """
    Represents a lens object.

    :ivar id: The unique ID of the lens.
    :vartype id: int

    :ivar name: The name of the lens.
    :vartype name: str
    """

    lomo: Lomography

    def __init__(self, lomo: Lomography, data: LensDict):
        """
        :param lomo: The Lomography instance.
        :type lomo: Lomography

        :param data: The lens data fetched from the API.
        :type data: LensDict
        """

        super().__init__(lomo, data)


class AsyncLomoLens(BaseLomoLens):
    """
    Represents an asynchronous lens object.

    :ivar id: The unique ID of the lens.
    :vartype id: int

    :ivar name: The name of the lens.
    :vartype name: str
    """

    lomo: AsyncLomography

    def __init__(self, lomo: AsyncLomography, data: LensDict):
        """
        :param lomo: The AsyncLomography instance.
        :type lomo: AsyncLomography

        :param data: The lens data fetched from the API.
        :type data: LensDict
        """

        super().__init__(lomo, data)

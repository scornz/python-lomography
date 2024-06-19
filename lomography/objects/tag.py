from __future__ import annotations

# Typing
from lomography.api.types import TagDict
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from lomography.base import BaseLomography, Lomography, AsyncLomography

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
    """
    Represents a tag object. This is used to categorize photos, it can include
    tags like "portrait", "landscape", "black and white", etc. and makes it easier
    for users to find the photos they are looking for

    :ivar id: The unique ID of the lens.
    :vartype id: int

    :ivar name: The name of the lens.
    :vartype name: str
    """

    lomo: Lomography

    def __init__(self, lomo: Lomography, data: TagDict):
        """
        :param lomo: The Lomography instance.
        :type lomo: Lomography

        :param data: The tag data fetched from the API.
        :type data: TagDict
        """

        super().__init__(lomo, data)


class AsyncLomoTag(BaseLomoTag):
    """
    Represents an asynchronous tag object. This is used to categorize photos, it can include
    tags like "portrait", "landscape", "black and white", etc. and makes it easier
    for users to find the photos they are looking for

    :ivar id: The unique ID of the lens.
    :vartype id: int

    :ivar name: The name of the lens.
    :vartype name: str
    """

    lomo: AsyncLomography

    def __init__(self, lomo: AsyncLomography, data: TagDict):
        """
        :param lomo: The AsyncLomography instance.
        :type lomo: AsyncLomography

        :param data: The tag data fetched from the API.
        :type data: TagDict
        """

        super().__init__(lomo, data)

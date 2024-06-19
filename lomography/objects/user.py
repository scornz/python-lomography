from __future__ import annotations

# Typing
from lomography.api.types import FilmDict, UserDict
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from lomography.base import BaseLomography, Lomography, AsyncLomography

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
    """
    Represents a user object. A user can be a photographer or a member of the Lomography community,
    and can have a profile image. They can upload photos.

    :ivar username: The username of the user.
    :vartype username: str

    :ivar url: The URL of the user's profile.
    :vartype url: str

    :ivar avatar: The user's profile image.
    :vartype avatar: Optional[LomoImage]
    """

    lomo: Lomography

    def __init__(self, lomo: Lomography, data: UserDict):
        """
        :param lomo: The Lomography instance.
        :type lomo: Lomography

        :param data: The user data fetched from the API.
        :type data: UserDict
        """

        super().__init__(lomo, data)


class AsyncLomoUser(BaseLomoUser):
    """
    Represents an asynchronous user object. A user can be a photographer or a member of the Lomography community,
    and can have a profile image. They can upload photos.

    :ivar username: The username of the user.
    :vartype username: str

    :ivar url: The URL of the user's profile.
    :vartype url: str

    :ivar avatar: The user's profile image.
    :vartype avatar: Optional[LomoImage]
    """

    lomo: AsyncLomography

    def __init__(self, lomo: AsyncLomography, data: UserDict):
        """
        :param lomo: The Lomography instance.
        :type lomo: Lomography

        :param data: The user data fetched from the API.
        :type data: UserDict
        """

        super().__init__(lomo, data)

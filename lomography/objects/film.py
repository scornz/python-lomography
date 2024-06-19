from __future__ import annotations

# Typing
from lomography.api.types import FilmDict
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from lomography.base import Lomography, BaseLomography, AsyncLomography

# External
from abc import ABC, abstractmethod


class BaseLomoFilm(ABC):

    lomo: BaseLomography

    id: int
    name: str

    def __init__(self, lomo: BaseLomography, data: FilmDict):
        self.lomo = lomo

        self.id = data["id"]
        self.name = data["name"]

    @abstractmethod
    def fetch_popular_photos(self, amt: int = 20, index: int = 0):
        raise NotImplementedError

    @abstractmethod
    def fetch_recent_photos(self, amt: int = 20, index: int = 0):
        raise NotImplementedError


class LomoFilm(BaseLomoFilm):
    """
    Represents a film object. This is used to categorize photos, it can include
    films like "Lomography Color Negative 400", "Lomography Lady Grey 400",
    "Lomography X-Pro Slide 200", etc. and makes it easier for users to find the
    photos they are looking for.

    :ivar id: The unique ID of the film.
    :vartype id: int

    :ivar name: The name of the film.
    :vartype name: str
    """

    lomo: Lomography

    def __init__(self, lomo: Lomography, data: FilmDict):
        """
        :param lomo: The Lomography instance.
        :type lomo: Lomography
        :param data: The film data fetched from the API.
        :type data: FilmDict
        """
        super().__init__(lomo, data)

    def fetch_popular_photos(self, amt: int = 20, index: int = 0):
        """
        Fetch popular photos taken with this film.

        :param amt: The amount of photos to fetch. Default is 20.
        :type amt: int
        :param index: The page number to fetch. Default is 0.
        :type index: int

        :return: A list of LomoPhoto objects representing the popular photos.
        :rtype: List[LomoPhoto]
        """
        return self.lomo.fetch_popular_photos_by_film_id(self.id, amt, index)

    def fetch_recent_photos(self, amt: int = 20, index: int = 0):
        """
        Fetch recent photos taken with this film.

        :param amt: The amount of photos to fetch. Default is 20.
        :type amt: int
        :param index: The page number to fetch. Default is 0.
        :type index: int

        :return: A list of LomoPhoto objects representing the recent photos.
        :rtype: List[LomoPhoto]
        """
        return self.lomo.fetch_recent_photos_by_film_id(self.id, amt, index)


class AsyncLomoFilm(BaseLomoFilm):
    """
    Represents an asynchronous film object. This is used to categorize photos, it can include
    films like "Lomography Color Negative 400", "Lomography Lady Grey 400",
    "Lomography X-Pro Slide 200", etc. and makes it easier for users to find the
    photos they are looking for.

    :ivar id: The unique ID of the film.
    :vartype id: int

    :ivar name: The name of the film.
    :vartype name: str
    """

    lomo: AsyncLomography

    def __init__(self, lomo: AsyncLomography, data: FilmDict):
        """
        :param lomo: The AsyncLomography instance.
        :type lomo: AsyncLomography
        :param data: The film data fetched from the API.
        :type data: FilmDict
        """
        super().__init__(lomo, data)

    async def fetch_popular_photos(self, amt: int = 20, index: int = 0):
        """
        Fetch popular photos taken with this film.

        :param amt: The amount of photos to fetch. Default is 20.
        :type amt: int
        :param index: The page number to fetch. Default is 0.
        :type index: int

        :return: A list of AsyncLomoPhoto objects representing the popular photos.
        :rtype: List[AsyncLomoPhoto]
        """
        return await self.lomo.fetch_popular_photos_by_film_id(self.id, amt, index)

    async def fetch_recent_photos(self, amt: int = 20, index: int = 0):
        """
        Fetch recent photos taken with this film.

        :param amt: The amount of photos to fetch. Default is 20.
        :type amt: int
        :param index: The page number to fetch. Default is 0.
        :type index: int

        :return: A list of AsyncLomoPhoto objects representing the recent photos.
        :rtype: List[AsyncLomoPhoto]
        """
        return await self.lomo.fetch_recent_photos_by_film_id(self.id, amt, index)

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

    lomo: Lomography

    def __init__(self, lomo: Lomography, data: FilmDict):
        super().__init__(lomo, data)

    def fetch_popular_photos(self, amt: int = 20, index: int = 0):
        """Fetch popular photos taken with this film. This will return the most
        popular photos (uploaded in the last month) taken with this film.

        Args:
            `amt` (`int`): The amount of photos to fetch. Default is 20.
            `index` (`int`): The page number to fetch. Default is 0.

        Returns:
            `List[LomoPhoto]`: A list of LomoPhoto objects representing the popular photos.
        """
        return self.lomo.fetch_popular_photos_by_film_id(self.id, amt, index)

    def fetch_recent_photos(self, amt: int = 20, index: int = 0):
        """Fetch recent photos taken with this film. This will return the most
        recent photos (right as they are uploaded) taken with this film.

        Args:
            `amt` (`int`): The amount of photos to fetch. Default is 20.
            `index` (`int`): The page number to fetch. Default is 0.

        Returns:
            `List[LomoPhoto]`: A list of LomoPhoto objects representing the recent photos.
        """
        return self.lomo.fetch_recent_photos_by_film_id(self.id, amt, index)


class AsyncLomoFilm(BaseLomoFilm):
    lomo: AsyncLomography

    def __init__(self, lomo: AsyncLomography, data: FilmDict):
        super().__init__(lomo, data)

    async def fetch_popular_photos(self, amt: int = 20, index: int = 0):
        """Fetch popular photos taken with this film. This will return the most
        popular photos (uploaded in the last month) taken with this film.

        Args:
            `amt` (`int`): The amount of photos to fetch. Default is 20.
            `index` (`int`): The page number to fetch. Default is 0.

        Returns:
            `List[AsyncLomoPhoto]`: A list of LomoPhoto objects representing the popular photos.
        """
        return await self.lomo.fetch_popular_photos_by_film_id(self.id, amt, index)

    async def fetch_recent_photos(self, amt: int = 20, index: int = 0):
        """Fetch recent photos taken with this film. This will return the most
        recent photos (right as they are uploaded) taken with this film.

        Args:
            `amt` (`int`): The amount of photos to fetch. Default is 20.
            `index` (`int`): The page number to fetch. Default is 0.

        Returns:
            `List[AsyncLomoPhoto]`: A list of LomoPhoto objects representing the recent photos.
        """
        return await self.lomo.fetch_recent_photos_by_film_id(self.id, amt, index)

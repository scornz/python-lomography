from __future__ import annotations

# Typing
from lomography.api.types import FilmDict
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from lomography.base import Lomography


class LomoFilm:

    lomo: Lomography

    id: int
    name: str

    def __init__(self, lomo: Lomography, data: FilmDict):
        self.lomo = lomo

        self.id = data["id"]
        self.name = data["name"]

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

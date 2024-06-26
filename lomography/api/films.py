from __future__ import annotations

# Typing
from typing import TYPE_CHECKING
from .types import FilmDict, PhotosResponseDict, FilmsResponseDict

if TYPE_CHECKING:
    from lomography.base import BaseLomography

# Utilities
from lomography.utils.requests import get


async def fetch_films(lomo: BaseLomography, page: int = 1) -> FilmsResponseDict:
    """Fetch all film types. This will return a list of all films.

    Args:
        `lomo` (BaseLomography): An instance of the BaseLomography class.
        `page` (int): The page number to fetch. Default is 1.

    Returns:
        FilmsResponseDict: A dictionary containing the metadata and a list of films.
    """
    return await get(lomo, "/films", {"page": page})


async def fetch_film_by_id(lomo: BaseLomography, film_id: int) -> FilmDict:
    """Fetch a singular film by its unique ID. This will return a single film.

    Args:
        `lomo` (BaseLomography): An instance of the BaseLomography class.
        `film_id` (int): The unique ID of the film.

    Returns:
        FilmDict: A dictionary containing the film data.
    """
    return await get(lomo, f"/films/{film_id}")


async def fetch_popular_photos_by_film_id(
    lomo: BaseLomography, film_id: int, page: int = 1
) -> PhotosResponseDict:
    """Fetch popular photos from a specific film. This will return the most
    popular photos (uploaded in the last month) taken with that film.

    Args:
        `lomo` (BaseLomography): An instance of the BaseLomography class.
        `film_id` (int): The unique ID of the film.
        `page` (int): The page number to fetch. Default is 1.

    Returns:
        PhotosResponseDict: A dictionary containing the metadata and a list of photos.
    """
    return await get(lomo, f"/films/{film_id}/photos/popular", {"page": page})


async def fetch_recent_photos_by_film_id(
    lomo: BaseLomography, film_id: int, page: int = 1
) -> PhotosResponseDict:
    """Fetch recent photos from a specific film. This will return the most
    recent photos (right as they are uploaded).

    Args:
        `lomo` (BaseLomography): An instance of the BaseLomography class.
        `film_id` (int): The unique ID of the film.
        `page` (int): The page number to fetch. Default is 1.

    Returns:
        PhotosResponseDict: A dictionary containing the metadata and a list of photos.
    """
    return await get(lomo, f"/films/{film_id}/photos/recent", {"page": page})

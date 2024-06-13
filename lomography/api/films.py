# Internal
from lomography.base import Lomography

# Typing
from typing import List, TypedDict
from .types import FilmDict, MetaDict, PhotosResponseDict

# Utilities
from lomography.utils.requests import get


class FilmsResponseDict(TypedDict):
    """A dictionary representing a response of films."""

    meta: MetaDict
    films: List[FilmDict]


def fetch_films(lomo: Lomography) -> FilmsResponseDict:
    """Fetch all film types. This will return a list of all films.

    Args:
        `lomo` (Lomography): An instance of the Lomography class.

    Returns:
        FilmsResponseDict: A dictionary containing the metadata and a list of films.
    """
    return get(lomo, "/films")


def fetch_film_by_id(lomo: Lomography, film_id: int) -> FilmDict:
    """Fetch a singular film by its unique ID. This will return a single film.

    Args:
        `lomo` (Lomography): An instance of the Lomography class.
        `film_id` (int): The unique ID of the film.

    Returns:
        FilmDict: A dictionary containing the film data.
    """
    return get(lomo, f"/films/{film_id}")


def fetch_popular_photos_by_film_id(
    lomo: Lomography, film_id: int
) -> PhotosResponseDict:
    """Fetch popular photos from a specific film. This will return the most
    popular photos (uploaded in the last month) taken with that film.

    Args:
        `lomo` (Lomography): An instance of the Lomography class.
        `film_id` (int): The unique ID of the film.

    Returns:
        PhotosResponseDict: A dictionary containing the metadata and a list of photos.
    """
    return get(lomo, f"/films/{film_id}/photos/popular")


def fetch_recent_photos_by_film_id(
    lomo: Lomography, film_id: int
) -> PhotosResponseDict:
    """Fetch recent photos from a specific film. This will return the most
    recent photos (right as they are uploaded).

    Args:
        `lomo` (Lomography): An instance of the Lomography class.
        `film_id` (int): The unique ID of the film.

    Returns:
        PhotosResponseDict: A dictionary containing the metadata and a list of photos.
    """
    return get(lomo, f"/films/{film_id}/photos/recent")

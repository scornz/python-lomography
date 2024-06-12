# Internal
from lomography.base import Lomography

# Typing
from typing import TypedDict, List
from .types import MetaDict, PhotoDict

# Utilities
from lomography.utils.requests import get


class PhotosResponseDict(TypedDict):
    """A dictionary representing a response of photos."""

    meta: MetaDict
    photos: List[PhotoDict]


def fetch_popular_photos(lomo: Lomography) -> PhotosResponseDict:
    """Fetch popular photos. This will return the most popular photos (uploaded in the last month).

    Args:
        `lomo` (Lomography): An instance of the Lomography class.

    Returns:
        PhotosResponseDict: A dictionary containing the metadata and a list of photos.
    """
    return get(lomo, "/photos/popular")


def fetch_recent_photos(lomo: Lomography) -> PhotosResponseDict:
    """Fetch recent photos. This will return the most recent photos (right as they are uploaded).

    Args:
        `lomo` (Lomography): An instance of the Lomography class.

    Returns:
        PhotosResponseDict: A dictionary containing the metadata and a list of photos.
    """
    return get(lomo, "/photos/recent")


def fetch_selected_photos(lomo: Lomography) -> PhotosResponseDict:
    """Fetch selected photos. This will return a handpicked collection of photos.

    Args:
        `lomo` (Lomography): An instance of the Lomography class.

    Returns:
        PhotosResponseDict: A dictionary containing the metadata and a list of photos.
    """
    return get(lomo, "/photos/selected")

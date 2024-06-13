# Internal
from lomography.base import Lomography

# Typing
from .types import PhotosResponseDict

# Utilities
from lomography.utils.requests import get


def fetch_popular_photos(lomo: Lomography, page: int = 1) -> PhotosResponseDict:
    """Fetch popular photos. This will return the most popular photos (uploaded in the last month).

    Args:
        `lomo` (Lomography): An instance of the Lomography class.
        `page` (int): The page number to fetch. Default is 1.

    Returns:
        PhotosResponseDict: A dictionary containing the metadata and a list of photos.
    """
    return get(lomo, "/photos/popular", {"page": page})


def fetch_recent_photos(lomo: Lomography, page: int = 1) -> PhotosResponseDict:
    """Fetch recent photos. This will return the most recent photos (right as they are uploaded).

    Args:
        `lomo` (Lomography): An instance of the Lomography class.
        `page` (int): The page number to fetch. Default is 1.

    Returns:
        PhotosResponseDict: A dictionary containing the metadata and a list of photos.
    """
    return get(lomo, "/photos/recent", {"page": page})


def fetch_selected_photos(lomo: Lomography, page: int = 1) -> PhotosResponseDict:
    """Fetch selected photos. This will return a handpicked collection of photos.

    Args:
        `lomo` (Lomography): An instance of the Lomography class.
        `page` (int): The page number to fetch. Default is 1.

    Returns:
        PhotosResponseDict: A dictionary containing the metadata and a list of photos.
    """
    return get(lomo, "/photos/selected", {"page": page})

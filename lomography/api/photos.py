# Typing
from __future__ import annotations
from typing import TYPE_CHECKING
from .types import PhotosResponseDict

if TYPE_CHECKING:
    from lomography.base import BaseLomography

# Utilities
from lomography.utils.requests import get


async def fetch_popular_photos(
    lomo: BaseLomography, page: int = 1
) -> PhotosResponseDict:
    """Fetch popular photos. This will return the most popular photos (uploaded in the last month).

    Args:
        `lomo` (BaseLomography): An instance of the BaseLomography class.
        `page` (int): The page number to fetch. Default is 1.

    Returns:
        PhotosResponseDict: A dictionary containing the metadata and a list of photos.
    """
    return await get(lomo, "/photos/popular", {"page": page})


async def fetch_recent_photos(
    lomo: BaseLomography, page: int = 1
) -> PhotosResponseDict:
    """Fetch recent photos. This will return the most recent photos (right as they are uploaded).

    Args:
        `lomo` (BaseLomography): An instance of the BaseLomography class.
        `page` (int): The page number to fetch. Default is 1.

    Returns:
        PhotosResponseDict: A dictionary containing the metadata and a list of photos.
    """
    return await get(lomo, "/photos/recent", {"page": page})


async def fetch_selected_photos(
    lomo: BaseLomography, page: int = 1
) -> PhotosResponseDict:
    """Fetch selected photos. This will return a handpicked collection of photos.

    Args:
        `lomo` (BaseLomography): An instance of the BaseLomography class.
        `page` (int): The page number to fetch. Default is 1.

    Returns:
        PhotosResponseDict: A dictionary containing the metadata and a list of photos.
    """
    return await get(lomo, "/photos/selected", {"page": page})

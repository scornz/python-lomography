from __future__ import annotations

# Typing
from typing import TYPE_CHECKING
from .types import PhotosResponseDict

if TYPE_CHECKING:
    from lomography.base import Lomography

# Utilities
from lomography.utils.requests import get


async def fetch_recent_photos_within_bounding_box(
    lomo: Lomography,
    latitude_north: float,
    longitude_east: float,
    latitude_south: float,
    longitude_west: float,
    page: int = 1,
) -> PhotosResponseDict:
    """Fetch recent photos within a particular bounding box. This will return
    the most recent photos (right as they are uploaded).

    Args:
        `lomo` (Lomography): An instance of the Lomography class.
        `latitude_north` (float): The northern latitude of the bounding box.
        `longitude_east` (float): The eastern longitude of the bounding box.
        `latitude_south` (float): The southern latitude of the bounding box.
        `longitude_west` (float): The western longitude of the bounding box.
        `page` (int): The page number to fetch. Default is 1.

    Returns:
        PhotosResponseDict: A dictionary containing the metadata and a list of photos.
    """
    return await get(
        lomo,
        f"/location/within/{latitude_north}/{longitude_east}/{latitude_south}/{longitude_west}/photos/recent",
        {"page": page},
    )


async def fetch_popular_photos_within_bounding_box(
    lomo: Lomography,
    latitude_north: float,
    longitude_east: float,
    latitude_south: float,
    longitude_west: float,
    page: int = 1,
) -> PhotosResponseDict:
    """Fetch popular photos within a particular bounding box. This will return
      the most popular photos (uploaded in the last month).

    Args:
        `lomo` (Lomography): An instance of the Lomography class.
        `latitude_north` (float): The northern latitude of the bounding box.
        `longitude_east` (float): The eastern longitude of the bounding box.
        `latitude_south` (float): The southern latitude of the bounding box.
        `longitude_west` (float): The western longitude of the bounding box.
        `page` (int): The page number to fetch. Default is 1.

    Returns:
        PhotosResponseDict: A dictionary containing the metadata and a list of photos.
    """
    return await get(
        lomo,
        f"/location/within/{latitude_north}/{longitude_east}/{latitude_south}/{longitude_west}/photos/popular",
        {"page": page},
    )


async def fetch_photos_near_point(
    lomo: Lomography, latitude: float, longitude: float, dist: int = 10, page: int = 1
) -> PhotosResponseDict:
    """Fetch photos near a particular point in a range. This will return the photos taken
    closest to that point.

    Args:
        `lomo` (Lomography): An instance of the Lomography class.
        `latitude` (float): The latitude of the point.
        `longitude` (float): The longitude of the point.
        `dist` (int): The range in kilometers to search for photos. Default is 10.
        `page` (int): The page number to fetch. Default is 1.

    Returns:
        PhotosResponseDict: A dictionary containing the metadata and a list of photos.
    """
    return await get(
        lomo,
        f"/location/around/{latitude}/{longitude}/{dist}/photos/distance",
        {"page": page},
    )


async def fetch_recent_photos_near_point(
    lomo: Lomography, latitude: float, longitude: float, dist: int = 10, page: int = 1
) -> PhotosResponseDict:
    """Fetch recent photos near a particular point in a range. This will return
    the most recent photos (right as they are uploaded).

    Args:
        `lomo` (Lomography): An instance of the Lomography class.
        `latitude` (float): The latitude of the point.
        `longitude` (float): The longitude of the point.
        `dist` (int): The range in kilometers to search for photos. Default is 10.
        `page` (int): The page number to fetch. Default is 1.

    Returns:
        PhotosResponseDict: A dictionary containing the metadata and a list of photos.
    """
    return await get(
        lomo,
        f"/location/around/{latitude}/{longitude}/{dist}/photos/recent",
        {"page": page},
    )


async def fetch_popular_photos_near_point(
    lomo: Lomography, latitude: float, longitude: float, dist: int = 10, page: int = 1
) -> PhotosResponseDict:
    """Fetch popular photos near a particular point in a range. This will return
      the most popular photos (uploaded in the last month).

    Args:
        `lomo` (Lomography): An instance of the Lomography class.
        `latitude` (float): The latitude of the point.
        `longitude` (float): The longitude of the point.
        `dist` (int): The range in kilometers to search for photos. Default is 10.
        `page` (int): The page number to fetch. Default is 1.

    Returns:
        PhotosResponseDict: A dictionary containing the metadata and a list of photos.
    """
    return await get(
        lomo,
        f"/location/around/{latitude}/{longitude}/{dist}/photos/popular",
        {"page": page},
    )

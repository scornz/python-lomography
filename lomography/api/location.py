# Internal
from lomography.base import Lomography

# Typing
from .types import PhotosResponseDict

# Utilities
from lomography.utils.requests import get


def fetch_recent_photos_within_bounding_box(
    lomo: Lomography,
    latitude_north: float,
    longitude_east: float,
    latitude_south: float,
    longitude_west: float,
) -> PhotosResponseDict:
    """Fetch recent photos within a particular bounding box. This will return
    the most recent photos (right as they are uploaded).

    Args:
        `lomo` (Lomography): An instance of the Lomography class.
        `latitude_north` (float): The northern latitude of the bounding box.
        `longitude_east` (float): The eastern longitude of the bounding box.
        `latitude_south` (float): The southern latitude of the bounding box.
        `longitude_west` (float): The western longitude of the bounding box.

    Returns:
        PhotosResponseDict: A dictionary containing the metadata and a list of photos.
    """
    return get(
        lomo,
        f"/location/within/{latitude_north}/{longitude_east}/{latitude_south}/{longitude_west}/photos/recent",
    )


def fetch_popular_photos_within_bounding_box(
    lomo: Lomography,
    latitude_north: float,
    longitude_east: float,
    latitude_south: float,
    longitude_west: float,
) -> PhotosResponseDict:
    """Fetch popular photos within a particular bounding box. This will return
      the most popular photos (uploaded in the last month).

    Args:
        `lomo` (Lomography): An instance of the Lomography class.
        `latitude_north` (float): The northern latitude of the bounding box.
        `longitude_east` (float): The eastern longitude of the bounding box.
        `latitude_south` (float): The southern latitude of the bounding box.
        `longitude_west` (float): The western longitude of the bounding box.

    Returns:
        PhotosResponseDict: A dictionary containing the metadata and a list of photos.
    """
    return get(
        lomo,
        f"/location/within/{latitude_north}/{longitude_east}/{latitude_south}/{longitude_west}/photos/popular",
    )


def fetch_photos_near_point(
    lomo: Lomography, latitude: float, longitude: float, dist: int = 10
) -> PhotosResponseDict:
    """Fetch photos near a particular point in a range. This will return the photos taken
    closest to that point.

    Args:
        `lomo` (Lomography): An instance of the Lomography class.
        `latitude` (float): The latitude of the point.
        `longitude` (float): The longitude of the point.
        `dist` (int): The range in kilometers to search for photos. Default is 10.

    Returns:
        PhotosResponseDict: A dictionary containing the metadata and a list of photos.
    """
    return get(
        lomo,
        f"/location/around/{latitude}/{longitude}/{dist}/photos/distance",
    )


def fetch_recent_photos_near_point(
    lomo: Lomography, latitude: float, longitude: float, dist: int = 10
) -> PhotosResponseDict:
    """Fetch recent photos near a particular point in a range. This will return
    the most recent photos (right as they are uploaded).

    Args:
        `lomo` (Lomography): An instance of the Lomography class.
        `latitude` (float): The latitude of the point.
        `longitude` (float): The longitude of the point.
        `dist` (int): The range in kilometers to search for photos. Default is 10.

    Returns:
        PhotosResponseDict: A dictionary containing the metadata and a list of photos.
    """
    return get(
        lomo,
        f"/location/around/{latitude}/{longitude}/{dist}/photos/recent",
    )


def fetch_popular_photos_near_point(
    lomo: Lomography, latitude: float, longitude: float, dist: int = 10
) -> PhotosResponseDict:
    """Fetch popular photos near a particular point in a range. This will return
      the most popular photos (uploaded in the last month).

    Args:
        `lomo` (Lomography): An instance of the Lomography class.
        `latitude` (float): The latitude of the point.
        `longitude` (float): The longitude of the point.
        `dist` (int): The range in kilometers to search for photos. Default is 10.

    Returns:
        PhotosResponseDict: A dictionary containing the metadata and a list of photos.
    """
    return get(
        lomo,
        f"/location/around/{latitude}/{longitude}/{dist}/photos/popular",
    )

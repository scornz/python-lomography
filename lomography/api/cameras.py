# Internal
from lomography.base import Lomography

# Typing
from typing import List, TypedDict
from .types import CameraDict, MetaDict, PhotosResponseDict

# Utilities
from lomography.utils.requests import get


class CamerasResponseDict(TypedDict):
    """A dictionary representing a response of cameras."""

    meta: MetaDict
    cameras: List[CameraDict]


def fetch_cameras(lomo: Lomography) -> CamerasResponseDict:
    """Fetch all cameras. This will return a list of all cameras.

    Args:
        `lomo` (Lomography): An instance of the Lomography class.

    Returns:
        CamerasResponseDict: A dictionary containing the metadata and a list of cameras.
    """
    return get(lomo, "/cameras")


def fetch_camera_by_id(lomo: Lomography, camera_id: int) -> CameraDict:
    """Fetch a singular camera by its unique ID. This will return a single camera.

    Args:
        `lomo` (Lomography): An instance of the Lomography class.
        `camera_id` (int): The unique ID of the camera.

    Returns:
        CameraDict: A dictionary containing the camera data.
    """
    return get(lomo, f"/cameras/{camera_id}")


def fetch_popular_photos_by_camera_id(
    lomo: Lomography, camera_id: int
) -> PhotosResponseDict:
    """Fetch popular photos from a specific camera. This will return the most
    popular photos (uploaded in the last month) taken with that camera.

    Args:
        `lomo` (Lomography): An instance of the Lomography class.
        `camera_id` (int): The unique ID of the camera.

    Returns:
        PhotosResponseDict: A dictionary containing the metadata and a list of photos.
    """
    return get(lomo, f"/cameras/{camera_id}/photos/popular")


def fetch_recent_photos_by_camera_id(
    lomo: Lomography, camera_id: int
) -> PhotosResponseDict:
    """Fetch recent photos from a specific camera. This will return the most
    recent photos (right as they are uploaded).

    Args:
        `lomo` (Lomography): An instance of the Lomography class.
        `camera_id` (int): The unique ID of the camera.

    Returns:
        PhotosResponseDict: A dictionary containing the metadata and a list of photos.
    """
    return get(lomo, f"/cameras/{camera_id}/photos/recent")

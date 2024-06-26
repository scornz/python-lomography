from __future__ import annotations

# Typing
from typing import TYPE_CHECKING
from .types import CameraDict, PhotosResponseDict, CamerasResponseDict

if TYPE_CHECKING:
    from lomography.base import BaseLomography

# Utilities
from lomography.utils.requests import get


async def fetch_cameras(lomo: BaseLomography, page: int = 1) -> CamerasResponseDict:
    """Fetch all cameras. This will return a list of all cameras.

    Args:
        `lomo` (BaseLomography): An instance of the BaseLomography class.
        `page` (int): The page number to fetch. Default is 1.

    Returns:
        CamerasResponseDict: A dictionary containing the metadata and a list of cameras.
    """
    return await get(lomo, "/cameras", {"page": page})


async def fetch_camera_by_id(lomo: BaseLomography, camera_id: int) -> CameraDict:
    """Fetch a singular camera by its unique ID. This will return a single camera.

    Args:
        `lomo` (BaseLomography): An instance of the BaseLomography class.
        `camera_id` (int): The unique ID of the camera.

    Returns:
        CameraDict: A dictionary containing the camera data.
    """
    return await get(lomo, f"/cameras/{camera_id}")


async def fetch_popular_photos_by_camera_id(
    lomo: BaseLomography, camera_id: int, page: int = 1
) -> PhotosResponseDict:
    """Fetch popular photos from a specific camera. This will return the most
    popular photos (uploaded in the last month) taken with that camera.

    Args:
        `lomo` (BaseLomography): An instance of the BaseLomography class.
        `camera_id` (int): The unique ID of the camera.
        `page` (int): The page number to fetch. Default is 1.

    Returns:
        PhotosResponseDict: A dictionary containing the metadata and a list of photos.
    """
    return await get(lomo, f"/cameras/{camera_id}/photos/popular", {"page": page})


async def fetch_recent_photos_by_camera_id(
    lomo: BaseLomography, camera_id: int, page: int = 1
) -> PhotosResponseDict:
    """Fetch recent photos from a specific camera. This will return the most
    recent photos (right as they are uploaded).

    Args:
        `lomo` (BaseLomography): An instance of the BaseLomography class.
        `camera_id` (int): The unique ID of the camera.
        `page` (int): The page number to fetch. Default is 1.

    Returns:
        PhotosResponseDict: A dictionary containing the metadata and a list of photos.
    """
    return await get(lomo, f"/cameras/{camera_id}/photos/recent", {"page": page})

from __future__ import annotations

# Typing
from lomography.api.types import CameraDict
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from lomography.base import Lomography, BaseLomography, AsyncLomography

# External
from abc import ABC, abstractmethod


class BaseLomoCamera(ABC):

    lomo: BaseLomography

    id: int
    name: str

    def __init__(self, lomo: BaseLomography, data: CameraDict):
        self.lomo = lomo

        self.id = data["id"]
        self.name = data["name"]

    @abstractmethod
    def fetch_popular_photos(self, amt: int = 20, index: int = 0):
        raise NotImplementedError

    @abstractmethod
    def fetch_recent_photos(self, amt: int = 20, index: int = 0):
        raise NotImplementedError


class LomoCamera(BaseLomoCamera):
    """
    Represents a camera object.

    Constructor:
        `lomo` (`Lomography`): An instance of the Lomography class.
        `data` (`CameraDict`): The camera data.

    Attributes:
        `id` (`int`): The unique ID of the camera.
        `name` (`str`): The name of the camera.
    """

    lomo: Lomography

    def __init__(self, lomo: Lomography, data: CameraDict):
        super().__init__(lomo, data)

    def fetch_popular_photos(self, amt: int = 20, index: int = 0):
        """Fetch popular photos taken with this camera. This will return the most
        popular photos (uploaded in the last month) taken with this camera.

        Args:
            `amt` (`int`): The amount of photos to fetch. Default is 20.
            `index` (`int`): The page number to fetch. Default is 0.

        Returns:
            `List[LomoPhoto]`: A list of LomoPhoto objects representing the popular photos.
        """
        return self.lomo.fetch_popular_photos_by_camera_id(self.id, amt, index)

    def fetch_recent_photos(self, amt: int = 20, index: int = 0):
        """Fetch recent photos taken with this camera. This will return the most
        recent photos (right as they are uploaded) taken with this camera.

        Args:
            `amt` (`int`): The amount of photos to fetch. Default is 20.
            `index` (`int`): The page number to fetch. Default is 0.

        Returns:
            `List[LomoPhoto]`: A list of LomoPhoto objects representing the recent photos.
        """
        return self.lomo.fetch_recent_photos_by_camera_id(self.id, amt, index)


class AsyncLomoCamera(BaseLomoCamera):
    """
    Represents a camera object.

    Constructor:
        `lomo` (`AsyncLomography`): An instance of the AsyncLomography class.
        `data` (`CameraDict`): The camera data.

    Attributes:
        `id` (`int`): The unique ID of the camera.
        `name` (`str`): The name of the camera.
    """

    lomo: AsyncLomography

    def __init__(self, lomo: AsyncLomography, data: CameraDict):
        super().__init__(lomo, data)

    async def fetch_popular_photos(self, amt: int = 20, index: int = 0):
        """Fetch popular photos taken with this camera. This will return the most
        popular photos (uploaded in the last month) taken with this camera.

        Args:
            `amt` (`int`): The amount of photos to fetch. Default is 20.
            `index` (`int`): The page number to fetch. Default is 0.

        Returns:
            `List[AsyncLomoPhoto]`: A list of AsyncLomoPhoto objects representing the popular photos.
        """
        return await self.lomo.fetch_popular_photos_by_camera_id(self.id, amt, index)

    async def fetch_recent_photos(self, amt: int = 20, index: int = 0):
        """Fetch recent photos taken with this camera. This will return the most
        recent photos (right as they are uploaded) taken with this camera.

        Args:
            `amt` (`int`): The amount of photos to fetch. Default is 20.
            `index` (`int`): The page number to fetch. Default is 0.

        Returns:
            `List[AsyncLomoPhoto]`: A list of AsyncLomoPhoto objects representing the recent photos.
        """
        raise await self.lomo.fetch_recent_photos_by_camera_id(self.id, amt, index)

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
    Represents a camera object. This is used to categorize photos, it can include
    cameras like "Diana F+", "Lomo LC-A+", "Holga 120N", etc. and makes it easier
    for users to find the photos they are looking for.

    :ivar id: The unique ID of the camera.
    :vartype id: int

    :ivar name: The name of the camera.
    :vartype name: str
    """

    lomo: Lomography

    def __init__(self, lomo: Lomography, data: CameraDict):
        """
        :param lomo: The Lomography instance.
        :type lomo: Lomography
        :param data: The camera data fetched from the API.
        :type data: CameraDict
        """
        super().__init__(lomo, data)

    def fetch_popular_photos(self, amt: int = 20, index: int = 0):
        """
        Fetch popular photos taken with this camera. This will return the most
        popular photos (uploaded in the last month) taken with this camera.

        :param amt: The amount of photos to fetch. Default is 20.
        :type amt: int
        :param index: The page number to fetch. Default is 0.
        :type index: in

        :return: A list of LomoPhoto objects representing the popular photos.
        :rtype: List[LomoPhoto]
        """
        return self.lomo.fetch_popular_photos_by_camera_id(self.id, amt, index)

    def fetch_recent_photos(self, amt: int = 20, index: int = 0):
        """
        Fetch recent photos taken with this camera. This will return the most
        recent photos (right as they are uploaded) taken with this camera.

        :param amt: The amount of photos to fetch. Default is 20.
        :type amt: int
        :param index: The page number to fetch. Default is 0.
        :type index: int

        :return: A list of LomoPhoto objects representing the recent photos.
        :rtype: List[LomoPhoto]
        """
        return self.lomo.fetch_recent_photos_by_camera_id(self.id, amt, index)


class AsyncLomoCamera(BaseLomoCamera):
    """
    Represents an asynchronous camera object. This is used to categorize photos, it can include
    cameras like "Diana F+", "Lomo LC-A+", "Holga 120N", etc. and makes it easier
    for users to find the photos they are looking for.

    :ivar id: The unique ID of the camera.
    :vartype id: int

    :ivar name: The name of the camera.
    :vartype name: str
    """

    lomo: AsyncLomography

    def __init__(self, lomo: AsyncLomography, data: CameraDict):
        """
        :param lomo: The AsyncLomography instance.
        :type lomo: AsyncLomography
        :param data: The camera data fetched from the API.
        :type data: CameraDict
        """
        super().__init__(lomo, data)

    async def fetch_popular_photos(self, amt: int = 20, index: int = 0):
        """
        Fetch popular photos taken with this camera. This will return the most
        popular photos (uploaded in the last month) taken with this camera.

        :param amt: The amount of photos to fetch. Default is 20.
        :type amt: int
        :param index: The page number to fetch. Default is 0.
        :type index: int

        :return: A list of AsyncLomoPhoto objects representing the popular photos.
        :rtype: List[AsyncLomoPhoto]
        """
        return await self.lomo.fetch_popular_photos_by_camera_id(self.id, amt, index)

    async def fetch_recent_photos(self, amt: int = 20, index: int = 0):
        """
        Fetch recent photos taken with this camera. This will return the most
        recent photos (right as they are uploaded) taken with this camera.

        :param amt: The amount of photos to fetch. Default is 20.
        :type amt: int
        :param index: The page number to fetch. Default is 0.
        :type index: int

        :return: A list of AsyncLomoPhoto objects representing the recent photos.
        :rtype: List[AsyncLomoPhoto]
        """
        return await self.lomo.fetch_recent_photos_by_camera_id(self.id, amt, index)

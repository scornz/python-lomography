from __future__ import annotations

# Typing
from typing import Sequence, Optional, TYPE_CHECKING, Union, Awaitable

if TYPE_CHECKING:
    from lomography.objects.photo import BaseLomoPhoto
    from lomography.objects.camera import BaseLomoCamera
    from lomography.objects.film import BaseLomoFilm


# Internal
from lomography.utils.misc import run_async
from lomography.utils.requests import (
    fetch_films,
    fetch_photos,
    fetch_cameras,
    fetch_photos_async,
    fetch_films_async,
    fetch_cameras_async,
)
from lomography.objects import LomoCamera, LomoFilm, AsyncLomoCamera, AsyncLomoFilm

# API functions
import lomography.api.photos
import lomography.api.cameras
import lomography.api.films
import lomography.api.location


# External
from aiohttp import ClientSession
import asyncio
from abc import ABCMeta, abstractmethod


class BaseLomography(metaclass=ABCMeta):
    """
    Abstract base class for Lomography API handling. This class provides shared attributes
    and an asynchronous method for session management, meant to be used by both synchronous
    and asynchronous derived classes.
    """

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.session: Optional[ClientSession] = None

    async def create_session(self):
        if not self.session:
            self.session = ClientSession()

    async def close(self):
        """Abstract method to close the session, must be implemented by subclasses."""
        if self.session:
            await self.session.close()

    @abstractmethod
    def fetch_popular_photos(
        self, amt: int = 20, index: int = 0
    ) -> Union[Sequence[BaseLomoPhoto], Awaitable[Sequence[BaseLomoPhoto]]]:
        raise NotImplementedError

    @abstractmethod
    def fetch_recent_photos(
        self, amt: int = 20, index: int = 0
    ) -> Union[Sequence[BaseLomoPhoto], Awaitable[Sequence[BaseLomoPhoto]]]:
        raise NotImplementedError

    @abstractmethod
    def fetch_selected_photos(
        self, amt: int = 20, index: int = 0
    ) -> Union[Sequence[BaseLomoPhoto], Awaitable[Sequence[BaseLomoPhoto]]]:
        raise NotImplementedError

    @abstractmethod
    def fetch_cameras(
        self, amt: int = 20, index: int = 0
    ) -> Union[Sequence[BaseLomoCamera], Awaitable[Sequence[BaseLomoCamera]]]:
        raise NotImplementedError

    @abstractmethod
    def fetch_camera_by_id(
        self, camera_id: int
    ) -> Union[BaseLomoCamera, Awaitable[BaseLomoCamera]]:
        raise NotImplementedError

    @abstractmethod
    def fetch_popular_photos_by_camera_id(
        self, camera_id: int, amt: int = 20, index: int = 0
    ) -> Union[Sequence[BaseLomoPhoto], Awaitable[Sequence[BaseLomoPhoto]]]:
        raise NotImplementedError

    @abstractmethod
    def fetch_recent_photos_by_camera_id(
        self, camera_id: int, amt: int = 20, index: int = 0
    ) -> Union[Sequence[BaseLomoPhoto], Awaitable[Sequence[BaseLomoPhoto]]]:
        raise NotImplementedError

    @abstractmethod
    def fetch_films(
        self, amt: int = 20, index: int = 0
    ) -> Union[Sequence[BaseLomoFilm], Awaitable[Sequence[BaseLomoFilm]]]:
        raise NotImplementedError

    @abstractmethod
    def fetch_film_by_id(
        self, film_id: int
    ) -> Union[BaseLomoFilm, Awaitable[BaseLomoFilm]]:
        raise NotImplementedError

    @abstractmethod
    def fetch_popular_photos_by_film_id(
        self, film_id: int, amt: int = 20, index: int = 0
    ) -> Union[Sequence[BaseLomoPhoto], Awaitable[Sequence[BaseLomoPhoto]]]:
        raise NotImplementedError

    @abstractmethod
    def fetch_recent_photos_by_film_id(
        self, film_id: int, amt: int = 20, index: int = 0
    ) -> Union[Sequence[BaseLomoPhoto], Awaitable[Sequence[BaseLomoPhoto]]]:
        raise NotImplementedError

    @abstractmethod
    def fetch_photos_near_point(
        self, latitude: float, longitude: float, dist: int = 10
    ) -> Union[Sequence[BaseLomoPhoto], Awaitable[Sequence[BaseLomoPhoto]]]:
        raise NotImplementedError

    @abstractmethod
    def fetch_popular_photos_near_point(
        self, latitude: float, longitude: float, dist: int = 10
    ) -> Union[Sequence[BaseLomoPhoto], Awaitable[Sequence[BaseLomoPhoto]]]:
        raise NotImplementedError

    @abstractmethod
    def fetch_recent_photos_near_point(
        self, latitude: float, longitude: float, dist: int = 10
    ) -> Union[Sequence[BaseLomoPhoto], Awaitable[Sequence[BaseLomoPhoto]]]:
        raise NotImplementedError

    @abstractmethod
    def fetch_recent_photos_within_bounding_box(
        self,
        latitude_north: float,
        longitude_east: float,
        latitude_south: float,
        longitude_west: float,
    ) -> Union[Sequence[BaseLomoPhoto], Awaitable[Sequence[BaseLomoPhoto]]]:
        raise NotImplementedError

    @abstractmethod
    def fetch_popular_photos_within_bounding_box(
        self,
        latitude_north: float,
        longitude_east: float,
        latitude_south: float,
        longitude_west: float,
    ) -> Union[Sequence[BaseLomoPhoto], Awaitable[Sequence[BaseLomoPhoto]]]:
        raise NotImplementedError


class Lomography(BaseLomography):
    """
    This class provides a synchronous Python interface for the Lomography API, designed to facilitate access
    to photographic content, camera and film data, and user information. The API offers methods
    to fetch popular and recent photos, as well as specific photos taken by certain cameras or films,
    and supports pagination to navigate through larger datasets.

    Example Usage:
        >>> lomo = Lomography(api_key="your_api_key_here")
        >>> popular_photos = lomo.fetch_popular_photos(amt=15)

    More information can be found in the Lomography API documentation at https://api.lomography.com.
    """

    def __init__(self, api_key: str, loop: Optional[asyncio.AbstractEventLoop] = None):
        """
        :param api_key: The API key for authentication to access the Lomography API.
        :type api_key: str
        :param loop: An optional event loop to use for asynchronous operations. If not provided, a self-managed event loop will be created and maintained by the class.
        :type loop: asyncio.AbstractEventLoop
        """

        super().__init__(api_key)
        # Flag to indicate whether we created the loop ourselves
        self._own_loop = False

        if loop is None:
            self.loop = asyncio.new_event_loop()
            self.own_loop = True
        else:
            self.loop = loop

        self.loop.run_until_complete(self.create_session())

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        """
        Synchronously close the session by running the asynchronous close method and then close the event loop if it was created by this instance.

        :param None: No parameters.
        :return: None.
        """
        if not self.loop.is_closed():
            self.loop.run_until_complete(super().close())
            if self.own_loop:
                self.loop.close()

    def fetch_popular_photos(self, amt: int = 20, index: int = 0):
        """
        Fetch the most popular photos uploaded in the last month.
        This method utilizes a predefined API endpoint function to fetch photos
        that have been identified as the most popular over the last month based on views or likes.

        :param amt: The number of photos to retrieve. Defaults to 20.
        :type amt: int
        :param index: The zero-based index from which to start the photo retrieval within the result set. Defaults to 0.
        :type index: int

        :return: A list of LomoPhoto objects representing the most popular photos.
        :rtype: List[LomoPhoto]
        """
        return fetch_photos(
            self, lomography.api.photos.fetch_popular_photos, amt, index
        )

    def fetch_recent_photos(self, amt: int = 20, index: int = 0):
        """
        Fetch the most recent photos (right as they are uploaded).
        This method calls a function to retrieve the latest photos added to the platform,
        reflecting the most current content available.

        :param amt: The number of photos to retrieve. Defaults to 20.
        :type amt: int
        :param index: The zero-based index from which to start the photo retrieval within the result set. Defaults to 0.
        :type index: int

        :return: A list of LomoPhoto objects representing the most recent photos.
        :rtype: List[LomoPhoto]
        """
        return fetch_photos(self, lomography.api.photos.fetch_recent_photos, amt, index)

    def fetch_selected_photos(self, amt: int = 20, index: int = 0):
        """
        Fetch a selection of featured photos, curated based on specific criteria like artistic value or themes.
        This method interfaces with a function designed to pull a curated list of photos that are highlighted
        for their notable features or thematic focus.

        :param amt: The number of photos to retrieve. Defaults to 20.
        :type amt: int
        :param index: The zero-based index from which to start the photo retrieval within the result set. Defaults to 0.
        :type index: int

        :return: A list of LomoPhoto objects representing the selected photos.
        :rtype: List[LomoPhoto]
        """
        return fetch_photos(
            self, lomography.api.photos.fetch_selected_photos, amt, index
        )

    def fetch_cameras(self, amt: int = 20, index: int = 0):
        """
        Fetch a list of cameras available.

        :param amt: The number of cameras to retrieve. Defaults to 20.
        :type amt: int
        :param index: The zero-based index from which to start the camera retrieval within the result set. Defaults to 0.
        :type index: int

        :return: A list of LomoCamera objects representing the cameras.
        :rtype: List[LomoCamera]
        """
        return fetch_cameras(self, lomography.api.cameras.fetch_cameras, amt, index)

    def fetch_camera_by_id(self, camera_id: int):
        """
        Fetch a specific camera by its unique ID.

        :param camera_id: The unique ID of the camera to retrieve.
        :type camera_id: int

        :return: A LomoCamera object representing the camera.
        :rtype: LomoCamera
        """
        info = run_async(
            self, lomography.api.cameras.fetch_camera_by_id(self, camera_id)
        )
        return LomoCamera(self, info)

    def fetch_popular_photos_by_camera_id(
        self, camera_id: int, amt: int = 20, index: int = 0
    ):
        """
        Fetch popular photos taken with a specific camera. This method returns the most
        popular photos (uploaded in the last month) taken with that camera.

        :param camera_id: The unique ID of the camera.
        :type camera_id: int
        :param amt: The number of photos to retrieve. Defaults to 20.
        :type amt: int
        :param index: The zero-based index from which to start the photo retrieval within the result set. Defaults to 0.
        :type index: int

        :return: A list of LomoPhoto objects representing the popular photos.
        :rtype: List[LomoPhoto]
        """
        return fetch_photos(
            self,
            lambda lomo, page: lomography.api.cameras.fetch_popular_photos_by_camera_id(
                lomo, camera_id, page
            ),
            amt,
            index,
        )

    def fetch_recent_photos_by_camera_id(
        self, camera_id: int, amt: int = 20, index: int = 0
    ):
        """
        Fetch recent photos taken with a specific camera. This method returns the most
        recent photos (right as they are uploaded) taken with that camera.

        :param camera_id: The unique ID of the camera.
        :type camera_id: int
        :param amt: The number of photos to retrieve. Defaults to 20.
        :type amt: int
        :param index: The zero-based index from which to start the photo retrieval within the result set. Defaults to 0.
        :type index: int

        :return: A list of LomoPhoto objects representing the recent photos.
        :rtype: List[LomoPhoto]
        """
        return fetch_photos(
            self,
            lambda lomo, page: lomography.api.cameras.fetch_recent_photos_by_camera_id(
                lomo, camera_id, page
            ),
            amt,
            index,
        )

    def fetch_films(self, amt: int = 20, index: int = 0):
        """
        Fetch a list of films available.

        :param amt: The number of films to retrieve. Defaults to 20.
        :type amt: int
        :param index: The zero-based index from which to start the film retrieval within the result set. Defaults to 0.
        :type index: int

        :return: A list of LomoFilm objects representing the films.
        :rtype: List[LomoFilm]
        """
        return fetch_films(self, lomography.api.films.fetch_films, amt, index)

    def fetch_film_by_id(self, film_id: int):
        """
        Fetch a specific film by its unique ID.

        :param film_id: The unique ID of the film to retrieve.
        :type film_id: int

        :return: A LomoFilm object representing the film.
        :rtype: LomoFilm
        """
        info = run_async(self, lomography.api.films.fetch_film_by_id(self, film_id))
        return LomoFilm(self, info)

    def fetch_popular_photos_by_film_id(
        self, film_id: int, amt: int = 20, index: int = 0
    ):
        """
        Fetch popular photos taken with a specific film. This will return the most
        popular photos (uploaded in the last month) taken with that film.

        :param film_id: The unique ID of the film.
        :type film_id: int
        :param amt: The number of photos to retrieve. Defaults to 20.
        :type amt: int
        :param index: The zero-based index from which to start the photo retrieval within the result set. Defaults to 0.
        :type index: int

        :return: A list of LomoPhoto objects representing the popular photos.
        :rtype: List[LomoPhoto]
        """
        return fetch_photos(
            self,
            lambda lomo, page: lomography.api.films.fetch_popular_photos_by_film_id(
                lomo, film_id, page
            ),
            amt,
            index,
        )

    def fetch_recent_photos_by_film_id(
        self, film_id: int, amt: int = 20, index: int = 0
    ):
        """
        Fetch recent photos taken with a specific film. This will return the most
        recent photos (right as they are uploaded) taken with that film.

        :param film_id: The unique ID of the film.
        :type film_id: int
        :param amt: The number of photos to retrieve. Defaults to 20.
        :type amt: int
        :param index: The zero-based index from which to start the photo retrieval within the result set. Defaults to 0.
        :type index: int

        :return: A list of LomoPhoto objects representing the recent photos.
        :rtype: List[LomoPhoto]
        """
        return fetch_photos(
            self,
            lambda lomo, page: lomography.api.films.fetch_recent_photos_by_film_id(
                lomo, film_id, page
            ),
            amt,
            index,
        )

    def fetch_photos_near_point(
        self,
        latitude: float,
        longitude: float,
        dist: int = 10,
        amt: int = 20,
        index: int = 0,
    ):
        """
        Fetch photos near a specific geographic point within a given distance.

        :param latitude: The latitude of the geographic point.
        :type latitude: float
        :param longitude: The longitude of the geographic point.
        :type longitude: float
        :param dist: The distance (in kilometers) around the point to include photos from. Defaults to 10 km.
        :type dist: int
        :param amt: The number of photos to retrieve. Defaults to 20.
        :type amt: int
        :param index: The zero-based index from which to start the photo retrieval within the result set. Defaults to 0.
        :type index: int

        :return: A list of LomoPhoto objects representing the photos.
        :rtype: List[LomoPhoto]
        """
        return fetch_photos(
            self,
            lambda lomo, page: lomography.api.location.fetch_photos_near_point(
                lomo, latitude, longitude, dist, page
            ),
            amt,
            index,
        )

    def fetch_popular_photos_near_point(
        self,
        latitude: float,
        longitude: float,
        dist: int = 10,
        amt: int = 20,
        index: int = 0,
    ):
        """
        Fetch popular photos near a specific geographic point within a given distance, based on popularity.

        :param latitude: The latitude of the geographic point.
        :type latitude: float
        :param longitude: The longitude of the geographic point.
        :type longitude: float
        :param dist: The distance (in kilometers) around the point to include photos from. Defaults to 10 km.
        :type dist: int
        :param amt: The number of photos to retrieve. Defaults to 20.
        :type amt: int
        :param index: The zero-based index from which to start the photo retrieval within the result set. Defaults to 0.
        :type index: int

        :return: A list of LomoPhoto objects representing the popular photos.
        :rtype: List[LomoPhoto]
        """
        return fetch_photos(
            self,
            lambda lomo, page: lomography.api.location.fetch_popular_photos_near_point(
                lomo, latitude, longitude, dist, page
            ),
            amt,
            index,
        )

    def fetch_recent_photos_near_point(
        self,
        latitude: float,
        longitude: float,
        dist: int = 10,
        amt: int = 20,
        index: int = 0,
    ):
        """
        Fetch recent photos near a specific geographic point within a given distance.

        :param latitude: The latitude of the geographic point.
        :type latitude: float
        :param longitude: The longitude of the geographic point.
        :type longitude: float
        :param dist: The distance (in kilometers) around the point to include photos from. Defaults to 10 km.
        :type dist: int
        :param amt: The number of photos to retrieve. Defaults to 20.
        :type amt: int
        :param index: The zero-based index from which to start the photo retrieval within the result set. Defaults to 0.
        :type index: int

        :return: A list of LomoPhoto objects representing the recent photos.
        :rtype: List[LomoPhoto]
        """
        return fetch_photos(
            self,
            lambda lomo, page: lomography.api.location.fetch_recent_photos_near_point(
                lomo, latitude, longitude, dist, page
            ),
            amt,
            index,
        )

    def fetch_recent_photos_within_bounding_box(
        self,
        latitude_north: float,
        longitude_east: float,
        latitude_south: float,
        longitude_west: float,
        amt: int = 20,
        index: int = 0,
    ):
        """
        Fetch recent photos within a specified bounding box.

        :param latitude_north: The northern latitude of the bounding box.
        :type latitude_north: float
        :param longitude_east: The eastern longitude of the bounding box.
        :type longitude_east: float
        :param latitude_south: The southern latitude of the bounding box.
        :type latitude_south: float
        :param longitude_west: The western longitude of the bounding box.
        :type longitude_west: float
        :param amt: The number of photos to retrieve. Defaults to 20.
        :type amt: int
        :param index: The zero-based index from which to start the photo retrieval within the result set. Defaults to 0.
        :type index: int

        :return: A list of LomoPhoto objects representing the recent photos.
        :rtype: List[LomoPhoto]
        """
        return fetch_photos(
            self,
            lambda lomo, page: lomography.api.location.fetch_recent_photos_within_bounding_box(
                lomo,
                latitude_north,
                longitude_east,
                latitude_south,
                longitude_west,
                page,
            ),
            amt,
            index,
        )

    def fetch_popular_photos_within_bounding_box(
        self,
        latitude_north: float,
        longitude_east: float,
        latitude_south: float,
        longitude_west: float,
        amt: int = 20,
        index: int = 0,
    ):
        """
        Fetch popular photos within a specified bounding box.

        :param latitude_north: The northern latitude of the bounding box.
        :type latitude_north: float
        :param longitude_east: The eastern longitude of the bounding box.
        :type longitude_east: float
        :param latitude_south: The southern latitude of the bounding box.
        :type latitude_south: float
        :param longitude_west: The western longitude of the bounding box.
        :type longitude_west: float
        :param amt: The number of photos to retrieve. Defaults to 20.
        :type amt: int
        :param index: The zero-based index from which to start the photo retrieval within the result set. Defaults to 0.
        :type index: int

        :return: A list of LomoPhoto objects representing the popular photos.
        :rtype: List[LomoPhoto]
        """
        return fetch_photos(
            self,
            lambda lomo, page: lomography.api.location.fetch_popular_photos_within_bounding_box(
                lomo,
                latitude_north,
                longitude_east,
                latitude_south,
                longitude_west,
                page,
            ),
            amt,
            index,
        )


class AsyncLomography(BaseLomography):
    """
    This class provides an asynchronous Python interface for the Lomography API, designed to facilitate access
    to photographic content, camera and film data, and user information. The API offers methods
    to fetch popular and recent photos, as well as specific photos taken by certain cameras or films,
    and supports pagination to navigate through larger datasets.

    Example Usage:
        >>> async_lomo = AsyncLomography(api_key="api_key_here")
        >>> photos = await async_lomo.fetch_popular_photos(amt=15)

    More information can be found in the Lomography API documentation at https://api.lomography.com.
    """

    def __init__(self, api_key: str):
        """
        :param api_key: The API key for authentication to access the Lomography API.
        :type api_key: str
        """

        super().__init__(api_key)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def fetch_popular_photos(self, amt: int = 20, index: int = 0):
        """
        Fetch the most popular photos uploaded in the last month using an asynchronous API endpoint.
        This method is designed to fetch photos based on views or likes, identifying them as most popular.

        :param amt: The number of photos to retrieve, default is 20.
        :type amt: int
        :param index: The zero-based index from which to start the photo retrieval, default is 0.
        :type index: int

        :return: A list of AsyncLomoPhoto objects representing the most popular photos.
        :rtype: List[AsyncLomoPhoto]
        """
        return await fetch_photos_async(
            self, lomography.api.photos.fetch_popular_photos, amt, index
        )

    async def fetch_recent_photos(self, amt: int = 20, index: int = 0):
        """
        Fetch the most recent photos asynchronously, capturing the latest uploads to the platform.

        :param amt: The number of photos to retrieve, defaults to 20.
        :type amt: int
        :param index: The zero-based index from which to start the photo retrieval, defaults to 0.
        :type index: int

        :return: A list of AsyncLomoPhoto objects representing the most recent photos.
        :rtype: List[AsyncLomoPhoto]
        """
        return await fetch_photos_async(
            self, lomography.api.photos.fetch_recent_photos, amt, index
        )

    async def fetch_selected_photos(self, amt: int = 20, index: int = 0):
        """
        Fetch a selection of featured photos asynchronously, curated based on specific criteria such as artistic value or themes.

        :param amt: The number of photos to retrieve, defaults to 20.
        :type amt: int
        :param index: The zero-based index from which to start the photo retrieval, defaults to 0.
        :type index: int

        :return: A list of AsyncLomoPhoto objects representing the selected photos.
        :rtype: List[AsyncLomoPhoto]
        """
        return await fetch_photos_async(
            self, lomography.api.photos.fetch_selected_photos, amt, index
        )

    async def fetch_cameras(self, amt: int = 20, index: int = 0):
        """
        Asynchronously fetch a list of cameras available on the platform.

        :param amt: The number of cameras to retrieve, defaults to 20.
        :type amt: int
        :param index: The zero-based index from which to start the camera retrieval, defaults to 0.
        :type index: int

        :return: A list of AsyncLomoCamera objects representing the cameras.
        :rtype: List[AsyncLomoCamera]
        """
        return await fetch_cameras_async(
            self, lomography.api.cameras.fetch_cameras, amt, index
        )

    async def fetch_camera_by_id(self, camera_id: int):
        """
        Asynchronously fetch a specific camera by its unique ID.

        :param camera_id: The unique ID of the camera to retrieve.
        :type camera_id: int

        :return: An AsyncLomoCamera object representing the camera.
        :rtype: AsyncLomoCamera
        """
        info = await lomography.api.cameras.fetch_camera_by_id(self, camera_id)
        return AsyncLomoCamera(self, info)

    async def fetch_popular_photos_by_camera_id(
        self, camera_id: int, amt: int = 20, index: int = 0
    ):
        """
        Asynchronously fetch popular photos taken with a specific camera, identified based on uploads in the last month.

        :param camera_id: The unique ID of the camera.
        :type camera_id: int
        :param amt: The number of photos to retrieve, defaults to 20.
        :type amt: int
        :param index: The zero-based index from which to start the photo retrieval, defaults to 0.
        :type index: int

        :return: A list of AsyncLomoPhoto objects representing the popular photos.
        :rtype: List[AsyncLomoPhoto]
        """
        return await fetch_photos_async(
            self,
            lambda lomo, page: lomography.api.cameras.fetch_popular_photos_by_camera_id(
                lomo, camera_id, page
            ),
            amt,
            index,
        )

    async def fetch_recent_photos_by_camera_id(
        self, camera_id: int, amt: int = 20, index: int = 0
    ):
        """
        Asynchronously fetch the most recent photos taken with a specific camera, showcasing the latest uploads.

        :param camera_id: The unique ID of the camera.
        :type camera_id: int
        :param amt: The number of photos to retrieve, defaults to 20.
        :type amt: int
        :param index: The zero-based index from which to start the photo retrieval, defaults to 0.
        :type index: int

        :return: A list of AsyncLomoPhoto objects representing the recent photos.
        :rtype: List[AsyncLomoPhoto]
        """
        return await fetch_photos_async(
            self,
            lambda lomo, page: lomography.api.cameras.fetch_recent_photos_by_camera_id(
                lomo, camera_id, page
            ),
            amt,
            index,
        )

    async def fetch_films(self, amt: int = 20, index: int = 0):
        """
        Asynchronously fetch a list of films available on the platform.

        :param amt: The number of films to retrieve, defaults to 20.
        :type amt: int
        :param index: The zero-based index from which to start the film retrieval, defaults to 0.
        :type index: int

        :return: A list of AsyncLomoFilm objects representing the films.
        :rtype: List[AsyncLomoFilm]
        """
        return await fetch_films_async(
            self, lomography.api.films.fetch_films, amt, index
        )

    async def fetch_film_by_id(self, film_id: int):
        """
        Asynchronously fetch a specific film by its unique ID.

        :param film_id: The unique ID of the film to retrieve.
        :type film_id: int

        :return: An AsyncLomoFilm object representing the film.
        :rtype: AsyncLomoFilm
        """
        info = await lomography.api.films.fetch_film_by_id(self, film_id)
        return AsyncLomoFilm(self, info)

    async def fetch_popular_photos_by_film_id(
        self, film_id: int, amt: int = 20, index: int = 0
    ):
        """
        Asynchronously fetch popular photos taken with a specific film. This method returns the most
        popular photos uploaded in the last month taken with that film.

        :param film_id: The unique ID of the film.
        :type film_id: int
        :param amt: The number of photos to retrieve. Defaults to 20.
        :type amt: int
        :param index: The zero-based index from which to start the photo retrieval. Defaults to 0.
        :type index: int

        :return: A list of AsyncLomoPhoto objects representing the popular photos.
        :rtype: List[AsyncLomoPhoto]
        """
        return await fetch_photos_async(
            self,
            lambda lomo, page: lomography.api.films.fetch_popular_photos_by_film_id(
                lomo, film_id, page
            ),
            amt,
            index,
        )

    async def fetch_recent_photos_by_film_id(
        self, film_id: int, amt: int = 20, index: int = 0
    ):
        """
        Asynchronously fetch recent photos taken with a specific film. This method returns the most
        recent photos uploaded, showcasing current content.

        :param film_id: The unique ID of the film.
        :type film_id: int
        :param amt: The number of photos to retrieve. Defaults to 20.
        :type amt: int
        :param index: The zero-based index from which to start the photo retrieval. Defaults to 0.
        :type index: int

        :return: A list of AsyncLomoPhoto objects representing the recent photos.
        :rtype: List[AsyncLomoPhoto]
        """
        return await fetch_photos_async(
            self,
            lambda lomo, page: lomography.api.films.fetch_recent_photos_by_film_id(
                lomo, film_id, page
            ),
            amt,
            index,
        )

    async def fetch_photos_near_point(
        self,
        latitude: float,
        longitude: float,
        dist: int = 10,
        amt: int = 20,
        index: int = 0,
    ):
        """
        Asynchronously fetch photos near a specific geographic point within a certain distance.

        :param latitude: The latitude of the point.
        :type latitude: float
        :param longitude: The longitude of the point.
        :type longitude: float
        :param dist: The distance in kilometers around the point to include for photo retrieval. Default is 10 km.
        :type dist: int
        :param amt: The number of photos to retrieve. Defaults to 20.
        :type amt: int
        :param index: The zero-based index from which to start the photo retrieval. Defaults to 0.
        :type index: int

        :return: A list of AsyncLomoPhoto objects representing the photos near the specified point.
        :rtype: List[AsyncLomoPhoto]
        """
        return await fetch_photos_async(
            self,
            lambda lomo, page: lomography.api.location.fetch_photos_near_point(
                lomo, latitude, longitude, dist, page
            ),
            amt,
            index,
        )

    async def fetch_popular_photos_near_point(
        self,
        latitude: float,
        longitude: float,
        dist: int = 10,
        amt: int = 20,
        index: int = 0,
    ):
        """
        Asynchronously fetch popular photos near a specific geographic point. This method focuses on the most
        popular photos uploaded in the last month within the specified distance.

        :param latitude: The latitude of the point.
        :type latitude: float
        :param longitude: The longitude of the point.
        :type longitude: float
        :param dist: The distance in kilometers around the point to include for photo retrieval. Default is 10 km.
        :type dist: int
        :param amt: The number of photos to retrieve. Defaults to 20.
        :type amt: int
        :param index: The zero-based index from which to start the photo retrieval. Defaults to 0.
        :type index: int

        :return: A list of AsyncLomoPhoto objects representing the popular photos near the specified point.
        :rtype: List[AsyncLomoPhoto]
        """
        return await fetch_photos_async(
            self,
            lambda lomo, page: lomography.api.location.fetch_popular_photos_near_point(
                lomo, latitude, longitude, dist, page
            ),
            amt,
            index,
        )

    async def fetch_recent_photos_near_point(
        self,
        latitude: float,
        longitude: float,
        dist: int = 10,
        amt: int = 20,
        index: int = 0,
    ):
        """
        Asynchronously fetch recent photos near a particular point in a range. This will return
        the most recent photos (right as they are uploaded) taken closest to that point.

        :param latitude: The latitude of the point.
        :type latitude: float
        :param longitude: The longitude of the point.
        :type longitude: float
        :param dist: The range in kilometers to search for photos. Default is 10.
        :type dist: int
        :param amt: The number of photos to retrieve. Defaults to 20.
        :type amt: int
        :param index: The zero-based index from which to start the photo retrieval within the result set. Defaults to 0.
        :type index: int

        :return: A list of AsyncLomoPhoto objects representing the recent photos.
        :rtype: List[AsyncLomoPhoto]
        """
        return await fetch_photos_async(
            self,
            lambda lomo, page: lomography.api.location.fetch_recent_photos_near_point(
                lomo, latitude, longitude, dist, page
            ),
            amt,
            index,
        )

    async def fetch_recent_photos_within_bounding_box(
        self,
        latitude_north: float,
        longitude_east: float,
        latitude_south: float,
        longitude_west: float,
        amt: int = 20,
        index: int = 0,
    ):
        """
        Asynchronously fetch recent photos within a particular bounding box. This will return the most
        recent photos (right as they are uploaded).

        :param latitude_north: The northern latitude of the bounding box.
        :type latitude_north: float
        :param longitude_east: The eastern longitude of the bounding box.
        :type longitude_east: float
        :param latitude_south: The southern latitude of the bounding box.
        :type latitude_south: float
        :param longitude_west: The western longitude of the bounding box.
        :type longitude_west: float
        :param amt: The number of photos to retrieve. Defaults to 20.
        :type amt: int
        :param index: The zero-based index from which to start the photo retrieval within the result set. Defaults to 0.
        :type index: int

        :return: A list of AsyncLomoPhoto objects representing the recent photos.
        :rtype: List[AsyncLomoPhoto]
        """
        return await fetch_photos_async(
            self,
            lambda lomo, page: lomography.api.location.fetch_recent_photos_within_bounding_box(
                lomo,
                latitude_north,
                longitude_east,
                latitude_south,
                longitude_west,
                page,
            ),
            amt,
            index,
        )

    async def fetch_popular_photos_within_bounding_box(
        self,
        latitude_north: float,
        longitude_east: float,
        latitude_south: float,
        longitude_west: float,
        amt: int = 20,
        index: int = 0,
    ):
        """
        Asynchronously fetch popular photos within a particular bounding box. This will return the most
        popular photos (uploaded in the last month).

        :param latitude_north: The northern latitude of the bounding box.
        :type latitude_north: float
        :param longitude_east: The eastern longitude of the bounding box.
        :type longitude_east: float
        :param latitude_south: The southern latitude of the bounding box.
        :type latitude_south: float
        :param longitude_west: The western longitude of the bounding box.
        :type longitude_west: float
        :param amt: The number of photos to retrieve. Defaults to 20.
        :type amt: int
        :param index: The zero-based index from which to start the photo retrieval within the result set. Defaults to 0.
        :type index: int

        :return: A list of AsyncLomoPhoto objects representing the popular photos.
        :rtype: List[AsyncLomoPhoto]
        """
        return await fetch_photos_async(
            self,
            lambda lomo, page: lomography.api.location.fetch_popular_photos_within_bounding_box(
                lomo,
                latitude_north,
                longitude_east,
                latitude_south,
                longitude_west,
                page,
            ),
            amt,
            index,
        )

from __future__ import annotations

# Typing
from typing import Sequence, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from lomography.objects.photo import BaseLomoPhoto
    from lomography.objects.camera import BaseLomoCamera
    from lomography.objects.film import BaseLomoFilm


# Internal
from lomography.utils.misc import run_async
from lomography.utils.requests import fetch_films, fetch_photos, fetch_cameras
from lomography.objects import LomoPhoto, LomoCamera, LomoFilm

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
    ) -> Sequence[BaseLomoPhoto]:
        raise NotImplementedError

    @abstractmethod
    def fetch_recent_photos(
        self, amt: int = 20, index: int = 0
    ) -> Sequence[BaseLomoPhoto]:
        raise NotImplementedError

    @abstractmethod
    def fetch_selected_photos(
        self, amt: int = 20, index: int = 0
    ) -> Sequence[BaseLomoPhoto]:
        raise NotImplementedError

    @abstractmethod
    def fetch_cameras(self, amt: int = 20, index: int = 0) -> Sequence[BaseLomoCamera]:
        raise NotImplementedError

    @abstractmethod
    def fetch_camera_by_id(self, camera_id: int) -> BaseLomoCamera:
        raise NotImplementedError

    @abstractmethod
    def fetch_popular_photos_by_camera_id(
        self, camera_id: int, amt: int = 20, index: int = 0
    ) -> Sequence[BaseLomoPhoto]:
        raise NotImplementedError

    @abstractmethod
    def fetch_recent_photos_by_camera_id(
        self, camera_id: int, amt: int = 20, index: int = 0
    ) -> Sequence[BaseLomoPhoto]:
        raise NotImplementedError

    @abstractmethod
    def fetch_films(self, amt: int = 20, index: int = 0) -> Sequence[BaseLomoFilm]:
        raise NotImplementedError

    @abstractmethod
    def fetch_film_by_id(self, film_id: int) -> BaseLomoFilm:
        raise NotImplementedError

    @abstractmethod
    def fetch_popular_photos_by_film_id(
        self, film_id: int, amt: int = 20, index: int = 0
    ) -> Sequence[BaseLomoPhoto]:
        raise NotImplementedError

    @abstractmethod
    def fetch_recent_photos_by_film_id(
        self, film_id: int, amt: int = 20, index: int = 0
    ) -> Sequence[BaseLomoPhoto]:
        raise NotImplementedError

    @abstractmethod
    def fetch_photos_near_point(
        self, latitude: float, longitude: float, dist: int = 10
    ) -> Sequence[BaseLomoPhoto]:
        raise NotImplementedError

    @abstractmethod
    def fetch_popular_photos_near_point(
        self, latitude: float, longitude: float, dist: int = 10
    ) -> Sequence[BaseLomoPhoto]:
        raise NotImplementedError

    @abstractmethod
    def fetch_recent_photos_near_point(
        self, latitude: float, longitude: float, dist: int = 10
    ) -> Sequence[BaseLomoPhoto]:
        raise NotImplementedError

    @abstractmethod
    def fetch_recent_photos_within_bounding_box(
        self,
        latitude_north: float,
        longitude_east: float,
        latitude_south: float,
        longitude_west: float,
    ) -> Sequence[BaseLomoPhoto]:
        raise NotImplementedError

    @abstractmethod
    def fetch_popular_photos_within_bounding_box(
        self,
        latitude_north: float,
        longitude_east: float,
        latitude_south: float,
        longitude_west: float,
    ) -> Sequence[BaseLomoPhoto]:
        raise NotImplementedError


class Lomography(BaseLomography):
    """
    This class provides a synchronous Python interface for the Lomography API, designed to facilitate access
    to photographic content, camera and film data, and user information. The API offers methods
    to fetch popular and recent photos, as well as specific photos taken by certain cameras or films,
    and supports pagination to navigate through larger datasets.

    Constructor:
        `api_key` (str): The API key for authentication to access the Lomography API.
        `verify` (bool): Whether or not to verify the API key upon construction. Default is False.

    Methods:
        `get_photos(category, page=1)`: Retrieve photos based on category ('popular', 'recent', or 'selected').
        `get_camera_photos(camera_id, category)`: Fetch photos taken with a specific camera.
        `get_film_photos(film_id, category)`: Fetch photos using a specific film type.
        `get_location_photos(latitude, longitude, radius, category)`: Fetch photos around a specific geographic location.

    Example Usage:
        >>> lomo = Lomography(api_key="your_api_key_here")
        >>> popular_photos = lomo.get_photos('popular')

    Raises:
        ValueError: If API key is missing or invalid.
        ConnectionError: If there are issues with the network connection.
        HTTPError: For HTTP errors from the API.

    The full API is documented at the Lomography website.
    """

    def __init__(self, api_key: str, loop: Optional[asyncio.AbstractEventLoop] = None):
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
        """Synchronously close the session by running the asynchronous close method and then close the event loop if it was created by this instance."""
        if not self.loop.is_closed():
            # Ensure the session close coroutine runs to completion
            self.loop.run_until_complete(super().close())
            # Only close the loop if it was created by this instance
            if self.own_loop:
                self.loop.close()

    def fetch_popular_photos(self, amt: int = 20, index: int = 0):
        """Fetch the most popular photos uploaded in the last month.
        This method utilizes a predefined API endpoint function to fetch photos
        that have been identified as the most popular over the last month based on
          views or likes.

        Args:
            `amt` (`int`): The number of photos to retrieve. Defaults to 20.
            `index` (`int`): The zero-based index from which to start the photo
            retrieval within the result set. Defaults to 0.

        Returns:
            `List[LomoPhoto]`: A list of LomoPhoto objects representing the most popular photos.
        """

        return fetch_photos(
            self, lomography.api.photos.fetch_popular_photos, amt, index
        )

    def fetch_recent_photos(self, amt: int = 20, index: int = 0):
        """Fetch the most recent photos (right as they are uploaded). This method calls a
        function to retrieve the latest photos added to the platform,
        reflecting the most current content available.

        Args:
            `amt` (`int`): The number of photos to retrieve. Defaults to 20.
            `index` (`int`): The zero-based index from which to start the photo
            retrieval within the result set. Defaults to 0.

        Returns:
            `List[LomoPhoto]`: A list of LomoPhoto objects representing the most recent photos.
        """

        return fetch_photos(self, lomography.api.photos.fetch_recent_photos, amt, index)

    def fetch_selected_photos(self, amt: int = 20, index: int = 0):
        """Fetch a selection of featured photos, curated based on specific
        criteria like artistic value or themes. This method interfaces with a
        function designed to pull a curated list of photos that are highlighted
        for their notable features or thematic focus.

        Args:
            `amt` (`int`): The number of photos to retrieve. Defaults to 20.
            `index` (`int`): The zero-based index from which to start the photo
            retrieval within the result set. Defaults to 0.

        Returns:
            `List[LomoPhoto]`: A list of LomoPhoto objects representing the selected photos.
        """

        return fetch_photos(
            self, lomography.api.photos.fetch_selected_photos, amt, index
        )

    def fetch_cameras(self, amt: int = 20, index: int = 0):
        """Fetch a list of cameras available.

        Args:
            `amt` (`int`): The number of cameras to retrieve. Defaults to 20.
            `index` (`int`): The zero-based index from which to start the camera
            retrieval within the result set. Defaults to 0.

        Returns:
            `List[LomoCamera]`: A list of LomoCamera objects representing the cameras.
        """
        return fetch_cameras(self, lomography.api.cameras.fetch_cameras, amt, index)

    def fetch_camera_by_id(self, camera_id: int):
        """Fetch a specific camera by its unique ID.

        Args:
            `camera_id` (`int`): The unique ID of the camera to retrieve.

        Returns:
            `LomoCamera`: A LomoCamera object representing the camera.
        """

        info = run_async(
            self, lomography.api.cameras.fetch_camera_by_id(self, camera_id)
        )
        return LomoCamera(self, info)

    def fetch_popular_photos_by_camera_id(
        self, camera_id: int, amt: int = 20, index: int = 0
    ):
        """Fetch popular photos taken with a specific camera. This will return the most
        popular photos (uploaded in the last month) taken with that camera.

        Args:
            `camera_id` (`int`): The unique ID of the camera.
            `amt` (`int`): The number of photos to retrieve. Defaults to 20.
            `index` (`int`): The zero-based index from which to start the photo
            retrieval within the result set. Defaults to 0.

        Returns:
            `List[LomoPhoto]`: A list of LomoPhoto objects representing the popular photos.
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
        """Fetch recent photos taken with a specific camera. This will return the most
        recent photos (right as they are uploaded) taken with that camera.

        Args:
            `camera_id` (`int`): The unique ID of the camera.
            `amt` (`int`): The number of photos to retrieve. Defaults to 20.
            `index` (`int`): The zero-based index from which to start the photo
            retrieval within the result set. Defaults to 0.

        Returns:
            `List[LomoPhoto]`: A list of LomoPhoto objects representing the recent photos.
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
        """Fetch a list of films available.

        Args:
            `amt` (`int`): The number of films to retrieve. Defaults to 20.
            `index` (`int`): The zero-based index from which to start the film
            retrieval within the result set. Defaults to 0.

        Returns:
            `List[LomoFilm]`: A list of LomoFilm objects representing the films.
        """
        return fetch_films(self, lomography.api.films.fetch_films, amt, index)

    def fetch_film_by_id(self, film_id: int):
        """
        Fetch a specific film by its unique ID.

        Args:
            `film_id` (int): The unique ID of the film to retrieve.

        Returns:
            `LomoFilm`: A LomoFilm object representing the film.
        """
        info = run_async(self, lomography.api.films.fetch_film_by_id(self, film_id))
        return LomoFilm(self, info)

    def fetch_popular_photos_by_film_id(
        self, film_id: int, amt: int = 20, index: int = 0
    ):
        """Fetch popular photos taken with a specific film. This will return the most
        popular photos (uploaded in the last month) taken with that film.

        Args:
            `film_id` (`int`): The unique ID of the film.
            `amt` (`int`): The number of photos to retrieve. Defaults to 20.
            `index` (`int`): The zero-based index from which to start the photo
            retrieval within the result set. Defaults to 0.

        Returns:
            `List[LomoPhoto]`: A list of LomoPhoto objects representing the popular photos.
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
        """Fetch recent photos taken with a specific film. This will return the most
        recent photos (right as they are uploaded) taken with that film.

        Args:
            `film_id` (`int`): The unique ID of the film.
            `amt` (`int`): The number of photos to retrieve. Defaults to 20.
            `index` (`int`): The zero-based index from which to start the photo
            retrieval within the result set. Defaults to 0.

        Returns:
            `List[LomoPhoto]`: A list of LomoPhoto objects representing the recent photos.
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
        """Fetch photos near a particular point in a range. This will return the photos taken
        closest to that point.

        Args:
            `latitude` (`float`): The latitude of the point.
            `longitude` (`float`): The longitude of the point.
            `dist` (`int`): The range in kilometers to search for photos. Default is 10.
            `amt` (`int`): The number of photos to retrieve. Defaults to 20.
            `index` (`int`): The zero-based index from which to start the photo
            retrieval within the result set. Defaults to 0.

        Returns:
            `List[LomoPhoto]`: A list of LomoPhoto objects representing the photos.
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
        """Fetch popular photos near a particular point in a range. This will return the most
        popular photos (uploaded in the last month) taken closest to that point.

        Args:
            `latitude` (`float`): The latitude of the point.
            `longitude` (`float`): The longitude of the point.
            `dist` (`int`): The range in kilometers to search for photos. Default is 10.
            `amt` (`int`): The number of photos to retrieve. Defaults to 20.
            `index` (`int`): The zero-based index from which to start the photo
            retrieval within the result set. Defaults to 0.

        Returns:
            `List[LomoPhoto]`: A list of LomoPhoto objects representing the popular photos.
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
        """Fetch recent photos near a particular point in a range. This will return
        the most recent photos (right as they are uploaded) taken closest to that point.

        Args:
            `latitude` (`float`): The latitude of the point.
            `longitude` (`float`): The longitude of the point.
            `dist` (`int`): The range in kilometers to search for photos. Default is 10.
            `amt` (`int`): The number of photos to retrieve. Defaults to 20.
            `index` (`int`): The zero-based index from which to start the photo
            retrieval within the result set. Defaults to 0.

        Returns:
            `List[LomoPhoto]`: A list of LomoPhoto objects representing the recent photos.
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
        """Fetch recent photos within a particular bounding box. This will return the most
        recent photos (right as they are uploaded).

        Args:
            `latitude_north` (`float`): The northern latitude of the bounding box.
            `longitude_east` (`float`): The eastern longitude of the bounding box.
            `latitude_south` (`float`): The southern latitude of the bounding box.
            `longitude_west` (`float`): The western longitude of the bounding box.
            `amt` (`int`): The number of photos to retrieve. Defaults to 20.
            `index` (`int`): The zero-based index from which to start the photo
            retrieval within the result set. Defaults to 0.

        Returns:
            `List[LomoPhoto]`: A list of LomoPhoto objects representing the recent photos.
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
        """Fetch popular photos within a particular bounding box. This will return the most
        popular photos (uploaded in the last month).

        Args:
            `latitude_north` (`float`): The northern latitude of the bounding box.
            `longitude_east` (`float`): The eastern longitude of the bounding box.
            `latitude_south` (`float`): The southern latitude of the bounding box.
            `longitude_west` (`float`): The western longitude of the bounding box.
            `amt` (`int`): The number of photos to retrieve. Defaults to 20.
            `index` (`int`): The zero-based index from which to start the photo
            retrieval within the result set. Defaults to 0

        Returns:
            `List[LomoPhoto]`: A list of LomoPhoto objects representing the popular photos.
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

    Constructor:
        `api_key` (str): The API key for authentication to access the Lomography API.
        `verify` (bool): Whether or not to verify the API key upon construction. Default is False.

    Methods:
        `get_photos(category, page=1)`: Retrieve photos based on category ('popular', 'recent', or 'selected').
        `get_camera_photos(camera_id, category)`: Fetch photos taken with a specific camera.
        `get_film_photos(film_id, category)`: Fetch photos using a specific film type.
        `get_location_photos(latitude, longitude, radius, category)`: Fetch photos around a specific geographic location.

    Example Usage:
        >>> lomo = AsyncLomography(api_key="your_api_key_here")
        >>> popular_photos = await lomo.get_photos('popular')
        >>> await lomo.close()

    Raises:
        ValueError: If API key is missing or invalid.
        ConnectionError: If there are issues with the network connection.
        HTTPError: For HTTP errors from the API.

    The full API is documented at the Lomography website.
    """

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def get_photos(self, category, page=1):
        # Asynchronous network calls
        pass

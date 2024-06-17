from __future__ import annotations

# Typing
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from lomography.objects import LomoPhoto, LomoCamera, LomoFilm

# Internal
from lomography.utils.requests import fetch_photos
from lomography.api.photos import (
    fetch_popular_photos,
    fetch_recent_photos,
    fetch_selected_photos,
)

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
    def fetch_popular_photos(self, amt: int = 20, index: int = 0):
        raise NotImplementedError

    @abstractmethod
    def fetch_recent_photos(self, amt: int = 20, index: int = 0):
        raise NotImplementedError

    @abstractmethod
    def fetch_selected_photos(self, amt: int = 20, index: int = 0):
        raise NotImplementedError

    @abstractmethod
    def fetch_cameras(self, amt: int = 20, index: int = 0):
        raise NotImplementedError

    @abstractmethod
    def fetch_camera_by_id(self, id: int):
        raise NotImplementedError

    @abstractmethod
    def fetch_films(self, amt: int = 20, index: int = 0):
        raise NotImplementedError

    @abstractmethod
    def fetch_film_by_id(self, id: int):
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

    def fetch_popular_photos(self, amt: int = 20, index: int = 0) -> List[LomoPhoto]:
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

        return fetch_photos(self, fetch_popular_photos, amt, index)

    def fetch_recent_photos(self, amt: int = 20, index: int = 0) -> List[LomoPhoto]:
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

        return fetch_photos(self, fetch_recent_photos, amt, index)

    def fetch_selected_photos(self, amt: int = 20, index: int = 0) -> List[LomoPhoto]:
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

        return fetch_photos(self, fetch_selected_photos, amt, index)

    def fetch_cameras(self, amt: int = 20, index: int = 0):
        raise NotImplementedError

    def fetch_camera_by_id(self, id: int):
        raise NotImplementedError

    def fetch_films(self, amt: int = 20, index: int = 0):
        raise NotImplementedError

    def fetch_film_by_id(self, id: int):
        raise NotImplementedError


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

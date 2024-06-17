from typing import Optional
from aiohttp import ClientSession
import asyncio


class BaseLomography:
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

    def get_photos(self, category, page=1):
        # Example synchronous method using asynchronous session management
        # Placeholder implementation
        pass


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

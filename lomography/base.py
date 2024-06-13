from requests import Session

from lomography.api import verify_authentication


class Lomography:
    """
    This class provides a Python interface for the Lomography API, designed to facilitate access
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

    def __init__(self, api_key: str, verify: bool = False):
        self._api_key = api_key
        self.session = Session()

        # Verify authentication, unless otherwise disabled
        if verify and not verify_authentication(self):
            raise ValueError(
                "Invalid API key. Please provide a valid Lomography API key."
            )

    @property
    def api_key(self):
        """Return the API key used for authentication."""

        return self._api_key

    def get_photos(self, category, page=1):
        pass

    def get_camera_photos(self, camera_id, category):
        pass

    def get_film_photos(self, film_id, category):
        pass

    def get_location_photos(self, latitude, longitude, radius, category):
        pass

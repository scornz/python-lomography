from lomography.base import Lomography
from lomography.api.cameras import fetch_camera_by_id

from requests import HTTPError


def verify_authentication(lomo: Lomography) -> bool:
    """Verify that the API key is valid. NOTE: This calls /cameras/3314883,
    which is a known camera ID, however this isn't an actual authentication
    endpoint. It works for now, but this implementation will probably change eventually.

    Args:
        `lomo` (Lomography): An instance of the Lomography class.

    Returns:
        bool: True if the API key is valid, False otherwise.
    """
    try:
        fetch_camera_by_id(lomo, 3314883)
        return True
    except HTTPError:
        return False

from __future__ import annotations

from lomography.api.cameras import fetch_camera_by_id

from requests import HTTPError

# Typing
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from lomography.base import BaseLomography


async def verify_authentication(lomo: BaseLomography) -> bool:
    """Verify that the API key is valid. NOTE: This calls /cameras/3314883,
    which is a known camera ID, however this isn't an actual authentication
    endpoint. It works for now, but this implementation will probably change eventually.

    Args:
        `lomo` (BaseLomography): An instance of the BaseLomography class.

    Returns:
        bool: True if the API key is valid, False otherwise.
    """
    try:
        await fetch_camera_by_id(lomo, 3314883)
        return True
    except HTTPError:
        return False

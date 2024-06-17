from __future__ import annotations

# Internal
from lomography.constants import BASE_URL
from .misc import run_async

# Typing
from typing import List, Optional, TYPE_CHECKING
from lomography.api.types import PhotoDict, PhotosResponseDict

if TYPE_CHECKING:
    from lomography.base import BaseLomography, Lomography
    from lomography.objects.photo import LomoPhoto

# External
from aiohttp import ClientError
import asyncio


async def get(lomo: BaseLomography, url: str, params: Optional[dict] = None):
    # If no parameters are provided, set it to an empty dictionary
    if params is None:
        params = {}

    try:
        assert lomo.session is not None
        async with lomo.session.get(
            f"{BASE_URL}{url}", params={**params, "api_key": lomo.api_key}
        ) as response:
            response.raise_for_status()
            return await response.json()
    except ClientError as e:
        raise e


async def _fetch_photo_dicts(
    lomo: BaseLomography, url: str, amt: int = 20, index: int = 0
) -> List[PhotoDict]:
    """Fetch a list of photos from the Lomography API based on the given URL and parameters.
    Start fetching from the specified index and return the specified amount of photos. Note that
    the API returns photos in pages of 20, so the index and amount are based on the full list of photos.
    Operating on numbers that are not divisble by 20 may result in fetching unnecessary pages.
    """

    # Photos are returned in pages of 20, so we need to calculate the page numbers we
    # need to fetch based on the index and amount
    start_page = (index // 20) + 1
    end_page = ((index + amt - 1) // 20) + 1

    # Generate all page URLs that need to be fetched
    tasks = []
    for page in range(start_page, end_page + 1):
        params = {"page": page}
        task = asyncio.create_task(get(lomo, url, params))
        tasks.append(task)

    # Run all the fetch tasks concurrently
    results: List[PhotosResponseDict] = await asyncio.gather(*tasks)
    photos = [photo for result in results for photo in result["photos"]]
    return photos[index : index + amt]


def fetch_photos(
    lomo: Lomography, url: str, amt: int = 20, index: int = 0
) -> List[LomoPhoto]:
    """Fetch a list of photos from the Lomography API based on the given URL and parameters.
    Start fetching from the specified index and return the specified amount of photos. Note that
    the API returns photos in pages of 20, so the index and amount are based on the full list of photos.
    Operating on numbers that are not divisble by 20 may result in fetching unnecessary pages. Return
    synchronous photo objects.
    """

    # Run the asynchronous function to fetch photo dictionaries
    photos = run_async(lomo, _fetch_photo_dicts(lomo, url, amt, index))

    # Import the LomoPhoto class here to avoid circular imports, so this function is available everywhere
    from lomography.objects.photo import LomoPhoto

    return [LomoPhoto(lomo, photo) for photo in photos]

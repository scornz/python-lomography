from __future__ import annotations

# Internal
from lomography.constants import BASE_URL
from .misc import run_async

# Typing
from typing import List, Optional, TYPE_CHECKING, Callable, Coroutine, Any
from lomography.api.types import (
    CameraDict,
    FilmDict,
    PhotoDict,
    PhotosResponseDict,
    CamerasResponseDict,
    FilmsResponseDict,
)

if TYPE_CHECKING:
    from lomography.base import BaseLomography, Lomography, AsyncLomography
    from lomography.objects import (
        LomoPhoto,
        LomoCamera,
        LomoFilm,
        AsyncLomoPhoto,
        AsyncLomoCamera,
        AsyncLomoFilm,
    )

# External
from aiohttp import ClientError
import asyncio


async def get(lomo: BaseLomography, url: str, params: Optional[dict] = None):
    # If no parameters are provided, set it to an empty dictionary
    if params is None:
        params = {}

    # Make sure lomography has a session
    await lomo.create_session()

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
    lomo: BaseLomography,
    fetch: Callable[[BaseLomography, int], Coroutine[Any, Any, PhotosResponseDict]],
    amt: int = 20,
    index: int = 0,
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
        task = asyncio.create_task(fetch(lomo, page))
        tasks.append(task)

    # Run all the fetch tasks concurrently
    results: List[PhotosResponseDict] = await asyncio.gather(*tasks)
    photos = [photo for result in results for photo in result["photos"]]
    return photos[index : index + amt]


async def _fetch_camera_dicts(
    lomo: BaseLomography,
    fetch: Callable[[BaseLomography, int], Coroutine[Any, Any, CamerasResponseDict]],
    amt: int = 20,
    index: int = 0,
) -> List[CameraDict]:
    """Fetch a list of cameras from the Lomography API based on the given URL and parameters.
    Start fetching from the specified index and return the specified amount of cameras. Note that
    the API returns photos in pages of 20, so the index and amount are based on the full list of cameras.
    Operating on numbers that are not divisble by 20 may result in fetching unnecessary pages.
    """

    # Photos are returned in pages of 20, so we need to calculate the page numbers we
    # need to fetch based on the index and amount
    start_page = (index // 20) + 1
    end_page = ((index + amt - 1) // 20) + 1

    # Generate all page URLs that need to be fetched
    tasks = []
    for page in range(start_page, end_page + 1):
        task = asyncio.create_task(fetch(lomo, page))
        tasks.append(task)

    # Run all the fetch tasks concurrently
    results: List[CamerasResponseDict] = await asyncio.gather(*tasks)
    cameras = [photo for result in results for photo in result["cameras"]]
    return cameras[index : index + amt]


async def _fetch_film_dicts(
    lomo: BaseLomography,
    fetch: Callable[[BaseLomography, int], Coroutine[Any, Any, FilmsResponseDict]],
    amt: int = 20,
    index: int = 0,
) -> List[FilmDict]:
    """Fetch a list of films from the Lomography API based on the given URL and parameters.
    Start fetching from the specified index and return the specified amount of films. Note that
    the API returns photos in pages of 20, so the index and amount are based on the full list of films.
    Operating on numbers that are not divisble by 20 may result in fetching unnecessary pages.
    """

    # Photos are returned in pages of 20, so we need to calculate the page numbers we
    # need to fetch based on the index and amount
    start_page = (index // 20) + 1
    end_page = ((index + amt - 1) // 20) + 1

    # Generate all page URLs that need to be fetched
    tasks = []
    for page in range(start_page, end_page + 1):
        task = asyncio.create_task(fetch(lomo, page))
        tasks.append(task)

    # Run all the fetch tasks concurrently
    results: List[FilmsResponseDict] = await asyncio.gather(*tasks)
    films = [photo for result in results for photo in result["films"]]
    return films[index : index + amt]


def fetch_photos(
    lomo: Lomography,
    fetch: Callable[[BaseLomography, int], Coroutine[Any, Any, PhotosResponseDict]],
    amt: int = 20,
    index: int = 0,
) -> List[LomoPhoto]:
    """Fetch a list of photos from the Lomography API based on the given URL and parameters.
    Start fetching from the specified index and return the specified amount of photos. Note that
    the API returns photos in pages of 20, so the index and amount are based on the full list of photos.
    Operating on numbers that are not divisble by 20 may result in fetching unnecessary pages. Return
    synchronous photo objects.
    """

    # Run the asynchronous function to fetch photo dictionaries
    photos = run_async(lomo, _fetch_photo_dicts(lomo, fetch, amt, index))

    # Import the LomoPhoto class here to avoid circular imports, so this function is available everywhere
    from lomography.objects.photo import LomoPhoto

    return [LomoPhoto(lomo, photo) for photo in photos]


async def fetch_photos_async(
    lomo: AsyncLomography,
    fetch: Callable[[BaseLomography, int], Coroutine[Any, Any, PhotosResponseDict]],
    amt: int = 20,
    index: int = 0,
):
    """Fetch a list of photos from the Lomography API based on the given URL and parameters.
    Start fetching from the specified index and return the specified amount of photos. Note that
    the API returns photos in pages of 20, so the index and amount are based on the full list of photos.
    Operating on numbers that are not divisble by 20 may result in fetching unnecessary pages. Return
    asynchronous photo objects.
    """

    # Run the asynchronous function to fetch photo dictionaries
    photos = await _fetch_photo_dicts(lomo, fetch, amt, index)

    # Import the LomoPhoto class here to avoid circular imports, so this function is available everywhere
    from lomography.objects.photo import AsyncLomoPhoto

    return [AsyncLomoPhoto(lomo, photo) for photo in photos]


def fetch_cameras(
    lomo: Lomography,
    fetch: Callable[[BaseLomography, int], Coroutine[Any, Any, CamerasResponseDict]],
    amt: int = 20,
    index: int = 0,
) -> List[LomoCamera]:
    """Fetch a list of cameras from the Lomography API based on the given URL and parameters.
    Start fetching from the specified index and return the specified amount of cameras. Note that
    the API returns cameras in pages of 20, so the index and amount are based on the full list of cameras.
    Operating on numbers that are not divisble by 20 may result in fetching unnecessary pages. Return
    synchronous camera objects.
    """

    # Run the asynchronous function to fetch photo dictionaries
    cameras = run_async(lomo, _fetch_camera_dicts(lomo, fetch, amt, index))

    # Import the LomoPhoto class here to avoid circular imports, so this function is available everywhere
    from lomography.objects.camera import LomoCamera

    return [LomoCamera(lomo, camera) for camera in cameras]


async def fetch_cameras_async(
    lomo: AsyncLomography,
    fetch: Callable[[BaseLomography, int], Coroutine[Any, Any, CamerasResponseDict]],
    amt: int = 20,
    index: int = 0,
):
    """Fetch a list of cameras from the Lomography API based on the given URL and parameters.
    Start fetching from the specified index and return the specified amount of cameras. Note that
    the API returns cameras in pages of 20, so the index and amount are based on the full list of cameras.
    Operating on numbers that are not divisble by 20 may result in fetching unnecessary pages. Return
    asynchronous camera objects.
    """

    # Run the asynchronous function to fetch photo dictionaries
    cameras = await _fetch_camera_dicts(lomo, fetch, amt, index)

    # Import the LomoPhoto class here to avoid circular imports, so this function is available everywhere
    from lomography.objects.camera import AsyncLomoCamera

    return [AsyncLomoCamera(lomo, camera) for camera in cameras]


def fetch_films(
    lomo: Lomography,
    fetch: Callable[[BaseLomography, int], Coroutine[Any, Any, FilmsResponseDict]],
    amt: int = 20,
    index: int = 0,
) -> List[LomoFilm]:
    """Fetch a list of films from the Lomography API based on the given URL and parameters.
    Start fetching from the specified index and return the specified amount of films. Note that
    the API returns films in pages of 20, so the index and amount are based on the full list of films.
    Operating on numbers that are not divisble by 20 may result in fetching unnecessary pages. Return
    synchronous film objects.
    """

    # Run the asynchronous function to fetch photo dictionaries
    films = run_async(lomo, _fetch_film_dicts(lomo, fetch, amt, index))

    # Import the LomoPhoto class here to avoid circular imports, so this function is available everywhere
    from lomography.objects.film import LomoFilm

    return [LomoFilm(lomo, film) for film in films]


async def fetch_films_async(
    lomo: AsyncLomography,
    fetch: Callable[[BaseLomography, int], Coroutine[Any, Any, FilmsResponseDict]],
    amt: int = 20,
    index: int = 0,
):
    """Fetch a list of films from the Lomography API based on the given URL and parameters.
    Start fetching from the specified index and return the specified amount of films. Note that
    the API returns films in pages of 20, so the index and amount are based on the full list of films.
    Operating on numbers that are not divisble by 20 may result in fetching unnecessary pages. Return
    asynchronous film objects.
    """

    # Run the asynchronous function to fetch photo dictionaries
    films = await _fetch_film_dicts(lomo, fetch, amt, index)

    # Import the LomoPhoto class here to avoid circular imports, so this function is available everywhere
    from lomography.objects.film import AsyncLomoFilm

    return [AsyncLomoFilm(lomo, film) for film in films]

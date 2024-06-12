# Typing
from typing import TypedDict


class CameraDict(TypedDict):
    """A specific camera model, associated with an ID and name. Returned
    directly from the Lomography API, with little to no processing.

    Example:
    ```
    {
        "id": 3314883,
        "name": "Lomo LC-A"
    }
    ```
    """

    id: int
    name: str


class FilmDict(TypedDict):
    """A specific type of film, associated with an ID and name. Returned
    directly from the Lomography API, with little to no processing.

    Example:
    ```
    {
      "id": 871911028,
      "name": "Lomographic X-Pro Slide 100"
    }
    ```
    """

    id: int
    name: str


class LocationDict(TypedDict):
    """A location object, normally associated with a particular photo. Returned
    directly from the Lomography API, with little to no processing.

    Example:
    ```
    {
        "longitude": -82.4575967,
        "latitude": 27.1000553
    }
    ```
    """

    longitude: float
    latitude: float


class ImageDict(TypedDict):
    """A specific image. Returned directly from the Lomography API,
    with little to no processing. Normally a sub-object of a photo object or
    an avatar of a user.

    Example:
    ```
    {
        "url": "http://cloud.lomography.com/576/386/88/3c4c6c7e9774abdd110b45b679c1c579a42da2.jpg",
        "width": 576,
        "height": 386
    }
    ```
    """

    url: str
    width: int
    height: int


class AssetsDict(TypedDict):
    """A specific set of photo assets, containing a small and large photo.
    Returned directly from the Lomography API, with little to no processing.

    Example:
    ```
    {
        "small": {
            "url": "http://cloud.lomography.com/96/64/88/3c4c6c7e9774abdd110b45b679c1c579a42da2.jpg",
            "width": 96,
            "height": 64
        },
        "large": {
            "url": "http://cloud.lomography.com/576/386/88/3c4c6c7e9774abdd110b45b679c1c579a42da2.jpg",
            "width": 576,
            "height": 386
        }
    }
    ```
    """

    """Small image (with an inner bounding box of 96 x 64 pixels - 
    that means the image is at least this size)"""
    small: ImageDict

    """Large image (with an outer bounding box of 576 x 576 pixels - that means 
    the image is at most this size)."""
    large: ImageDict


class UserDict(TypedDict):
    """A specific user. Returned directly from the Lomography API, with
    little to no processing. Normally a sub-object of a photo object.

    Example:
    ```
    {
        "username": "recurving",
        "url": "http://www.lomography.com/homes/recurving",
        "avatar": {
          "url": "http://cloud.lomography.com/290/192/58/63307c8ed53828bd563cc08156d044de8dd93f.jpg",
          "width": 290,
          "height": 192
        }
    }
    ```
    """

    username: str
    url: str
    avatar: ImageDict


class PhotoDict(TypedDict):
    """A specific photo. Returned directly from the Lomography API,
    with little to no processing.

    Example:
    ```
    {
        "id": 11336951,
        "title": "Los Angeles",
        "description": "All these shots were taken during a trip to Los Angeles in April 2010.",
        "url": "http://www.lomography.com/photos/11336951",
        "camera": {
            "id": 3314883,
            "name": "Lomo LC-A"
        },
        "film": {
            "id": 871911028,
            "name": "Lomographic X-Pro Slide 100"
        },
        "location": {
            "longitude": -82.4575967,
            "latitude": 27.1000553
        },
        "assets": {
            "small": {
            "url": "http://cloud.lomography.com/96/64/88/3c4c6c7e9774abdd110b45b679c1c579a42da2.jpg",
            "width": 96,
            "height": 64
            },
            "large": {
            "url": "http://cloud.lomography.com/576/386/88/3c4c6c7e9774abdd110b45b679c1c579a42da2.jpg",
            "width": 576,
            "height": 386
            }
        },
        "user": {
            "username": "recurving",
            "url": "http://www.lomography.com/homes/recurving",
            "avatar": {
            "url": "http://cloud.lomography.com/290/192/58/63307c8ed53828bd563cc08156d044de8dd93f.jpg",
            "width": 290,
            "height": 192
            }
        }
    }
    ```
    """

    id: str
    title: str
    description: str
    url: str
    camera: CameraDict
    film: FilmDict
    location: LocationDict
    assets: AssetsDict
    user: UserDict


class MetaDict(TypedDict):
    """Metadata associated with a response from the Lomography API.
    Normally contains information about the total number of items and
    the current page.

    Example:
    ```
    {
        "total_entries": 20,
        "per_page": 20,
        "page": 1
    }
    ```
    """

    total_entries: int
    per_page: int
    page: int

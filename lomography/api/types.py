# Typing
from typing import List, Literal, NotRequired, Optional, TypedDict, Union


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


class LensDict(TypedDict):
    """A specific lens model, associated with an ID and name. Returned
    directly from the Lomography API, with little to no processing.

    Example:
    ```
    {
        "id":3532,
        "name":"Zenzanon MC 40mm f4"
    }
    ```
    """

    id: int
    name: str


class TagDict(TypedDict):
    """A specific tag, associated with an ID and name. Returned
    directly from the Lomography API, with little to no processing.

    Example:
    ```
    {
        "id": 74065,
        "name": "lewis"
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
    with little to no processing.

    Example:
    ```
    {
        "url": "http://cloud.lomography.com/576/386/88/3c4c6c7e9774abdd...",
        "width": 576,
        "height": 386
    }
    ```
    """

    url: str
    width: int
    height: int


class PhotoImageDict(ImageDict):
    """A specific photo. Returned directly from the Lomography API,
    with little to no processing. Normally a sub-object of a photo object.

    Example:
    ```
    {
        "url":"https://cdn.assets.lomography.com/33/520...",
        "width":576,
        "height":432,
        "ratio":1.33333333333333,
        "filename":"576x432x2.jpg"
    }
    ```
    """

    ratio: float
    filename: str


class AssetsDict(TypedDict):
    """A specific set of photo assets, containing a small and large photo.
    Returned directly from the Lomography API, with little to no processing.

    Example:
    ```
    {
        "small": {
            "url": "http://cloud.lomography.com/96/64/88/3c4c6c7e9774...",
            "width": 96,
            "height": 64
        },
        "large": {
            "url": "http://cloud.lomography.com/576/386/88/3c4c6c7e9774...",
            "width": 576,
            "height": 386
        }
    }
    ```
    """

    """Small image (with an inner bounding box of 96 x 64 pixels - 
    that means the image is at least this size)"""
    small: PhotoImageDict

    """Large image (with an outer bounding box of 576 x 576 pixels - that means 
    the image is at most this size)."""
    large: PhotoImageDict


class UserDict(TypedDict):
    """A specific user. Returned directly from the Lomography API, with
    little to no processing. Normally a sub-object of a photo object.

    Example:
    ```
    {
        "username": "recurving",
        "url": "http://www.lomography.com/homes/recurving",
        "avatar": {
          "url": "http://cloud.lomography.com/290/192/58/63307c8ed53828b...",
          "width": 290,
          "height": 192
        }
    }
    ```
    """

    username: str
    url: str
    avatar: Optional[ImageDict]


class PhotoDict(TypedDict):
    """A specific photo. Returned directly from the Lomography API,
    with little to no processing.

    Example:
    ```
    {
        "id": 27316210,
        "title":"Shieling, Barvas, Lewis",
        "description":"ETRSi ~ Kentmere 100 ~ Rodinal 1+25 @ 9mins",
        "url":"http://www.lomography.com/photos/27316210",
        "assets":{
            "large":{
                "url":"https://cdn.assets.lomography.com/33/520...",
                "width":576,
                "height":432,
                "ratio":1.33333333333333,
                "filename":"576x432x2.jpg"
            },
            "small":{
                "url":"https://cdn.assets.lomography.com/33/520...",
                "width":96,
                "height":72,
                "ratio":1.33333333333333,
                "filename":"96x72x2.jpg"
            }
        },
        "asset_hash":"33520fdaf9568a5c722546e919ef90de96eec983",
        "asset_width":3500,
        "asset_height":2625,
        "asset_ratio":1.33333333333333,
        "asset_preview":"data:image/gif;base64,R0lGODdhBQAFAPQAAB4e...",
        "film":{
            "id":871927949,
            "name":"Kentmere 100"
        },
        "camera":{
            "id":3323987,
            "name":"Zenza Bronica ETRSi"
        },
        "lens":{
            "id":3532,
            "name":"Zenzanon MC 40mm f4"
        },
        "user":{
            "id":536699,
            "username":"jonography",
            "url":"http://www.lomography.com/homes/jonography",
            "avatar":{
                "url":"https://cdn.assets.lomography.com/33/da621a4c20...",
                "width":192,
                "height":192
            }
        },
        "tags":[
            {
                "id":74065,
                "name":"lewis"
            },
            {
                "id":87148,
                "name":"outer hebrides"
            },
        ]
    }
    ```
    """

    id: int
    title: str
    description: str
    url: str
    camera: Optional[CameraDict]
    film: Optional[FilmDict]

    # Specified in the API documentation, but currently not included
    # location: NotRequired[LocationDict]

    assets: AssetsDict

    asset_hash: str
    asset_width: int
    asset_height: int
    asset_ratio: float
    asset_preview: str

    lens: Optional[LensDict]
    tags: List[TagDict]

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


class PhotosResponseDict(TypedDict):
    """A dictionary representing a response of photos."""

    meta: MetaDict
    photos: List[PhotoDict]


class CamerasResponseDict(TypedDict):
    """A dictionary representing a response of cameras."""

    meta: MetaDict
    cameras: List[CameraDict]


class FilmsResponseDict(TypedDict):
    """A dictionary representing a response of films."""

    meta: MetaDict
    films: List[FilmDict]

from __future__ import annotations

# Typing
from lomography.api.types import PhotoDict
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from lomography.base import BaseLomography, Lomography, AsyncLomography

# External
from abc import ABC

# Internal
from .camera import BaseLomoCamera, LomoCamera, AsyncLomoCamera
from .film import BaseLomoFilm, LomoFilm, AsyncLomoFilm
from .image import LomoPhotoImage
from .lens import BaseLomoLens, LomoLens, AsyncLomoLens
from .tag import BaseLomoTag, LomoTag, AsyncLomoTag
from .user import BaseLomoUser, LomoUser, AsyncLomoUser


class BaseLomoPhoto(ABC):

    lomo: BaseLomography

    id: int
    title: Optional[str]
    description: Optional[str]
    url: str

    camera: Optional[BaseLomoCamera]
    film: Optional[BaseLomoFilm]
    user: BaseLomoUser

    small: LomoPhotoImage
    large: LomoPhotoImage

    asset_hash: str
    asset_width: int
    asset_height: int
    asset_ratio: float
    asset_preview: str

    lens: Optional[BaseLomoLens]
    tags: List[BaseLomoTag]

    def __init__(self, lomo: BaseLomography, data: PhotoDict):
        self.lomo = lomo
        self._data = data

        self.id = data["id"]
        self.title = data["title"] if data["title"] else None
        self.description = data["description"] if data["description"] else None

        self.url = data["url"]

        self.small = LomoPhotoImage(data["assets"]["small"])
        self.large = LomoPhotoImage(data["assets"]["large"])

        self.asset_hash = data["asset_hash"]
        self.asset_width = data["asset_width"]
        self.asset_height = data["asset_height"]
        self.asset_ratio = data["asset_ratio"]
        self.asset_preview = data["asset_preview"]


class LomoPhoto(BaseLomoPhoto):
    """
    A photo object from Lomography, containing all the necessary information
    about a photo. This class contains the camera, film, user, lens, tags, and
    images associated with the photo.

    :ivar id: The unique identifier for the photo.
    :vartype id: int

    :ivar title: The title of the photo.
    :vartype title: Optional[str]

    :ivar description: The description of the photo.
    :vartype description: Optional[str]

    :ivar url: The URL of the photo.
    :vartype url: str

    :ivar camera: The camera used to take the photo.
    :vartype camera: Optional[LomoCamera]

    :ivar film: The film used to take the photo.
    :vartype film: Optional[LomoFilm]

    :ivar user: The user who uploaded the photo.
    :vartype user: LomoUser

    :ivar small: The small version of the photo.
    :vartype small: LomoPhotoImage

    :ivar large: The large version of the photo.
    :vartype large: LomoPhotoImage

    :ivar asset_hash: The hash of the photo asset.
    :vartype asset_hash: str

    :ivar asset_width: The width of the photo asset.
    :vartype asset_width: int

    :ivar asset_height: The height of the photo asset.
    :vartype asset_height: int

    :ivar asset_ratio: The aspect ratio of the photo asset.
    :vartype asset_ratio: float

    :ivar asset_preview: The preview of the photo asset.
    :vartype asset_preview: str

    :ivar lens: The lens used to take the photo.
    :vartype lens: Optional[LomoLens]

    :ivar tags: The tags associated with the photo.
    :vartype tags: List[LomoTag]
    """

    lomo: Lomography

    camera: Optional[LomoCamera]
    film: Optional[LomoFilm]
    user: LomoUser

    lens: Optional[LomoLens]
    tags: List[LomoTag]  # type: ignore

    def __init__(self, lomo: Lomography, data: PhotoDict):
        """
        :param lomo: The Lomography instance
        :type lomo: Lomography
        :param data: The photo data, fetched directly from the API
        :type data: PhotoDict
        """

        super().__init__(lomo, data)

        self.camera = LomoCamera(lomo, data["camera"]) if data["camera"] else None
        self.film = LomoFilm(lomo, data["film"]) if data["film"] else None
        self.user = LomoUser(lomo, data["user"])

        self.lens = LomoLens(lomo, data["lens"]) if data["lens"] else None
        self.tags = [LomoTag(lomo, tag) for tag in data["tags"]]


class AsyncLomoPhoto(BaseLomoPhoto):
    """
    An asynchronous photo object from Lomography, containing all the necessary information
    about a photo. This class contains the camera, film, user, lens, tags, and
    images associated with the photo.

    :ivar id: The unique identifier for the photo.
    :vartype id: int

    :ivar title: The title of the photo.
    :vartype title: Optional[str]

    :ivar description: The description of the photo.
    :vartype description: Optional[str]

    :ivar url: The URL of the photo.
    :vartype url: str

    :ivar camera: The camera used to take the photo.
    :vartype camera: Optional[AsyncLomoCamera]

    :ivar film: The film used to take the photo.
    :vartype film: Optional[AsyncLomoFilm]

    :ivar user: The user who uploaded the photo.
    :vartype user: AsyncLomoUser

    :ivar small: The small version of the photo.
    :vartype small: LomoPhotoImage

    :ivar large: The large version of the photo.
    :vartype large: LomoPhotoImage

    :ivar asset_hash: The hash of the photo asset.
    :vartype asset_hash: str

    :ivar asset_width: The width of the photo asset.
    :vartype asset_width: int

    :ivar asset_height: The height of the photo asset.
    :vartype asset_height: int

    :ivar asset_ratio: The aspect ratio of the photo asset.
    :vartype asset_ratio: float

    :ivar asset_preview: The preview of the photo asset.
    :vartype asset_preview: str

    :ivar lens: The lens used to take the photo.
    :vartype lens: Optional[AsyncLomoLens]

    :ivar tags: The tags associated with the photo.
    :vartype tags: List[AsyncLomoTag]
    """

    lomo: AsyncLomography

    camera: Optional[AsyncLomoCamera]
    film: Optional[AsyncLomoFilm]
    user: AsyncLomoUser

    lens: Optional[AsyncLomoLens]
    tags: List[AsyncLomoTag]  # type: ignore

    def __init__(self, lomo: AsyncLomography, data: PhotoDict):
        """
        :param lomo: The AsyncLomography instance
        :type lomo: AsyncLomography
        :param data: The photo data, fetched directly from the API
        :type data: PhotoDict
        """

        super().__init__(lomo, data)

        self.camera = AsyncLomoCamera(lomo, data["camera"]) if data["camera"] else None
        self.film = AsyncLomoFilm(lomo, data["film"]) if data["film"] else None
        self.user = AsyncLomoUser(lomo, data["user"])

        self.lens = AsyncLomoLens(lomo, data["lens"]) if data["lens"] else None
        self.tags = [AsyncLomoTag(lomo, tag) for tag in data["tags"]]

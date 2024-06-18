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

    lomo: Lomography

    camera: Optional[LomoCamera]
    film: Optional[LomoFilm]
    user: LomoUser

    lens: Optional[LomoLens]
    tags: List[LomoTag]  # type: ignore

    def __init__(self, lomo: Lomography, data: PhotoDict):
        super().__init__(lomo, data)

        self.camera = LomoCamera(lomo, data["camera"]) if data["camera"] else None
        self.film = LomoFilm(lomo, data["film"]) if data["film"] else None
        self.user = LomoUser(lomo, data["user"])

        self.lens = LomoLens(lomo, data["lens"]) if data["lens"] else None
        self.tags = [LomoTag(lomo, tag) for tag in data["tags"]]


class AsyncLomoPhoto(BaseLomoPhoto):

    lomo: AsyncLomography

    camera: Optional[AsyncLomoCamera]
    film: Optional[AsyncLomoFilm]
    user: AsyncLomoUser

    lens: Optional[AsyncLomoLens]
    tags: List[AsyncLomoTag]  # type: ignore

    def __init__(self, lomo: AsyncLomography, data: PhotoDict):
        super().__init__(lomo, data)

        self.camera = AsyncLomoCamera(lomo, data["camera"]) if data["camera"] else None
        self.film = AsyncLomoFilm(lomo, data["film"]) if data["film"] else None
        self.user = AsyncLomoUser(lomo, data["user"])

        self.lens = AsyncLomoLens(lomo, data["lens"]) if data["lens"] else None
        self.tags = [AsyncLomoTag(lomo, tag) for tag in data["tags"]]

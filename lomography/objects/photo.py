from __future__ import annotations

# Typing
from lomography.api.types import AssetsDict, PhotoDict
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from lomography.base import Lomography

from lomography.objects import LomoPhotoImage, LomoCamera, LomoFilm, LomoUser


class LomoPhoto:

    lomo: Lomography

    id: int

    title: Optional[str]
    description: Optional[str]
    url: str

    camera: Optional[LomoCamera]
    film: Optional[LomoFilm]
    user: LomoUser

    small: LomoPhotoImage
    large: LomoPhotoImage

    # Additional info about the asset, unchanged and unfiltered from the API
    asset_hash: str
    asset_width: int
    asset_height: int
    asset_ratio: float
    asset_preview: str

    def __init__(self, lomo: Lomography, data: PhotoDict):

        self.lomo = lomo
        self._data = data

        self.id = data["id"]
        # If the title is empty (falsely string), then set to null
        self.title = data["title"] if data["title"] else None
        self.description = data["description"] if data["description"] else None

        self.url = data["url"]

        self.small = LomoPhotoImage(data["assets"]["small"])
        self.large = LomoPhotoImage(data["assets"]["large"])

        self.camera = (
            LomoCamera(lomo, data["camera"])
            if data["camera"] and data["camera"] != "None"
            else None
        )

        self.film = (
            LomoFilm(lomo, data["film"])
            if data["film"] and data["film"] != "None"
            else None
        )

        self.user = LomoUser(lomo, data["user"])

        self.asset_hash = data["asset_hash"]
        self.asset_width = data["asset_width"]
        self.asset_height = data["asset_height"]
        self.asset_ratio = data["asset_ratio"]
        self.asset_preview = data["asset_preview"]

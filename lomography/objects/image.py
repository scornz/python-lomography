# Typing
from lomography.api.types import ImageDict, PhotoImageDict


class LomoImage:
    """A class representing an image. This is a generic, base class for all
    image objects. It can represent a user avatars, actual photo assets, etc."""

    url: str
    width: int
    height: int

    def __init__(self, data: ImageDict):
        self.url = data["url"]
        self.width = data["width"]
        self.height = data["height"]


class LomoPhotoImage(LomoImage):
    """A class representing a photo image. This is associated with a LomoPhoto,
    and usually fits into the `small` and `large` attributes of a LomoPhoto object.
    This is normally not a user profile picture, but an actual asset."""

    ratio: float
    filename: str

    def __init__(self, data: PhotoImageDict):
        super().__init__(data)
        self.ratio = data["ratio"]
        self.filename = data["filename"]

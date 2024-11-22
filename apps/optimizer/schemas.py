from ninja import Schema
from typing import Literal, Optional

class ImageUploadSchema(Schema):
    img: str
    mode: Optional[Literal["Sync", "Async"]] = "Sync"
    format: Optional[Literal["jpeg", "png", "webp", 'jpg']] = "webp"
    compression: Optional[int] = 50
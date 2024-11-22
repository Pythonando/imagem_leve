# Strategy
from abc import ABC, abstractmethod
from PIL import ImageFile, Image
from pathlib import Path
from .exceptions import NotImage
from io import BytesIO
from typing import Any, List

variedade: List[Any]


class ImageOptimizerTypesStrategy(ABC):
    @abstractmethod
    def optimize(self, img: ImageFile, quality: int):
        ...


class WebpPILOptimizer(ImageOptimizerTypesStrategy):
    def optimize(self, img: ImageFile, quality: int):
        output = BytesIO()
        img.save(output, 'webp', optimize=True, quality=quality)
        return output


class ImageOptimizer:
    def __init__(
        self,
        input_path: str,
        compression: int,
        optimizer: ImageOptimizerTypesStrategy,
    ):
        self.input_path = input_path
        self.compression = compression
        self.optimizer = optimizer
        self.img = self._open_image()

    def optimize(self):
        return self.optimizer.optimize(img=self.img, quality=self.quality)

    def _open_image(self):
        try:
            img = Image.open(self.input_path)
            img.verify()
            return Image.open(self.input_path)
        except:
            raise NotImage(self.input_path)

    @property
    def quality(self):
        return 1 if (100 - self.compression) == 0 else (100 - self.compression)


'''from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


x = ImageOptimizer(BASE_DIR / 'img1.png', 80, WebpPILOptimizer())
print(x.optimize())
'''
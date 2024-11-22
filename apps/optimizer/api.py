from ninja import Router
from imagem_leve.auth import ApiKey
from .schemas import ImageUploadSchema
import base64
from .models import OptimizingImages
from django.core.files.base import ContentFile
from django.conf import settings
from image_optimize.app import ImageOptimizer, WebpPILOptimizer
from .choices import *
from datetime import datetime
from .tasks import optimizer_images_async

optimizer_router = Router()

@optimizer_router.post('imagem/', auth=ApiKey())
def optimize_image(request, image_upload: ImageUploadSchema):

    img = base64.b64decode(image_upload.img)

    content = ContentFile(img, name=f"optmizing.{image_upload.format}")

    image_instance = OptimizingImages(
        user=request.auth,
        default_image=content,
        mode=image_upload.mode,
        format=image_upload.format,
        compression=image_upload.compression
    )
    image_instance.save()

    if image_upload.mode.upper() == 'SYNC':
        file_path = settings.MEDIA_ROOT / image_instance.default_image.name if settings.DEBUG else image_instance.default_image.url
        webp_pil_optimizer = ImageOptimizer(file_path, image_upload.compression, WebpPILOptimizer())
        
        img_result = webp_pil_optimizer.optimize().getvalue()

        name = f'optimized.{image_upload.format}'
        image_instance.optimized_image.save(
            name,
            ContentFile(img_result, name=name),
        )
        image_instance.status = ImageStatus.PROCESSED
        image_instance.complete_at = datetime.now()
        image_instance.save()

        return 200, {'encoded_image': base64.b64encode(img_result).decode(), 'image_url': image_instance.optimized_image.url, 'uuid': image_instance.id}
    else:
        optimizer_images_async.delay(image_instance.id)
        return 200, {'status': 'Imagem em processamento', 'uuid': image_instance.id}
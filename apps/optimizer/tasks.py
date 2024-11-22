from celery import shared_task
from .models import OptimizingImages, WebhookLog
from django.core.files.base import ContentFile
from django.conf import settings
from image_optimize.app import ImageOptimizer, WebpPILOptimizer
from .choices import *
from datetime import datetime
import requests
import json
import base64

def send_webhook(payload, url):
    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, data=json.dumps(payload), headers=headers)
    return response

@shared_task(bind=True, max_retries=10, retry_backoff=True)
def optimizer_images_async(self, uuid):
    try:
        image_instance = OptimizingImages.objects.get(id=uuid)

        image_instance.status = ImageStatus.PROCESSING
        image_instance.save()

        file_path = settings.MEDIA_ROOT / image_instance.default_image.name if settings.DEBUG else image_instance.default_image.url
        webp_pil_optimizer = ImageOptimizer(file_path, image_instance.compression, WebpPILOptimizer())
        
        img_result = webp_pil_optimizer.optimize().getvalue()

        name = f'optimized.{image_instance.format}'
        image_instance.optimized_image.save(
            name,
            ContentFile(img_result, name=name),
        )
        image_instance.status = ImageStatus.PROCESSED
        image_instance.complete_at = datetime.now()
        image_instance.save()

        payload = {'encoded_image': base64.b64encode(img_result).decode(), 'image_url': image_instance.optimized_image.url, 'uuid': str(image_instance.id)}
        
        response = send_webhook(payload, image_instance.user.webhook)

        log = WebhookLog(
            user=image_instance.user,
            url=image_instance.user.webhook,
            status=int(response.status_code),
            request=payload,
            response=response.text
        )
        log.save()

        return {'status': 'Done'}
    except Exception as e:
        raise self.retry(exc=e, countdow=self.request.retries**2)
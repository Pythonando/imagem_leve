from django.db import models

class ImageStatus(models.TextChoices):
    AWAITING = "awaiting", "Aguardando Processamento"
    PROCESSING = "processing", "Em Processamento"
    PROCESSED = "processed", "Processado"

class ProcessingMode(models.TextChoices):
    SYNC = "Sync", "Síncrono"
    ASYNC = "Async", "Assíncrono"

class ImageFormat(models.TextChoices):
    JPEG = "jpeg", "JPEG"
    PNG = "png", "PNG"
    WEBP = "webp", "WEBP"
    JPG = "jpg", "JPG"
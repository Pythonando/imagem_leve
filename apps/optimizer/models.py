from django.db import models
from accounts.models import User
import secrets
from hashlib import sha256
import uuid
from .choices import *

class AccessTokens(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=64)
    create_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = self.gen_token(self.user.id)
        super().save(*args, **kwargs)

    @classmethod
    def gen_token(cls, user_id):
        unique_string = f'{user_id}-{secrets.token_hex(16)}'
        return sha256(unique_string.encode()).hexdigest()

class OptimizingImages(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    default_image = models.ImageField(upload_to='default_images')
    optimized_image = models.ImageField(upload_to='optimized_image', null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=ImageStatus.choices,
        default=ImageStatus.AWAITING,
    )
    mode = models.CharField(
        max_length=10,
        choices=ProcessingMode.choices,
        default=ProcessingMode.SYNC,
    )
    format = models.CharField(
        max_length=10,
        choices=ImageFormat.choices,
        default=ImageFormat.JPEG,
    )
    compression = models.IntegerField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    complete_at = models.DateTimeField(null=True, blank=True)

class WebhookLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.URLField()
    status = models.IntegerField()
    request = models.JSONField()
    response = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)
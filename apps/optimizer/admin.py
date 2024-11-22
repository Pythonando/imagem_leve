from django.contrib import admin
from .models import AccessTokens, OptimizingImages, WebhookLog

admin.site.register(AccessTokens)
admin.site.register(OptimizingImages)
admin.site.register(WebhookLog)

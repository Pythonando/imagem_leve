from django.contrib import admin
from .models import CreditCards, ProcessedWebhook

# Register your models here.
admin.site.register(CreditCards)
admin.site.register(ProcessedWebhook)
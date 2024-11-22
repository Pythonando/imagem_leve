from django.db import models
from accounts.models import User

# Create your models here.
class CreditCards(models.Model):
    last_numbers_credit_card = models.CharField(max_length=4)
    credit_card_brand = models.CharField(max_length=50)
    credit_card_token = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.user} - {self.last_numbers_credit_card}'


class ProcessedWebhook(models.Model):
    event_id = models.CharField(max_length=255, unique=True)
    invoice_id = models.CharField(max_length=255, unique=True)
    event = models.CharField(max_length=50)
    payload = models.JSONField()
    processed_at = models.DateTimeField(auto_now_add=True)

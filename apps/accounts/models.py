from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager
from .model_validators import validate_cpf_cnpj

# Create your models here.
class User(AbstractUser):
    username = models.CharField(max_length=150, null=True, blank=True)
    email = models.EmailField(unique=True)

    customer_id = models.CharField(max_length=50, null=True, blank=True)
    cpf_cnpj = models.CharField(
        max_length=50, null=True, blank=True, validators=[validate_cpf_cnpj]
    )
    balance = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self) -> str:
        return self.email

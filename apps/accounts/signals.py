from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User
from payments.asaas.asaas_payment import AsaasCustomer


@receiver(post_save, sender=User)
def create_customer(sender, instance, created, **kwargs):
    if created:
        asaas = AsaasCustomer()
        response = asaas.create_customer(
            name=instance.first_name, cpfCnpj=instance.cpf_cnpj
        )
        instance.customer_id = response['id']
        instance.save()

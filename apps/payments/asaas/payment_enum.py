from enum import Enum


class BillingType(Enum):
    BOLETO = 'BOLETO'
    PIX = 'PIX'
    CREDIT_CARD = 'CREDIT_CARD'

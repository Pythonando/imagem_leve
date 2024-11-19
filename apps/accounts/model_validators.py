from django.db import models
from django.core.exceptions import ValidationError
import re


def validate_cpf_cnpj(value):
    def is_valid_cpf(cpf):
        if cpf == cpf[0] * len(cpf):
            return False

        for i in range(9, 11):
            soma = sum(int(cpf[j]) * ((i + 1) - j) for j in range(i))
            digito = (soma * 10) % 11
            if digito == 10:
                digito = 0
            if digito != int(cpf[i]):
                return False
        return True

    def is_valid_cnpj(cnpj):
        if len(cnpj) < 14:
            return False
        if cnpj == cnpj[0] * len(cnpj):
            return False

        pesos = [6, 7, 8, 9, 2, 3, 4, 5]
        for i in range(12, 14):
            soma = sum(
                int(cnpj[j]) * pesos[(j - 12) % len(pesos)] for j in range(i)
            )
            digito = soma % 11
            digito = 0 if digito < 2 else 11 - digito
            if digito != int(cnpj[i]):
                return False
        return True

    if value:
        # Remove caracteres não numéricos
        value = re.sub(r'\D', '', value)
        if len(value) < 11:
            raise ValidationError('CPF/CNPJ inválido')

        if not is_valid_cpf(value) and not is_valid_cnpj(value):
            raise ValidationError('CPF/CNPJ inválido')

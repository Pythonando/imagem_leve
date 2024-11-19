# from django.conf import settings
from urllib.parse import urlencode, urljoin
import requests
from .payments_dataclasses import CreditCard, creditCardHolderInfo, Billing
from dataclasses import asdict
from .payment_enum import BillingType
from datetime import date, timedelta


class AsaasBasePayment:
    def __init__(self):
        self._BASE_URL = 'https://sandbox.asaas.com/api/v3/'
        self._API_KEY = '$aact_YTU5YTE0M2M2N2I4MTliNzk0YTI5N2U5MzdjNWZmNDQ6OjAwMDAwMDAwMDAwMDAwNzc4Mjk6OiRhYWNoXzdhMDIwOTAxLTFmYjgtNDYwYi1hYmE3LTZkYzE0ZWVkOTlkNg=='

        """self._API_KEY = settings.API_KEY_ASAAS
        
        self._BASE_URL = (
            'https://api.asaas.com/'
            if not settings.DEBUG
            else 'https://sandbox.asaas.com/api/v3/'
        )"""

    def _send_request(
        self,
        path,
        method='GET',
        body=None,
        headers={},
        params_url={},
        use_api_key=True,
    ):
        method.upper()
        url = self._mount_url(path, params_url)

        if not isinstance(headers, dict):
            headers = {}

        if use_api_key:
            headers['access_token'] = str(self._API_KEY)

        headers['Content-Type'] = 'application/json'

        match method:
            case 'GET':
                response = requests.get(url, headers=headers, json=body)
            case 'POST':
                response = requests.post(url, headers=headers, json=body)
            case 'PUT':
                response = requests.put(url, headers=headers, json=body)
            case 'DELETE':
                response = requests.delete(url, headers=headers, json=body)

        return response

    def _mount_url(self, path, params_url):
        if isinstance(params_url, dict):
            parameters = urlencode(params_url)

        url = urljoin(self._BASE_URL, path)
        if parameters:
            url = url + '?' + parameters

        return url


class AsaasCustomer(AsaasBasePayment):
    def create_customer(self, **kwargs):
        """Possibilidades de parametros para kwargs no link:
        https://docs.asaas.com/reference/criar-novo-cliente
        """
        if 'name' not in kwargs.keys() or 'cpfCnpj' not in kwargs.keys():
            raise KeyError('name e cpfCnpj são campos obrigatorios')

        return self._send_request(
            path='customers', method='POST', body=kwargs
        ).json()

    def list_customer(self, **kwargs):
        """kwargs representam os params_url confira as possibilidades em:
        https://docs.asaas.com/reference/listar-clientes
        """

        return self._send_request(path='customers', params_url=kwargs).json()

    def get_customer(self, customer_id):
        return self._send_request(path=f'customers/{customer_id}').json()


class AsaasInvoice(AsaasBasePayment):
    def tokenize_credit_card(
        self,
        customer_id: str,
        credit_card: CreditCard,
        credit_card_holder_info: creditCardHolderInfo,
        remote_ip,
    ):
        payload = {
            'customer': customer_id,
            'creditCard': asdict(credit_card),
            'creditCardHolderInfo': asdict(credit_card_holder_info),
            'remoteIp': remote_ip,
        }
        return self._send_request(
            path=f'creditCard/tokenizeCreditCard', method='POST', body=payload
        ).json()

    def create_invoice(self, billing: Billing):
        return self._send_request(
            path='payments', method='POST', body=asdict(billing)
        ).json()

    def get_invoice(self, invoice_id):
        return self._send_request(path=f'payments/{invoice_id}').json()

    def pay_invoice(
        self,
        invoice_id,
        credit_card: CreditCard,
        credit_card_holder_info: creditCardHolderInfo,
        credit_card_token=None,
    ):
        payload = {
            'creditCard': asdict(credit_card),
            'creditCardHolderInfo': asdict(credit_card_holder_info),
            'creditCardToken': credit_card_token,
        }
        return self._send_request(
            path=f'payments/{invoice_id}/payWithCreditCard',
            method='POST',
            body=payload,
        )

    def get_pix_invoice(self, invoice_id):
        return self._send_request(
            path=f'payments/{invoice_id}/pixQrCode'
        ).json()


asaas = AsaasInvoice()

# response = asaas.get_customer('cus_000006350645')

"""response = asaas.tokenize_credit_card(
    'cus_000006350645',
    CreditCard('Caio Sampaio', '0000000000000000', '12', '25', '000'),
    creditCardHolderInfo(
        'Caio Sampaio',
        'caio@pythonando.com.br',
        '47.836.553/0001-42',
        '14401059',
        '00',
        '16992805442',
    ),
    '127.0.0.1',
)"""

# due_date = (date.today() + timedelta(days=1)).strftime('%Y-%m-%d')
# billing = Billing('cus_000006350645', BillingType.BOLETO.value, 20, due_date)
# response = asaas.create_invoice(billing)
# response = asaas.get_invoice('pay_55eh4kh1kni09p37')
"""response = asaas.pay_invoice(
    'pay_f394n34cfz4kgkai',
    CreditCard('Caio Sampaio', '0000000000000000', '12', '25', '000'),
    creditCardHolderInfo(
        'Caio Sampaio',
        'email@email.com.br',
        '47.836.553/0001-42',
        '14401059',
        '00',
        '00000000000',
    ),
)"""
#response = asaas.get_pix_invoice('pay_wnlwhmcy0279z3q7')

#print(response)

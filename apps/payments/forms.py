from django import forms

TAILWIND_INPUT = 'block w-full rounded-md border-0 px-2 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm/6'

class CheckoutCreditCard(forms.Form):
    holder_name = forms.CharField(
        label="Nome impresso no cartão",
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': TAILWIND_INPUT,
            'placeholder': 'Nome do titular do cartão',
        })
    )
    card_number = forms.CharField(
        label="Número do Cartão",
        max_length=19,
        widget=forms.TextInput(attrs={
            'class': TAILWIND_INPUT,
            'placeholder': '1234 5678 1234 5678',
            'data-mask': 'card',
            'autocomplete': 'cc-number'
        })
    )
    expiration_date = forms.CharField(
        label="Data de Expiração (MM/YY)",
        max_length=5,  
        widget=forms.TextInput(attrs={
            'class': TAILWIND_INPUT,
            'placeholder': 'MM/YY',
            'data-mask': 'expiration',
            'autocomplete': 'cc-exp'
        })
    )
    cvc = forms.CharField(
        label="CVC",
        max_length=4,
        widget=forms.TextInput(attrs={
            'class': TAILWIND_INPUT,
            'placeholder': 'CVC',
            'data-mask': 'cvc',
        })
    )
    postal_code = forms.CharField(
        label="CEP",
        max_length=9,
        widget=forms.TextInput(attrs={
            'class': TAILWIND_INPUT,
            'placeholder': '12345-678',
            'data-mask': 'cep',
        })
    )
    house_number = forms.CharField(
        label="Número da Casa",
        max_length=10,
        widget=forms.TextInput(attrs={
            'class': TAILWIND_INPUT,
            'placeholder': 'Número da Casa',
        })
    )
    phone = forms.CharField(
        label="Telefone",
        max_length=15,
        widget=forms.TextInput(attrs={
            'class': TAILWIND_INPUT,
            'placeholder': '(99) 99999-9999',
            'data-mask': 'phone',
        })
    )
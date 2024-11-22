from django.contrib.auth import forms
from .models import User


class UserChangeForm(forms.UserChangeForm):
    class Meta(forms.UserChangeForm.Meta):
        model = User


class UserCreationForm(forms.UserCreationForm):
    class Meta(forms.UserCreationForm.Meta):
        model = User
        fields = ('email', 'cpf_cnpj', 'first_name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placelholders = {
            'password1': 'Digite sua senha',
            'password2': 'Confirmar senha',
        }
        for field_name, field in self.fields.items():
            placelholder = placelholders.get(
                field_name, f'Digite seu {field.label}'
            )
            field.widget.attrs.update(
                {
                    'class': 'block w-full rounded-md border-0 px-2 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm/6',
                    'placeholder': placelholder,
                }
            )

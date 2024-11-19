from django.contrib import admin
from .models import User
from django.contrib.auth import admin as admin_auth_django
from .forms import UserChangeForm, UserCreationForm


@admin.register(User)
class UserAdmin(admin_auth_django.UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    model = User
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    fieldsets = (
        (
            'Autenticação',
            {
                'fields': (
                    'email',
                    'password',
                )
            },
        ),
        (
            'Pagamento',
            {
                'fields': (
                    'balance',
                    'customer_id',
                ),
            },
        ),
        
        (
            'Geral',
            {
                'fields': (
                    'first_name',
                    'cpf_cnpj',
                    'last_login',
                    'date_joined',
                    'is_staff',
                    'is_superuser',
                )
            },
        ),
    )

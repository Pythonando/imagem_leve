from django.urls import path
from . import views

urlpatterns = [
   path('gerar_token/', views.GenerateToken.as_view(), name="generate_token")
]

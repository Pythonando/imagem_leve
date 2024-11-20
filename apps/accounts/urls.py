from django.urls import path
from . import views

urlpatterns = [
    path('cadastro/', views.Register.as_view(), name='register'),
    path('perfil/', views.Perfil.as_view(), name='perfil')
]

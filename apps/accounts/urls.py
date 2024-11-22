from django.urls import path
from . import views

urlpatterns = [
    path('cadastro/', views.Register.as_view(), name='register'),
    path('perfil/', views.Perfil.as_view(), name='perfil'),
    path('set_webhook/', views.SetWebhook.as_view(), name='set_webhook'),
    path('ver_log/<int:id>', views.ViewLog.as_view(), name="view_log")
]

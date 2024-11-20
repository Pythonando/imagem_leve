from django.urls import path
from . import views

urlpatterns = [
    path('step-1/', views.Step1.as_view(), name="step1"),
    path('step-2/<str:invoice_id>', views.Step2.as_view(), name="step2"),
    path('webhook/', views.Webhook.as_view(), name="webhook")
]

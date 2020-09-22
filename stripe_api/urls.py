from django.urls import path
from . import views

app_name = 'stripe_api'

urlpatterns = [
    path('config', views.config),
    path('create-checkout-session/<str:mode>/<str:stripePriceId>', views.create_checkout_session), 
    path('webhook', views.webhook), 
]
from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('check-user-pass/<str:password>', views.checkUserPass),
    path('subscriptions', views.subscriptions, name='subscriptions'),
    path('subscriptions/activated', views.succesfulSubscription),
]
"""RanksAnalyzer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
"""
# Django imports
from django.conf.urls import include, url
from django.urls import path
from django.contrib import admin
from django.contrib.auth import views as auth_views
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from users import views as userViews

urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/account', userViews.account, name='account'),
    path('accounts/password/change/', login_required(userViews.CustomPasswordChangeView.as_view()), name="account_change_password"),
    path('accounts/', include('allauth.urls')),
    path('users/', include('users.urls', namespace = 'users')),
    path('analyze/', include('analyze.urls', namespace = 'analyze')),
    path('tools/', include('tools.urls', namespace = 'tools')),
    path('stripe_api/', include('stripe_api.urls', namespace = 'stripe_api')),
    
    # enable the admin interface
    url(r'^amministra/', admin.site.urls),
]

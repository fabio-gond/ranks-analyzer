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


urlpatterns = [
    # Examples:
    # url(r'^blog/', include('blog.urls', namespace='blog')),
    path('', views.index, name='index'),
    
    url(r'^login/$', LoginView.as_view(template_name='core/login.html'), name='core_login'),
    url(r'^logout/$', LogoutView.as_view(), name='core_logout'),
    path('accounts/', include('allauth.urls')),
    
    #url(r'account/', include('django.contrib.auth.urls')),

    # provide the most basic login/logout functionality
    #url(r'^login/$', auth_views.login,
     #   {'template_name': 'core/login.html'}, name='core_login'),
    #url(r'^logout/$', auth_views.logout, name='core_logout'),

    # enable the admin interface
    url(r'^admin/', admin.site.urls),
]

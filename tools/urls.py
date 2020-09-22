from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'tools'

urlpatterns = [
    path('', views.index, name='index'),
    path('system_logs', views.system_logs, name='system_logs'),
    path('load_scraped_ranks', views.loadScrapedRanks, name='load_scraped_ranks'),
]
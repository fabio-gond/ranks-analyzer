from django.urls import path

from . import views

app_name = 'analyze'

urlpatterns = [
    path('', views.index, name='index'),
    path('products', views.products, name='products'),
    path('products/current_products_model', views.downloadCurrentProductsModel),
    path('products/check_products_file', views.checkProductsFile),
    path('products/upload_keywords_file', views.uploadKeywordsFile),
    path('ranks_graph', views.amazonRanksGraph, name='ranks_graph'),
    path('api/get_product_variants/<int:pk>', views.apiGetProductVariant),
]
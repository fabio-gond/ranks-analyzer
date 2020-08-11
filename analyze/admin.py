from django.contrib import admin
from .models import Product,ProductParent

""" class SellerAdmin(admin.ModelAdmin):
    list_display = ('name', 'platform', 'created_at')
    list_filter = ('platform',) """

class ProductAdmin(admin.ModelAdmin):
    list_display = ('code', 'asin', 'parent', 'user','created_at')
    list_filter = ('user' , 'parent',)

class ProductParentAdmin(admin.ModelAdmin):
    list_display = ('code', 'asin', 'user','created_at')
    list_filter = ('user', )


admin.site.register(ProductParent,ProductParentAdmin)
admin.site.register(Product, ProductAdmin)
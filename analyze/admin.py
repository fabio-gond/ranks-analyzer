from django.contrib import admin
from .models import Product,ProductParent,Seller

class SellerAdmin(admin.ModelAdmin):
    list_display = ('name', 'platform', 'created_at')
    list_filter = ('platform',)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('code', 'asin', 'parent', 'seller','created_at')
    list_filter = ('seller' , 'parent',)

class ProductParentAdmin(admin.ModelAdmin):
    list_display = ('code', 'asin', 'seller','created_at')
    list_filter = ('seller', )


admin.site.register(ProductParent,ProductParentAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Seller, SellerAdmin)
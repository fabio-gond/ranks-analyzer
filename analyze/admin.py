from django.contrib import admin
from .models import Product,ProductParent, Keyword,AmazonRank


class ProductAdmin(admin.ModelAdmin):
    list_display = ('code', 'asin', 'parent', 'user','created_at')
    list_filter = ('user' , 'parent',)

class ProductParentAdmin(admin.ModelAdmin):
    list_display = ('code', 'asin', 'user','created_at')
    list_filter = ('user', )

class KeywordAdmin(admin.ModelAdmin):
    model = Keyword
    list_display = ('keyword', 'product', 'marketplace', 'get_product_pk')
    list_filter = ('marketplace', )
    def get_product_pk(self, obj):
        return obj.product.pk

class AmazonRankAdmin(admin.ModelAdmin):
    list_display = ('keyword', 'day', 'indexed','rank','amazon_choice')
    list_filter = ('amazon_choice',)



admin.site.register(ProductParent,ProductParentAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Keyword, KeywordAdmin)
admin.site.register(AmazonRank, AmazonRankAdmin)
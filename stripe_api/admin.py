from django.contrib import admin
from .models import Plan, OneTimeProduct

class PlanAdmin(admin.ModelAdmin):
    list_display = ('name','code','kwds_qty', 'days_step','interval','price')
class OneTimeProductAdmin(admin.ModelAdmin):
    list_display = ('name','code','kwds_qty', 'days_step','interval','price')



admin.site.register(Plan,PlanAdmin)
admin.site.register(OneTimeProduct,OneTimeProductAdmin)

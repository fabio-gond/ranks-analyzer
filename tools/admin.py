from django.contrib import admin
from .models import Log

class LogAdmin(admin.ModelAdmin):
    list_display = ('log', 'user', 'context', 'severity','time')
    list_filter = ('severity' , 'context', 'user')

admin.site.register(Log, LogAdmin)



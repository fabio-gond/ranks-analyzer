from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'username',]
    fieldsets = UserAdmin.fieldsets + ( (('Other'), {'fields': ('platform','other','plan','plan_current_checkout','plan_paid_until','stripe_email','stripe_cust_id','stripe_checkout_session_id')}), )
    """ fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (('Personal Info'), {'fields': ('first_name', 'last_name', 'email','friends')}),
        (('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (('Important Dates'), {'fields': ('last_login', 'date_joined',)}),
    ) """

admin.site.register(CustomUser, CustomUserAdmin)

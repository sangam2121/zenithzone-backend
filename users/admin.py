from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser, OTPstore
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group

from .forms import CustomUserCreationForm, CustomUserChangeForm


# Register your models here.

class UserAdmin(BaseUserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    # list_display = ['email', 'username', 'age', 'is_staff', ]
    list_display = ['email', 'first_name', 'last_name', 'user_type', ]
    fieldsets = (
        (None, {'fields': ('email', 'password',
         'first_name', 'last_name', 'user_type', 'phone', 'address', 'bio',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff',
         'is_superuser',)}),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {'fields': ('email', 'password1', 'password2',
         'first_name', 'last_name', 'user_type', 'phone', 'address', 'bio',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff',
         'is_superuser', )}),
    )

    ordering = ('email',)
    list_filter = ('email', 'first_name', 'last_name', 'user_type', )
    filter_horizontal = ()


admin.site.register(CustomUser, UserAdmin)
admin.site.unregister(Group)
admin.site.register(OTPstore)
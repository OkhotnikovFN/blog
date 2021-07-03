from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from app_users import models, forms


@admin.register(models.CustomUser)
class AdminCustomUser(UserAdmin):
    """Регистрация раширенной модели пользователя в панели администрирования"""

    readonly_fields = ['slug']
    form = forms.AdminCustomUserChangeForm
    add_form = forms.CustomUserCreationForm

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name',
                                         'last_name', 'email', 'telephone_number', 'user_photo', 'slug')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'telephone_number', 'password1', 'password2'),
        }),
    )

    list_display = ('username', 'email', 'telephone_number', 'first_name', 'last_name', 'is_staff')

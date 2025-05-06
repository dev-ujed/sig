from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    # Campos que se mostrarán en la vista de lista
    list_display = ('email', 'username', 'matricula', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_active')

    # Campos para el formulario de detalle del admin
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Información personal'), {'fields': ('username', 'matricula', 'name', 'last_name')}),
        (_('Permisos'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Fechas importantes'), {'fields': ('last_login',)}),
    )

    # Campos al crear un nuevo usuario desde el admin
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'matricula', 'name', 'last_name', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )

    search_fields = ('email', 'username', 'matricula')
    ordering = ('email',)

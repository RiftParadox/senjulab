from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CuponDescuento, Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ('username', 'email', 'telefono', 'sellos_tarjeta', 'is_staff', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('Información SenjuLab', {'fields': ('telefono', 'sellos_tarjeta')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Información SenjuLab', {'fields': ('email', 'telefono', 'sellos_tarjeta')}),
    )


@admin.register(CuponDescuento)
class CuponDescuentoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'usuario', 'porcentaje_descuento', 'usado', 'fecha_creacion')
    list_filter = ('usado',)
    search_fields = ('codigo', 'usuario__username', 'usuario__email')
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Usuario(AbstractUser):
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    sellos_tarjeta = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return f"{self.username} (Sellos: {self.sellos_tarjeta}/5)"


class CuponDescuento(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cupones'
    )
    codigo = models.CharField(max_length=50, unique=True)
    porcentaje_descuento = models.PositiveIntegerField(
        default=10,
        validators=[MinValueValidator(1), MaxValueValidator(100)]
    )
    usado = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_uso = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = 'Cupón de Descuento'
        verbose_name_plural = 'Cupones de Descuento'
        ordering = ['-fecha_creacion']

    def __str__(self):
        estado = 'Usado' if self.usado else 'Disponible'
        return f"{self.codigo} ({self.porcentaje_descuento}%) - {self.usuario.username} [{estado}]"
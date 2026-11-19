import uuid

from django.db import transaction
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from clientes.models import CuponDescuento, Usuario


@transaction.atomic
def validar_y_consumir_cupon(
    usuario: Usuario, codigo_cupon: str | None
) -> CuponDescuento:
    if not isinstance(codigo_cupon, str):
        raise ValidationError('El código del cupón es obligatorio.')

    codigo_normalizado = codigo_cupon.strip().upper()
    if not codigo_normalizado:
        raise ValidationError('El código del cupón es obligatorio.')

    try:
        cupon = CuponDescuento.objects.select_for_update().get(
            codigo__iexact=codigo_normalizado,
            usuario=usuario,
            usado=False,
        )
    except CuponDescuento.DoesNotExist as exc:
        raise ValidationError('El cupón no existe o ya fue usado.') from exc

    cupon.usado = True
    cupon.fecha_uso = timezone.now()
    cupon.save(update_fields=['usado', 'fecha_uso'])
    return cupon


@transaction.atomic
def otorgar_sello_por_entrega(usuario: Usuario) -> CuponDescuento | None:
    user = Usuario.objects.select_for_update().get(pk=usuario.pk)
    user.sellos_tarjeta += 1

    if user.sellos_tarjeta >= 5:
        user.sellos_tarjeta = 0
        codigo = uuid.uuid4().hex[:10].upper()
        while CuponDescuento.objects.filter(codigo=codigo).exists():
            codigo = uuid.uuid4().hex[:10].upper()
        cupon = CuponDescuento.objects.create(usuario=user, codigo=codigo)
        user.save(update_fields=['sellos_tarjeta'])
        return cupon

    user.save(update_fields=['sellos_tarjeta'])
    return None

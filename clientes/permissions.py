"""Permisos reutilizables para los recursos de la API."""

from typing import Any

from rest_framework.permissions import BasePermission
from rest_framework.request import Request


def _esta_autenticado(request: Request) -> bool:
    return bool(request.user and request.user.is_authenticated)


def _es_propietario(request: Request, obj: Any) -> bool:
    usuario = request.user
    return _esta_autenticado(request) and (
        obj is usuario
        or obj == usuario
        or getattr(obj, 'usuario', None) == usuario
    )


class EsAdmin(BasePermission):
    """Permite el acceso a usuarios autenticados de staff o superusuarios."""

    def has_permission(self, request: Request, view: Any) -> bool:
        if not _esta_autenticado(request):
            return False
        return bool(request.user.is_staff or request.user.is_superuser)


class EsAdminOEsPropietario(BasePermission):
    """Permite el acceso a staff o al propietario autenticado del objeto."""

    def has_permission(self, request: Request, view: Any) -> bool:
        return _esta_autenticado(request)

    def has_object_permission(
        self, request: Request, view: Any, obj: Any
    ) -> bool:
        if not _esta_autenticado(request):
            return False
        return bool(request.user.is_staff or _es_propietario(request, obj))


class EsPropietario(BasePermission):
    """Permite el acceso únicamente al propietario autenticado del objeto."""

    def has_permission(self, request: Request, view: Any) -> bool:
        return _esta_autenticado(request)

    def has_object_permission(
        self, request: Request, view: Any, obj: Any
    ) -> bool:
        return _es_propietario(request, obj)

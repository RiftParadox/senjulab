from rest_framework import generics, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from clientes.models import CuponDescuento, Usuario
from clientes.permissions import EsAdmin
from clientes.serializers import (
    CuponDescuentoSerializer,
    LoginSerializer,
    PerfilSerializer,
    RegistroSerializer,
    UsuarioAdminSerializer,
)


class RegistroView(generics.CreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = RegistroSerializer
    permission_classes = (AllowAny,)


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)


class RefreshTokenView(TokenRefreshView):
    permission_classes = (AllowAny,)


class MiPerfilView(generics.RetrieveUpdateAPIView):
    serializer_class = PerfilSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ('get', 'patch', 'head', 'options')

    def get_object(self):
        return self.request.user


class MisCuponesView(generics.ListAPIView):
    serializer_class = CuponDescuentoSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        cupones = CuponDescuento.objects.filter(
            usuario=self.request.user
        ).order_by('-fecha_creacion')
        usado = self.request.query_params.get('usado')
        if usado is not None:
            usado_normalizado = usado.lower()
            if usado_normalizado not in ('true', 'false'):
                raise ValidationError(
                    {'usado': 'El valor debe ser true o false.'}
                )
            cupones = cupones.filter(usado=usado_normalizado == 'true')
        return cupones


class UsuariosAdminView(generics.ListAPIView):
    queryset = Usuario.objects.all().order_by('-date_joined')
    serializer_class = UsuarioAdminSerializer
    permission_classes = (EsAdmin,)


class CuponesAdminViewSet(viewsets.ModelViewSet):
    queryset = CuponDescuento.objects.select_related('usuario')
    serializer_class = CuponDescuentoSerializer
    permission_classes = (EsAdmin,)

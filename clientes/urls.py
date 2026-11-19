from django.urls import path

from clientes.views import (
    CuponesAdminViewSet,
    LoginView,
    MiPerfilView,
    MisCuponesView,
    RefreshTokenView,
    RegistroView,
    UsuariosAdminView,
)

urlpatterns = [
    path('registro/', RegistroView.as_view(), name='clientes-registro'),
    path('login/', LoginView.as_view(), name='clientes-login'),
    path('token/refresh/', RefreshTokenView.as_view(), name='clientes-token-refresh'),
    path('me/', MiPerfilView.as_view(), name='clientes-me'),
    path('mis-cupones/', MisCuponesView.as_view(), name='clientes-mis-cupones'),
    path('admin/usuarios/', UsuariosAdminView.as_view(), name='clientes-admin-usuarios'),
    path(
        'admin/cupones/',
        CuponesAdminViewSet.as_view({'get': 'list', 'post': 'create'}),
        name='clientes-admin-cupones-list',
    ),
    path(
        'admin/cupones/<int:pk>/',
        CuponesAdminViewSet.as_view(
            {
                'get': 'retrieve',
                'put': 'update',
                'patch': 'partial_update',
                'delete': 'destroy',
            }
        ),
        name='clientes-admin-cupones-detail',
    ),
]

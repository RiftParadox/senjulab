from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from clientes.models import CuponDescuento, Usuario


class RegistroSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Usuario
        fields = (
            'id',
            'username',
            'email',
            'telefono',
            'sellos_tarjeta',
            'password',
        )
        read_only_fields = ('id', 'sellos_tarjeta')

    def validate(self, attrs):
        email = attrs['email'].strip().lower()
        username = attrs['username'].strip()

        if Usuario.objects.filter(email__iexact=email).exists():
            raise ValidationError({'email': 'Este correo ya está registrado.'})
        if Usuario.objects.filter(username__iexact=username).exists():
            raise ValidationError({'username': 'Este nombre de usuario ya está registrado.'})

        attrs['email'] = email
        attrs['username'] = username
        candidate = Usuario(username=username, email=email)
        try:
            validate_password(attrs['password'], user=candidate)
        except DjangoValidationError as exc:
            raise ValidationError({'password': exc.messages}) from exc
        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data['sellos_tarjeta'] = 0
        return Usuario.objects.create_user(password=password, **validated_data)


class LoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = {
            'id': self.user.pk,
            'username': self.user.username,
            'email': self.user.email,
            'is_staff': self.user.is_staff,
            'sellos_tarjeta': self.user.sellos_tarjeta,
        }
        return data


class PerfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = (
            'id',
            'username',
            'email',
            'telefono',
            'sellos_tarjeta',
            'is_staff',
            'is_active',
        )
        read_only_fields = ('id', 'sellos_tarjeta', 'is_staff', 'is_active')


class CuponDescuentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CuponDescuento
        fields = (
            'id',
            'usuario',
            'codigo',
            'porcentaje_descuento',
            'usado',
            'fecha_creacion',
            'fecha_uso',
        )
        read_only_fields = ('id', 'fecha_creacion')


class UsuarioAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = (
            'id',
            'username',
            'email',
            'telefono',
            'sellos_tarjeta',
            'is_staff',
            'is_active',
            'date_joined',
        )

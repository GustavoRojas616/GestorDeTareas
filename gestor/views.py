from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics, permissions
from .models import Usuario
from .serializers import UsuarioRegistroSerializer, UsuarioPerfilSerializer

class RegistroUsuarioView(generics.CreateAPIView):
    """
    POST /api/usuarios/register/  → crea un nuevo usuario.
    """
    queryset = Usuario.objects.all()
    serializer_class = UsuarioRegistroSerializer
    permission_classes = (permissions.AllowAny,)


class PerfilUsuarioView(generics.RetrieveAPIView):
    """
    GET /api/usuarios/me/  → devuelve los datos del usuario autenticado.
    """
    serializer_class = UsuarioPerfilSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user
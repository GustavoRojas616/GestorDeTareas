from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegistroUsuarioView, PerfilUsuarioView

urlpatterns = [
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('usuarios/register/', RegistroUsuarioView.as_view(), name='usuario_registro'),
    path('usuarios/me/',       PerfilUsuarioView.as_view(),   name='perfil_usuario'),
]
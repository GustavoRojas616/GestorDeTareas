from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegistroUsuarioView, PerfilUsuarioView, TareaListCreateView, TareaDetailView

urlpatterns = [
    # Rutas de autenticación con JWT 
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'), # POST /api/auth/login/: recibe user/pass y devuelve access y refresh tokens
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # POST /api/auth/refresh/: recibe refresh token y devuelve nuevo access token

    # Rutas para registro de usuarios y, solo para usuarios autenticados, los detalles de su perfil 
    path('usuarios/register/', RegistroUsuarioView.as_view(), name='usuario_registro'), # POST /api/usuarios/register/: crea nueva cuenta
    path('usuarios/me/', PerfilUsuarioView.as_view(),   name='perfil_usuario'), # GET  /api/usuarios/me/: muestra datos del usuario autenticado

    # Rutas CRUD de tareas para los propietarios de las mismas
    path('tareas/', TareaListCreateView.as_view(), name='tarea_list_create'), # GET /api/tareas/: lista/filtra tareas propias, POST crea nueva tarea
    path('tareas/<int:pk>/', TareaDetailView.as_view(),   name='tarea_detail'), # GET/PUT/PATCH/DELETE /api/tareas/{pk}/: ver, actualizar o borrar tarea propia
]
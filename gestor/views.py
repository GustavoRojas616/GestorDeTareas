from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Usuario
from .models import Tarea
from .serializers import TareaSerializer
from .serializers import UsuarioRegistroSerializer, UsuarioPerfilSerializer

# Vista para registrar nuevos usuarios
# Como se nos permitió usar CreateAPIView de DRF ya implementa la lógica POST y la validación
class RegistroUsuarioView(generics.CreateAPIView):
    # POST /api/usuarios/register/  → crea un nuevo usuario.
    queryset = Usuario.objects.all()
    serializer_class = UsuarioRegistroSerializer
    #Vamos usar AllowAny para que cualquiera pueda crear cuenta para generar su token en el login
    permission_classes = (permissions.AllowAny,)

# Vista para mostrar el perfil del usuario logueado
# Se usa ahora RetrieveAPIView de DRF
class PerfilUsuarioView(generics.RetrieveAPIView):
    #GET /api/usuarios/me/  → devuelve los datos del usuario autenticado.
    serializer_class = UsuarioPerfilSerializer
    # Se usa IsAuthenticated para que se requiera un token válido
    permission_classes = (permissions.IsAuthenticated,)

    # get_object() retorna directamente el usuario autenticado, sin usar pk
    def get_object(self):
        # De esta forma obtenemos el perfil del usuario que hizo la petición
        return self.request.user
    
# Vista para listar y crear tareas del usuario
# ListCreateAPIView maneja GET y POST, por otro lado la interfaz que se ve es la Browsable API de DRFclass TareaListCreateView(generics.ListCreateAPIView):
class TareaListCreateView(generics.ListCreateAPIView): 
    #GET  /api/tareas/       → lista las tareas del usuario (con filtro ?completed=true/false)
    #POST /api/tareas/       → crea una nueva tarea asignada al usuario.
    serializer_class = TareaSerializer
    # Solo permite ver/añadir las tareas del usuario autenticado
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        # Filtramos tareas para que solo aparezcan las del usuario autenticado
        qs = Tarea.objects.filter(owner=self.request.user)
        #Filtro para tareas completadas
        comp = self.request.query_params.get('completed')
        if comp is not None:
            if comp.lower() in ('true', '1'):
                qs = qs.filter(completed=True)
            elif comp.lower() in ('false', '0'):
                qs = qs.filter(completed=False)
        return qs

    def perform_create(self, serializer):
        # Al crear la tarea, asignamos automáticamente el usuario autenticado como owner
        serializer.save(owner=self.request.user)


# Vista para ver, actualizar o borrar una tarea
# Usamos RetrieveUpdateDestroyAPIView que soporta GET, PUT, PATCH, DELETE
class TareaDetailView(generics.RetrieveUpdateDestroyAPIView):
    #GET    /api/tareas/{pk}/   → detalles de la tarea del dueño que la consulta.
    #PUT    /api/tareas/{pk}/   → actualiza todos los campos.
    #PATCH  /api/tareas/{pk}/   → actualización de completada o no.
    #DELETE /api/tareas/{pk}/   → elimina la tarea.
    serializer_class = TareaSerializer
    # Solo interactua sobre tareas del usuario autenticado
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        # Asegura que solo pueda acceder/editar/borrar sus propias tareas
        return Tarea.objects.filter(owner=self.request.user)
from rest_framework import serializers
from .models import Usuario
from .models import Tarea

# Serializer para el registro de usuarios
# Aquí definimos cómo llegan y se guardan los datos cuando alguien se registra.
class UsuarioRegistroSerializer(serializers.ModelSerializer):
    # Campo para la contraseña, solo se envía del cliente al servidor (solo escritura).
    # además le pedimos mínimo 8 caracteres, es solo para darle un poco más de seguridad.
    password = serializers.CharField(write_only=True, required=True, min_length=8)

    class Meta:
        model = Usuario
        # Campos que vamos a exponer en la API (el id lo deja Django, password solo para crear)
        fields = ('id', 'username', 'email', 'password')

    def create(self, validated_data):
        # Cuando todo pasa las validaciones, creamos el usuario aquí.
        # No guardamos la password directamente, usamos set_password para hashearla.
        user = Usuario(
            username=validated_data['username'],
            email=validated_data['email']
        )
        # Esto convierte la contraseña en un hash seguro
        user.set_password(validated_data['password'])
        user.save() # guardamos el usuario en la base de datos
        return user

# Serializer para mostrar el perfil del usuario autenticado
# Solo lee datos, no permite editar nada.
class UsuarioPerfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        # Mostramos el perfil
        fields = ('id', 'username', 'email', 'is_active')
        # Hacemos todo de solo lectura para que no se cambie por aquí
        read_only_fields = fields


# Serializer para el modelo Tarea
# Aquí definimos cómo entran y salen los datos de las tareas.
class TareaSerializer(serializers.ModelSerializer):
    # El owner se expone como el username, y no se acepta al crear/actualizar
    owner = serializers.ReadOnlyField(source='owner.username')
    # Validación solicituda para que el título deba tener mínimo 3 caracteres
    title = serializers.CharField(min_length=3)
    class Meta:
        model = Tarea
        # Campos que la API maneja para cada tarea
        fields = ('id', 'title', 'description', 'completed', 'created_at', 'owner')
        # Algunos campos son solo de lectura
        read_only_fields = ('id', 'created_at', 'owner')

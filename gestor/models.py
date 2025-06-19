from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    # AbstractUser ya define: username, password, is_active, email, etc.
    # Solo sobreescribimos email para que sea único:
    email = models.EmailField(unique=True)
    def __str__(self):
        return self.username

class Tarea(models.Model):
    title = models.CharField(max_length=200,blank=False, null=False) #Título de la tarea, obligatorio
    description = models.TextField(blank=True, null=True) #Descripción de la tarea, opcional
    completed = models.BooleanField(default=False) #Si la tarea esá completada
    created_at = models.DateTimeField(auto_now_add=True) #Fecha y hora, asignada automáticamente
    owner = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="tareas") #Usuario al que pertenece esta tarea
    
    def __str__(self):
        return self.title
    
#Ambos def __str__ son para darle legibilidad y facilitar la parte del debugging
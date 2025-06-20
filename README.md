# Gestor de Tareas API

API RESTful para gestión de usuarios y tareas con:
- Autenticación JWT
- Paginación
- Documentación Swagger/OpenAPI

---

# Instrucciones para configurar y ejecutar el proyecto

1. Para ejecutar localmente se debe clonar el repositorio 
   **Recuerda tener git instalado para poder seguir con las siguientes líneas de código desde tu terminal**
   git clone https://github.com/GustavoRojas616/GestorDeTareas

2. Entrar en la carpeta del proyecto con
   cd GestorDeTareas

3. Crea y activa un entorno virtual (desde Windows PowerShell)
   python -m venv venv
   .\venv\Scripts\Activate

   Desde Linux/macOS
   python3 -m venv venv
   source venv/bin/activate

4. Instala las dependencias
   pip install -r requirements.txt

5. Al ser una prueba puedes ya proceder a aplicar migraciones y recolectar estáticos que no serviran en estos pasos que es para ejecutar localmente
    python manage.py migrate
    python manage.py collectstatic --noinput

6. Ejecuta el servidor local
    python manage.py runserver

7. Accede mediante el local host
    Rutas disponibles para acceso:
        https://http://127.0.0.1:8000//api/usuarios/register/
        https://http://127.0.0.1:8000//api/auth/login/ 
    
    # Swagger local: http://127.0.0.1:8000/swagger/

Sin embargo, al momento en el cuál se entrega esta prueba se encuentra desplegada, rutas disponible para acceso:
    https://gestordetareas-tx1q.onrender.com/api/usuarios/register/
    https://gestordetareas-tx1q.onrender.com/api/auth/login/ 

# Documentación Swagger
https://gestordetareas-tx1q.onrender.com/swagger/

**NOTA: Se tienen más rutas de acceso, sin embargo, aquellas con las cuales se puede interactuar directamente son las anteriores, las demás se van a especificar en los ejemplos de peticiones cURL**

# Ejemplos de peticiones cURL
Vamos a explicar los ejemplos de peticiones cURL con el proyecto desplegado (cURL considerados para ser ejecutados en Windows PowerShell):

# 1) Registro de usuario
curl.exe --% -X POST https://gestordetareas-tx1q.onrender.com/api/usuarios/register/ -H "Content-Type: application/json" -d "{\"username\":\"pepito\",\"email\":\"pepito@correo.com\",\"password\":\"admin1234\"}"

# 2) Login → obtiene access token y refresh token
curl.exe --% -X POST https://gestordetareas-tx1q.onrender.com/api/auth/login/       -H "Content-Type: application/json" -d "{\"username\":\"pepito\",\"password\":\"admin1234\"}"


# 3) Refresh → renueva el access token
curl.exe --% -X POST https://gestordetareas-tx1q.onrender.com/api/auth/refresh/     -H "Content-Type: application/json" -d "{\"refresh\":\"<refresh_token>\"}"


# 4) Detalle de usuario autenticado
curl.exe --% -X GET  https://gestordetareas-tx1q.onrender.com/api/usuarios/me/      -H "Authorization: Bearer <access_token>"


# 5) Listar todas las tareas (pág. 1)
curl.exe --% -X GET  https://gestordetareas-tx1q.onrender.com/api/tareas/?page=1           -H "Authorization: Bearer <access_token>"


# 6) Listar solo tareas completadas (pág. 1)
curl.exe --% -X GET  "https://gestordetareas-tx1q.onrender.com/api/tareas/?completed=true&page=1"  -H "Authorization: Bearer <access_token>"


# 7) Listar solo tareas pendientes (pág. 1)
curl.exe --% -X GET  "https://gestordetareas-tx1q.onrender.com/api/tareas/?completed=false&page=1" -H "Authorization: Bearer <access_token>"


# 8) Crear una nueva tarea
curl.exe --% -X POST https://gestordetareas-tx1q.onrender.com/api/tareas/           -H "Authorization: Bearer <access_token>" -H "Content-Type: application/json" -d "{\"title\":\"Comprar pan\",\"description\":\"Ir a la tienda\"}"


# 9) Actualizar parcialmente una tarea (PATCH)
curl.exe --% -X PATCH https://gestordetareas-tx1q.onrender.com/api/tareas/<id_tarea>/         -H "Authorization: Bearer <access_token>" -H "Content-Type: application/json" -d "{\"completed\":true}"


# 10) Eliminar una tarea
curl.exe --% -X DELETE https://gestordetareas-tx1q.onrender.com/api/tareas/<id_tarea>/        -H "Authorization: Bearer <access_token>"



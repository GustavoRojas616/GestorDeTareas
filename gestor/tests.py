from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Usuario, Tarea

class TareaEndpointTests(APITestCase):
    """
    Pruebas para los endpoints de Tarea:
      - Crear tarea propia
      - Listar tareas del usuario
      - Actualizar solo tareas propias
      - Bloquear acceso a tareas ajenas
    """

    def setUp(self):
        # 1) Creamos un usuario de prueba con credenciales conocidas
        self.user = Usuario.objects.create_user(
            username='prueba',
            email='prueba@do.com',
            password='12345678'
        )
        # 2) Obtenemos el endpoint de login y solicitamos tokens
        url_login = reverse('token_obtain_pair')
        resp = self.client.post(url_login, {
            'username': 'prueba',
            'password': '12345678'
        }, format='json')
        # Verificamos que el login retorne 200 OK
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        # 3) Guardamos el access token en la cabecera para futuros requests
        token = resp.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    def test_crear_tarea(self):
        """
        POST /api/tareas/ debería crear una tarea nueva:
          - Responder con 201 Created
          - El campo 'owner' debe ser el username del creador
          - El título debe coincidir con el enviado
        """
        url = reverse('tarea_list_create')
        data = {'title': 'Prueba', 'description': 'Algo', 'completed': False}
        resp = self.client.post(url, data, format='json')
        # Comprobamos código HTTP
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        # El owner debe ser 'prueba'
        self.assertEqual(resp.data['owner'], 'prueba')
        # El título debe guardarse correctamente
        self.assertEqual(resp.data['title'], 'Prueba')

    def test_listar_tareas(self):
        """
        GET /api/tareas/ debería devolver solo las tareas del usuario autenticado.
        Se crean dos tareas con distinto estado y se verifica que ambas aparezcan.
        """
        # Creamos dos tareas para el usuario 'prueba'
        Tarea.objects.create(owner=self.user, title='T11', description='', completed=False)
        Tarea.objects.create(owner=self.user, title='T22', description='', completed=True)
        url = reverse('tarea_list_create')
        resp = self.client.get(url, format='json')
        # Debe devolver 200 OK
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        # Al usar paginación, los resultados suelen estar en 'results'
        results = resp.data.get('results', resp.data)
        titles = [t['title'] for t in results]
        # Verificamos que ambas tareas estén en la lista
        self.assertIn('T11', titles)
        self.assertIn('T22', titles)

    def test_actualizar_tarea_propia(self):
        """
        PATCH /api/tareas/{pk}/ solo debe permitir que el propietario marque la tarea.
        Creamos una tarea, la marcamos como completada y comprobamos el cambio.
        """
        task = Tarea.objects.create(owner=self.user, title='Antes', description='', completed=False)
        url = reverse('tarea_detail', args=[task.id])
        resp = self.client.patch(url, {'completed': True}, format='json')
        # El servidor responde 200 OK y el campo 'completed' pasa a True
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue(resp.data['completed'])

    def test_no_puede_modificar_ajena(self):
        """
        Un usuario no debería poder acceder a tareas que no le pertenecen.
        Creamos una tarea de otro usuario y esperamos 404 Not Found.
        """
        other = Usuario.objects.create_user('otro', 'otro@x.com', 'pass1234')
        task2 = Tarea.objects.create(owner=other, title='Ajena', description='', completed=False)
        url2 = reverse('tarea_detail', args=[task2.id])
        resp2 = self.client.get(url2)
        # Django devolverá 404 porque no encuentra esa tarea en el queryset del usuario
        self.assertEqual(resp2.status_code, status.HTTP_404_NOT_FOUND)

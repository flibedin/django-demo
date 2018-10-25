from django.http import HttpRequest
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from AppTwo.models import Cliente
from AppTwo import views
from security import views


class AppTwoTests(TestCase):

    def setUp(self):
        # Create two users
        user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        user1.save()


    # testeo crear un nuevo cliente
    def test_new_cliente(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')

        frm = {'first_name': 'ana',
               'last_name': 'iglesias',
               'email': 'ana@example.com',
               }
        response = self.client.post(reverse('AppTwo:edit'), data=frm)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Clientes')


    # veo si puedo actualizar un cliente
    def test_update_cliente(self):

        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')

        frm = {'first_name': 'ana',
               'last_name': 'prieto',
               'email': 'ana@example.com',
               }

        response = self.client.post(reverse('AppTwo:edit'), data=frm, kwargs={'pk': '1'})
        self.assertContains(response, 'Clientes')

        # verifico si se actualizo
        response = self.client.get(reverse('AppTwo:users'))
        self.assertContains(response, 'prieto')


    # Testea la vista con la lista de Clientes
    def test_client_list(self):

        # creo un par de clientes
        Cliente.objects.create(first_name='sigal', last_name='libedinsky', email='sigal.lp@gmail.com')
        Cliente.objects.create(first_name='ilan', last_name='libedinsky', email='ilan@gmail.com')

        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('AppTwo:users'))
        self.assertContains(response, 'libedinsky')




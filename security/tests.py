
from django.http import HttpRequest
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from AppTwo.models import Cliente
from AppTwo import views
from security import views


class SecurityTests(TestCase):

    def setUp(self):
        # Create two users
        user1 = User.objects.create(username='testuser1')
        user1.set_password('12345')
        user1.save()

        # creo un par de clientes
        Cliente.objects.create(first_name='sigal', last_name='libedinsky',  email='sigal.lp@gmail.com')
        Cliente.objects.create(first_name='ilan', last_name='libedinsky',  email='ilan@gmail.com')

    # testeo el login_required
    def test_login_required(self):
        # accedo a una pagina protegida para usuarios registrados
        response = self.client.get(reverse('AppTwo:users'))
        self.assertRedirects(response, '/security/user_login?next=/users/', fetch_redirect_response=False)


    # simulo el login de un usuario y veo si funciona
    def test_login(self):
        login = self.client.login(username='testuser1', password='12345')
        response = self.client.get(reverse('views.index'))

        # verifico que se cargo la pagina para el usuario autentificado
        self.assertContains(response, 'Perfil')

        # Check if user is logged in
        self.assertEqual(str(response.context['user']), 'testuser1')


    # Test del logout
    def test_logout(self):
        login = self.client.login(username='testuser1', password='12345')

        response = self.client.get(reverse('security:logout'), follow=True)

        self.assertContains(response, 'Login')


    # simulo el Registro de un nuevo usuario
    def test_registration(self):
        frm = {'username': 'ana',
                    'password': 'ana1234',
                    'email': 'ana@example.com',
                    'portfolio': '',
                    'portfolio_pic': '',
                    }

        response = self.client.post(reverse('security:register'), data=frm)
        self.assertContains(response, 'Gracias')

    def test_fail_registration(self):
        frm = {'username': 'ana',
               'password': '',
               'email': 'ana@example.com',
               'portfolio': '',
               'portfolio_pic': '',
               }

        '''
        response = self.client.post(reverse('security:register'), data=frm)

        # verifico que se grabo
        self.assertContains(response, 'Gracias')
        '''






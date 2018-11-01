
from django.http import HttpRequest
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from AppTwo.models import Cliente
from AppTwo import views
from security import views
from security.models import UserProfileInfo

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
        response = self.client.get(reverse('AppTwo:users'),  follow=True)
        self.assertContains(response, 'Login')
        # self.assertRedirects(response, '/security/user_login?next=/users/', fetch_redirect_response=False)


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

        frm = {'username': 'ilan',
                'password': 'ilan1234',
                'email': 'sigal@example.com',
                 'portfolio': '',
                'profile_pic': '',
                 }

        response = self.client.post(reverse('security:register'), data=frm)
        self.assertContains(response, 'Gracias')

        user = User.objects.get(username='ilan')
        self.assertEquals( user.username, 'ilan')
        user.set_password('ilan1234')
        user.save()

        # verifico que pueda logearse
        login = self.client.login(username='ilan', password='ilan1234')
        response = self.client.get(reverse('views.index'))
        self.assertEqual(str(response.context['user']), 'ilan')


    # test de actualización de foto
    def test_photo(self):
        image = '/Users/fernando/Desktop/sigal1.jpg'
        with open(image, 'rb') as fp:
            frm = {'username': 'sigal',
                   'password': 'sigal1234',
                   'email': 'sigal@example.com',
                   'portfolio': '',
                   'profile_pic': fp,
                   }

            # registro un nuevo usuario con su foto
            response = self.client.post(reverse('security:register'), data=frm,  format='multipart')

        self.assertContains(response, 'Gracias')

        user = User.objects.get(username='sigal')


        # me logeo
        login = self.client.login(username='sigal', password='sigal1234')

        # verifico su perfil, que tenga foto
        response = self.client.get(reverse('security:user_detail'))
        self.assertContains(response, 'sigal1')


        # cambio la foto
        with open('/Users/fernando/Desktop/sigal2.jpg', 'rb') as fp:
            response = self.client.post(reverse('security:user_edit'), data={'profile_pic': fp }, format='multipart')


        # verifico el cambio
        response = self.client.get(reverse('security:user_detail'))
        self.assertContains(response, 'sigal2')

        # cambio el apellido
        frm = {'first_name': 'sigal',
               'last_name': 'libedinsky pardo',
               'email': 'sigal@example.com',
                  }
        response = self.client.post(reverse('security:user_edit'), data=frm, follow=True)
        self.assertContains(response, 'pardo')



    def test_fail_registration(self):
        frm = {'username': 'testuser1',
               'password': '',
               'email': 'ana@example.com',
               'portfolio': '',
               'portfolio_pic': '',
               }

        # verifico el caso de usuario ya existente
        response = self.client.post(reverse('security:register'), data=frm)
        self.assertContains(response, 'Ya existe')

        # usuario sin password
        frm['username'] = 'fernando2'
        response = self.client.post(reverse('security:register'), data=frm)
        self.assertContains(response, 'campo es obligatorio')



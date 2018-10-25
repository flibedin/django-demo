
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
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(username='testuser2', password='2HJ1vRV0Z&3iD')

        test_user1.save()
        test_user2.save()

        # creo un par de clientes
        Cliente.objects.create(first_name='sigal', last_name='libedinsky',  email='sigal.lp@gmail.com')
        Cliente.objects.create(first_name='ilan', last_name='libedinsky',  email='ilan@gmail.com')

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('AppTwo:users'))
        self.assertRedirects(response, '/security/user_login?next=/users/', fetch_redirect_response=False)

    def test_logged_in_user(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('AppTwo:users'))

        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser1')
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)
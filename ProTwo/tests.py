
# Create your tests here.
from django.http import HttpRequest
from django.test import TestCase
from django.urls import reverse

from AppTwo import views


class HomePageTests(TestCase):

    def test_home_url(self):
        response = self.client.get(reverse('views.index'))
        self.assertEquals(response.status_code, 200)

    def test_home_view(self):
        response = self.client.get(reverse('views.index'))
        self.assertEquals(response.status_code, 200)


    def test_home_page_contains_correct_html(self):
        response = self.client.get(reverse('views.index'))
        self.assertContains(response, 'Libedinsky')

    def test_home_page_does_not_contain_incorrect_html(self):
        response = self.client.get(reverse('views.index'))
        self.assertNotContains(
            response, 'Hi there! I should not be on the page.')

    def test_home_page_contains_login(self):
        response = self.client.get(reverse('views.index'))
        self.assertContains(response, 'Login')


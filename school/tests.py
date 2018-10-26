from django.http import HttpRequest
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from school.models import School, Student
from school import views
from security import views


class SchoolTests(TestCase):

    def setUp(self):
        # Create a school with a list of students
        school = School( name = 'instituto hebreo', principal = 'Juan Perez',location = 'Santiago')
        school.save()

        # ahora creo estudiantes
        Student.objects.create(name='ilan', age=28, school=school)
        Student.objects.create(name='sigal', age=22, school=school)

    # Lista de escuelas
    def test_school_list(self):
        response = self.client.get(reverse('school:list'))
        self.assertContains(response, 'hebreo')
        self.assertTemplateUsed(response, 'school_list.html')   # Test del template usado

    # testeo la vista de detalle de escuela
    def test_school_detail(self):

        response = self.client.get(reverse('school:detail', kwargs={'pk': '1'}))
        self.assertContains(response, 'Actualizar')


    # actualizar una escuela
    def test_school_update(self):

        frm = {'name': 'instituto hebreo',
               'principal': 'Perico Perez',
               'region': 'Santiago',
               }

        response = self.client.post(reverse('school:update', kwargs={'pk': '1'}), data=frm )
        self.assertContains(response, 'Perico')

    def test_school_delete(self):
        frm = {'name': 'instituto hebreo',
               'principal': 'Perico Perez',
               'region': 'Santiago',
               }

        # primero pruebo  la pagina de confirmación de borrado
        response = self.client.get(reverse('school:delete', kwargs={'pk': '1'}))
        self.assertContains(response, 'Borrar')

        # Aca pruebo el borrado definitivo
        response = self.client.post(reverse('school:delete', kwargs={'pk': '1'}), follow=True)
        self.assertNotContains(response, 'instituto')





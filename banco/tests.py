
# Create your tests here.
from django.http import HttpRequest
from django.test import TestCase
from django.urls import reverse

from . import views
from  banco.models import Cliente, Transaccion


class BancoTests(TestCase):

    # este metodo inicializa los datos para el test
    @classmethod
    def setUpTestData(self):

        # creo una transaccion para todos los tests
        c = Cliente( nombre='sigal', apellido='libedinsky', direccion='California 2537', sucursal='01', sexo='M')
        c.save()

        t = Transaccion( cliente=c, fecha='2018-10-24', monto=95000, tipo='A')
        t.save()

        return


    def test_lista_cliente_banco(self):
        response = self.client.get(reverse('banco:list'))
        self.assertContains(response, 'sigal')

    def test_detail_banco(self):
        response = self.client.get(reverse('banco:detail', kwargs={'pk': '1'}))
        self.assertContains(response, 'California')


    def test_query_banco(self):
        response = self.client.post(reverse('banco:query'), {'cliente': '1'})
        self.assertContains(response, '95000')

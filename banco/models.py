from django.db import models

Sucursales = ( ('01', 'Alameda'), ('02', 'Providencia'), ('03', 'Las Condes'), ('04', 'Vitacura'))

# Create your models here.
class Cliente(models.Model):
    nombre = models.CharField(max_length=64)
    apellido = models.CharField(max_length=64)

    direccion = models.CharField(max_length=256)
    sucursal = models.CharField(max_length=2,choices=Sucursales)
    sexo = models.CharField(max_length=1,choices=( ('H', 'Hombre'), ('M', 'Mujer')))

    def __str__(self):
        return "{} {}".format(self.nombre, self.apellido)


class Transaccion(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha = models.DateField()
    monto = models.PositiveIntegerField()
    tipo = models.CharField(max_length=1,choices=( ('A', 'Abono'), ('R', 'Retiro')))

    def __str__(self):
        return "TX {} {}".format(self.fecha, self.pk)
